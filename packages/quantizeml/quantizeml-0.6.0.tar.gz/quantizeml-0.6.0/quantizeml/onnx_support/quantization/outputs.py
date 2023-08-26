import numpy as np

from ..layers.fixed_point import to_fixed_point
from .input_scale import AKIDA_IO_MAX


def downscale(output_range, i_scale, bitwidth=8):
    """Calculates the scale that should be applied to an integer tensor
    with i_scale to project it to a desired bitwidth.

    The following set of operations must be applied to the tensor to project it
    into the output scale:

    >>> out_tensor = tensor * scale
    >>> out_tensor = out_tensor >> log2(shift)

    Args:
        output_range (tuple of np.ndarray): the MinMax calibrated tuple
        i_scale (np.ndarray): the input scale
        bitwidth (int): the desired output width

    Returns:
        np.ndarray, np.ndarray, np.ndarray: the integer scale/shift and the new float scale
    """
    assert len(output_range) == 2, "Expected (min,max) in output_range."
    # Compute symmetrical range
    output_max = np.maximum(np.abs(output_range[0]), np.abs(output_range[1]))
    # Replace output_max == 0 by an epsilon to avoid divide by zero
    output_max = np.maximum(output_max, 1e-7)
    # "Correct" output scale taking max_value into account. Note: we consider
    # all conv outputs to be 8 bit, otherwise the scale would be different.
    ocalib_scale = AKIDA_IO_MAX / output_max
    # Divide o_calib_scale by i_scale in the same axis to obtain output scale:
    # this will consider the input scale into account.
    align_shape = [1] * (i_scale.ndim - 1)
    o_scale = ocalib_scale.reshape((-1, *align_shape)) / i_scale
    # Quantize o_scale to fit in scale + shift at 8 bit
    scale, shift = to_fixed_point(o_scale, bitwidth=bitwidth, signed=False)
    # Return shift value as a power of two
    s_out = np.array(2. ** shift, dtype=np.int32)
    return scale, s_out, ocalib_scale
