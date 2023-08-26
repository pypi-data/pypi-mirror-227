from pathlib import Path
import tempfile
from collections import namedtuple
import onnx
import numpy as np
from onnxruntime.quantization.quant_utils import load_model
from .calibration import calibrate
from . import conv_convert, input_zp_scale, depthwise_convert, gemm_convert
from ..layers.graph_tools import nodes_to_ops_list, array_to_tp, get_tensor_shape, find_by_name
from ..layers import AKIDA_ONNX_LAYERS
from ..layers.base_layer import get_brainchip_opsetid
from ..layers.sanitize import sanitize
from .data_reader import CalibrationDataReader
from ...layers.quantization_params import QuantizationParams

# Define named tuples for QuantizerPattern and Quantizer
QuantizePattern = namedtuple('QuantizerPattern', ['pattern', 'f'])
Quantizer = namedtuple('Quantizer', ['qpattern', 'index', 'len'])

# List of supported patterns, together with matching function
PATTERNS_MAP = [
    QuantizePattern(["Conv", "Relu", "GlobalAveragePool"], conv_convert),
    QuantizePattern(["Conv", "Relu", "MaxPool"], conv_convert),
    QuantizePattern(["Conv", "GlobalAveragePool"], conv_convert),
    QuantizePattern(["Conv", "Relu"], conv_convert),
    QuantizePattern(["Conv"], conv_convert),
    QuantizePattern(["DepthwiseConv", "Relu"], depthwise_convert),
    QuantizePattern(["DepthwiseConv"], depthwise_convert),
    QuantizePattern(["Flatten", "Gemm", "Relu"], gemm_convert),
    QuantizePattern(["Flatten", "Gemm"], gemm_convert),
    QuantizePattern(["Gemm", "Relu"], gemm_convert),
    QuantizePattern(["Gemm"], gemm_convert),
]

QUANTIZED_SUFFIX = "_quantized"
DEQUANTIZED_SUFFIX = "_dequantized"


def get_input_value_info(input_name, graph):
    """
    Given an input name, retrieve its value_info from the graph.

    Args:
        input_name: name of the input to retrieve
        graph: onnx graph

    Returns:
        input_value_info: input value info for the input name
    """
    # Retrieve from previous graph the input shape from graph, with format BCXY
    input_shape = get_tensor_shape(input_name, graph)
    input_dtype = onnx.TensorProto.FLOAT
    # Set batch size as first element
    if input_shape[0] is None:
        input_shape = ("N", *input_shape[1:])
    input_value_info = onnx.helper.make_tensor_value_info(
        input_name, input_dtype, input_shape)
    return input_value_info


def get_output_value_info(output_name, graph):
    """
    Given an output name, retrieve its value_info from the graph.

    Args:
        output_name: name of the output to retrieve
        graph: onnx graph

    Returns:
        output_value_info: output value info for the output name
    """
    # If last layer was dequantizer, remove prefix
    if output_name.endswith(DEQUANTIZED_SUFFIX):
        output_name_in_original_graph = output_name[:-len(DEQUANTIZED_SUFFIX)]
    else:
        output_name_in_original_graph = output_name
    # Retrieve from previous graph the output shape from graph, with format BCXY
    output_shape = get_tensor_shape(output_name_in_original_graph, graph)
    # Set batch size as first element
    if output_shape[0] is None:
        output_shape = ("N", *output_shape[1:])
    output_dtype = onnx.TensorProto.FLOAT
    output_value_info = onnx.helper.make_tensor_value_info(
        output_name, output_dtype, output_shape)
    return output_value_info


def add_dequantizer(scale, input_name):
    """
    Given a scale, create a dequantizer node and its associated scale tensor.

    Args:
        scale: scale to use for dequantizer
        input_name: name of the input to dequantize

    Returns:
        dequantizer: dequantizer node
        onnx_scale: dequantizer scale
    """
    # Onnx scale for dequantizer is reciprocal of akida one
    scale = np.array(scale)
    scale = (1 / scale).astype(np.float32)
    onnx_scale = array_to_tp(deq_scale=scale)
    dequantizer = onnx.helper.make_node(
        'DequantizeLinear',
        inputs=[input_name, 'deq_scale'],
        outputs=[input_name + DEQUANTIZED_SUFFIX],
    )
    return dequantizer, onnx_scale


def add_quantizer(tensor_range, graph):
    """
    Given a tensor range, create a quantizer node and its associated scale and
    zero point tensors.

    Args:
        tensor_range: range to use for quantizer
        graph: onnx graph

    Returns:
        quantizer: quantizer node
        weights: quantizer scale and zero point tensors
    """
    input_name = graph.input[0].name
    scale, zero_point = input_zp_scale(input_name, tensor_range, graph)
    # Scale is reciprocal of Akida one
    scale = np.array(1 / scale, dtype=np.float32)
    weights = array_to_tp(inputs_scale=scale, inputs_zp=zero_point)
    quantizer = onnx.helper.make_node(
        'QuantizeLinear',
        inputs=[input_name, 'inputs_scale', 'inputs_zp'],
        outputs=[input_name + QUANTIZED_SUFFIX],
    )
    return quantizer, weights


def build_model(nodes, weights, input_vinfo, output_vinfo):
    """
    Given a list of nodes, weights, input value info and output value info,
    create a model and return it.

    Args:
        nodes: list of nodes
        weights: list of weights
        input_vinfo: input value info
        output_vinfo: output value info

    Returns:
        model: onnx model build from given data
    """
    graph = onnx.helper.make_graph(nodes,
                                   "quantized_model",
                                   [input_vinfo],
                                   [output_vinfo],
                                   initializer=weights)
    # TODO: modify this so it fills it with opset_imports from nodes
    opset_imports = [get_brainchip_opsetid(), onnx.helper.make_opsetid(
        "", onnx.defs.onnx_opset_version())]
    model = onnx.helper.make_model(graph,
                                   functions=AKIDA_ONNX_LAYERS,
                                   opset_imports=opset_imports
                                   )
    return model


