import numpy as np
import warnings

import onnx
from onnxruntime.quantization import CalibrationDataReader as _CalibrationDataReader

from ..layers.graph_tools import get_tensor_dtype, get_tensor_shape


def preprocessing(samples, output_type, rescale_type="01"):
    """Project input samples in one of the following output ranges:

        - rescale_type="IMAGENET": samples rescaled following the legacy IMAGENET preprocessing
        - rescale_type="MEAN_0": samples rescaled to [-1, 1]
        - rescale_type="255": samples rescaled to [0, 255]
        - rescale_type="01": samples rescaled to [0, 1]

    Args:
        samples (np.ndarray): samples to rescale.
        output_type (np.dtype): the expected output type.
        rescale_type (str, optional): the rescale type. Defaults to "01".

    Returns:
        np.ndarray: the projected array

    Note: If output type is integer, rescale_type is ignored
          (e.g. np.int8 expects samples between [-128, 127]).
    """
    assert samples.ndim >= 2, "Unsupport samples with less than 2 dimensions"
    output_type = np.dtype(output_type)

    # Compute input scale and offset
    samples_range = [samples.min(), samples.max()]
    assert samples_range[0] != samples_range[1]
    in_scale = 1 / (samples_range[1] - samples_range[0])
    in_offset = samples_range[0] * -in_scale

    # Define output scale/offset
    if issubclass(output_type.type, np.integer):
        # Ignore rescale when model expects integer inputs
        iinfo = np.iinfo(output_type)
        out_scale = 1 / (iinfo.max - iinfo.min)
        out_offset = -float(iinfo.min) * out_scale
    elif rescale_type == 'IMAGENET':
        # Samples rescaled to IMAGENET mean/std
        assert samples.shape[1] == 3, "Unsupported rescale for non-RGB inputs"
        reshape_to = (1, -1) + tuple([1] * (samples.ndim - 2))
        out_scale = np.array([0.229, 0.224, 0.225]).reshape(reshape_to)
        out_offset = np.array([0.485, 0.456, 0.406]).reshape(reshape_to)
    elif rescale_type == 'MEAN_0':
        # Samples rescaled to [-1, 1]
        out_offset, out_scale = 0.5, 0.5
    elif rescale_type == '255':
        # Samples rescaled to [0, 255]
        out_offset, out_scale = 0, 1 / 255.0
    elif rescale_type == "01":
        # Samples rescaled to [0, 1]
        out_offset, out_scale = 0.0, 1.0
    else:
        raise ValueError(f"Unrecognized {rescale_type} rescale. "
                         "Choose one of {'IMAGENET', 'MEAN_0', '255', '01'}.")

    # Compute parameters to project samples into new ranges
    alpha = in_scale / out_scale
    beta = alpha * (in_offset / out_scale) - (out_offset / out_scale)

    # Rescale the samples and convert to expect type
    samples = alpha * samples + beta
    return samples.astype(output_type)


class CalibrationDataReader(_CalibrationDataReader):
    """Object to read or generate a set of samples to calibrate an ONNX model to be quantized.

    Also, it performs a desired preprocessing, following the :attr:`rescale_type` attribute.
    See :func:`preprocessing` for more details.

    Common use mode:
    >>> dr = CalibrationDataReader(onnx_path, num_samples=10, batch_size=1, rescale_type="01")
    >>> sample = dr.get_next()
    >>> assert sample[dr.inputs_name].shape[0] == 1
    >>> assert sample[dr.inputs_name].min() > 0
    >>> assert sample[dr.inputs_name].max() < 1

    Args:
        model (str or ModelProto): the ONNX model (or its path) to be calibrated.
        samples (str or np.ndarray, optional): the samples (or its path) to process.
            If not provided, generate random samples following the model input shape
            and the batch_size attribute. Defaults to None.
        num_samples (int, optional): the number of samples to generate.
            Ignore it if samples are provided. Defaults to None.
        batch_size (int, optional): split samples in batches.
            Overwrite it when the model has static inputs. Defaults to 1.
        rescale_type (str, optional): the projection type, one of
            {'IMAGENET', 'MEAN_0', '01', '255'}. Defaults to "01".
    """

    def __init__(self,
                 model,
                 samples=None,
                 num_samples=None,
                 batch_size=1,
                 rescale_type="01"):

        model, samples = _read_model_samples(model, samples)
        self.inputs_name = model.graph.input[0].name

        # Set mandatory batch size when model is not batchable
        input_shape = get_tensor_shape(model.graph.input[0].name, model.graph)
        self.batch_size = input_shape[0] or batch_size or 1

        # Generate random samples if needed
        self.dataset = samples
        input_type = get_tensor_dtype(model.graph.input[0].name, model.graph)
        if samples is None:
            if num_samples is None:
                raise ValueError("Either samples or num_samples must be specified")
            samples = np.random.rand(num_samples * self.batch_size, *input_shape[1:])
            self.dataset = preprocessing(samples, input_type, rescale_type)
        elif input_shape[0] is not None:
            # Truncate samples to fit model batch size
            N = (samples.shape[0] // self.batch_size) * self.batch_size
            if N != samples.shape[0]:
                warnings.warn("Truncating samples to fit model batch size "
                              f"({N} instead of {samples.shape[0]}).")
                self.dataset = samples[:N]

        # Verify that dataset type is the same as the model input type
        assert self.dataset.dtype == input_type
        # Process samples
        self.index = 0
        self.num_samples = self.dataset.shape[0] / self.batch_size

        # Check samples are the expected model shape
        if self.dataset.shape[1:] != input_shape[1:]:
            raise RuntimeError("Samples shape does not match model input shape. "
                               f"Please verify samples are compatible with {input_shape}.")

    def get_next(self):
        if self.index >= self.num_samples:
            print(f"\rCalibrating with {self.index}/{self.num_samples} samples", end="")
            return print()

        sample = self.dataset[self.index * self.batch_size:(self.index + 1) * self.batch_size]
        self.index += 1
        return {self.inputs_name: sample}

    def rewind(self):
        self.index = 0


def _read_model_samples(model, samples):
    if isinstance(samples, str):
        data = np.load(samples)
        samples = np.concatenate([data[item] for item in data.files])
    if isinstance(model, str):
        model = onnx.load_model(model)

    assert len(model.graph.input) == 1, "multi-input are not supported models yet"
    assert len(model.graph.output) == 1, "multi-outputs are not supported models yet"
    assert isinstance(samples, np.ndarray) or samples is None, f"Unrecognized samples {samples}"
    return model, samples