def quantize_calibrated(model, tensors_range):
    """
    Given a calibrated onnx model and associated tensor ranges, create a quantized onnx
    model compatible with Brainchip's Akida IP and returns it as a new onnx model.

    Args:
        model: file path of model to quantize
        tensors_range: dictionary of tensor name and its range.
            Range is a tuple of min and max values.
            Example: {"input_0": (-1.23, +4.56)}

    Returns:
        quantized onnx model.
    """
    # Sanitize the model and make it quantization ready
    model = sanitize(model)

    graph = model.graph
    nodes = list(graph.node)
    ops_list = nodes_to_ops_list(nodes)

    # Split in blocks
    quantizers = []
    i = 0
    while i < len(ops_list):
        pattern_found = False
        for qpattern in PATTERNS_MAP:
            pattern = qpattern.pattern
            pat_len = len(pattern)
            if ops_list[i:i + pat_len] == pattern:
                pattern_found = True
                quantizer = Quantizer(qpattern, i, pat_len)
                quantizers.append(quantizer)
                i += pat_len
                break
        if not pattern_found:
            break

    if i == 0:
        raise RuntimeError("No quantizable pattern found")
    # Save last quantizable block
    last_block_index = i

    # Now create quantized nodes
    # Input scale for first layer will be deduced from tensor_range
    i_scale = None
    qnodes = []
    weights = []

    # Add quantizer at the beginning of the model
    quantizer, q_weights = add_quantizer(tensors_range, graph)
    qnodes.append(quantizer)
    weights += q_weights

    for quantizer in quantizers:
        block_nodes = nodes[quantizer.index:quantizer.index + quantizer.len]
        last_quantizer = quantizer == quantizers[-1]
        qnode, i_scale, onnx_weights = quantizer.qpattern.f(
            block_nodes, tensors_range, graph, i_scale, last_quantizer)
        qnodes.append(qnode)
        weights += onnx_weights
    # Fix first converted node input, with quantizer output
    qnodes[1].input[0] = qnodes[0].output[0]

    # Append dequantizer
    deq, deq_scale = add_dequantizer(i_scale, qnodes[-1].output[0])
    qnodes.append(deq)
    weights += deq_scale

    # If there were non-quantized nodes, add them
    # Note: This code will not work with skip connections
    if last_block_index < len(ops_list):
        # Get list of all initializer names
        initializer_names = set(init.name for init in graph.initializer)
        deq_index = len(qnodes) - 1
        for i in range(last_block_index, len(ops_list)):
            # just copy the node as it was
            qnodes.append(nodes[i])
            # Get the initializers associated with the node
            # and add them to the list of weights
            node_init_names = [
                n for n in nodes[i].input if n in initializer_names]
            new_weights = [find_by_name(n, graph.initializer)
                           for n in node_init_names]
            weights += new_weights
        # Update new_node input to match dequantized output
        qnodes[deq_index + 1].input[0] = qnodes[deq_index].output[0]

    # Create value info for inputs and outputs (same for old and new graph)
    inputs_vinfo = get_input_value_info(qnodes[0].input[0], graph)
    outputs_vinfo = get_output_value_info(qnodes[-1].output[0], graph)

    # Finally build model
    qmodel = build_model(qnodes, weights, inputs_vinfo, outputs_vinfo)
    return qmodel


def quantize(model_input,
             qparams=QuantizationParams(),
             samples=None,
             num_samples=1024,
             batch_size=None):
    """
    Given an onnx model and calibration data reader, create a quantized onnx
    model compatible with Brainchip's Akida IP and returns it as a new onnx model.

    Args:

        model_input (ModelProto): the onnx model instance to quantize
        qparams (QuantizationParams, optional): Quantization parameters. It is used
            to determine if quantizing per-tensor or per-axis.
        samples (list of numpy arrays, optional): List of input samples to use for
            calibration. If not provided, random samples will be generated. Defaults
            to None.
        num_samples (int, optional): Number of samples to use for calibration.
            Defaults to 1024.
        batch_size (int, optional): Batch size to use for calibration. Defaults to
            None.

    Returns:
        quantized onnx model.
    """
    # For now only a limited QuantizationParams configuration is supported: test that
    if (
            qparams.activation_bits != 8 or
            qparams.buffer_bits != 32 or
            qparams.input_weight_bits != 8 or
            qparams.output_bits != 8 or
            qparams.weight_bits != 8):
        raise ValueError("Only default bitwidth params params qparams is allowed.")

    with tempfile.TemporaryDirectory(prefix="pre.quant.") as quant_tmp_dir:
        # To perfom ONNXRuntime optimization, we would like to use
        # onnxruntime.quantization.load_model, to optimize the model (when required)
        # and infer the intermediate shapes.
        # However, it always expects to read the model from a path. That is why we
        # save the input model if it is not a path.
        onnx.save_model(model_input, f"{quant_tmp_dir}/model.onnx")
        model_input = f"{quant_tmp_dir}/model.onnx"

        # Perform preprocessing
        model = load_model(Path(model_input), need_optimize=True)

    # Compute statistical ranges
    # Create a calibration data reader from given samples. Note that by default,
    # MEAN_0 rescale_type is chosen.
    calibration_data_reader = CalibrationDataReader(
        model, samples, num_samples, batch_size, rescale_type="MEAN_0")
    tensors_range = calibrate(model,
                              calibration_data_reader,
                              per_tensor_activations=qparams.per_tensor_activations)

    qmodel = quantize_calibrated(model, tensors_range)
    return qmodel
