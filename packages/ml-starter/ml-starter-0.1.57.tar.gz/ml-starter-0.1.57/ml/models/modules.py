"""Miscellaneous shared modules which can be used in various models."""

import math

import torch
import torch.nn.functional as F
from torch import Tensor, nn
from torch.autograd.function import Function, FunctionCtx
from torch.nn.common_types import _size_1_t
from torch.nn.modules.utils import _single


class _InvertGrad(Function):
    @staticmethod
    def forward(ctx: FunctionCtx, input: Tensor, scale: float) -> Tensor:  # type: ignore[override]
        ctx.scale = scale
        return input

    @staticmethod
    def backward(ctx: FunctionCtx, grad_output: Tensor) -> tuple[Tensor, None]:  # type: ignore[override]
        return grad_output * ctx.scale, None


def scale_grad(x: Tensor, scale: float) -> Tensor:
    """Scales the gradient of the input.

    Args:
        x: Input tensor.
        scale: Scale factor.

    Returns:
        The identity of the input tensor in the forward pass, and the scaled
        gradient in the backward pass.
    """
    return _InvertGrad.apply(x, scale)


def invert_grad(x: Tensor) -> Tensor:
    return scale_grad(x, -1.0)


class _SwapGrads(Function):
    @staticmethod
    def forward(ctx: FunctionCtx, x: Tensor, y: Tensor) -> tuple[Tensor, Tensor]:  # type: ignore[override]
        return x, y

    @staticmethod
    def backward(ctx: FunctionCtx, grad_x: Tensor, grad_y: Tensor) -> tuple[Tensor, Tensor]:  # type: ignore[override]
        return grad_y, grad_x


def swap_grads(x: Tensor, y: Tensor) -> tuple[Tensor, Tensor]:
    """Swaps the gradients of the inputs.

    On the forward pass, this function returns the identity of the inputs.
    On the backward pass, the gradients of X and Y are swapped.

    Args:
        x: First input tensor.
        y: Second input tensor.

    Returns:
        The identity of the inputs in the forward pass, and the swapped
        gradients in the backward pass.
    """
    return _SwapGrads.apply(x, y)


class _CombineGrads(Function):
    @staticmethod
    def forward(ctx: FunctionCtx, x: Tensor, y: Tensor) -> tuple[Tensor, Tensor]:  # type: ignore[override]
        return x, y

    @staticmethod
    def backward(ctx: FunctionCtx, grad_x: Tensor, grad_y: Tensor) -> tuple[Tensor, Tensor]:  # type: ignore[override]
        grad = grad_x + grad_y
        return grad, grad


def combine_grads(x: Tensor, y: Tensor) -> tuple[Tensor, Tensor]:
    """Combines the gradients of the inputs.

    On the forward pass, this function returns the identity of the inputs.
    On the backward pass, the gradients of X and Y are summed.

    Args:
        x: First input tensor.
        y: Second input tensor.

    Returns:
        The identity of the inputs in the forward pass, and the summed
        gradients in the backward pass.
    """
    return _CombineGrads.apply(x, y)


def streaming_conv_1d(
    x: Tensor,
    state: tuple[Tensor, int] | None,
    weight: Tensor,
    bias: Tensor | None,
    stride: int,
    dilation: int,
    groups: int,
) -> tuple[Tensor, tuple[Tensor, int]]:
    """Applies a streaming convolution.

    Args:
        x: The input to the convolution.
        state: The state of the convolution, which is the part of the previous
            input which is left over for computing the current convolution,
            along with an integer tracker for the number of samples to clip
            from the current input.
        weight: The convolution weights.
        bias: The convolution bias.
        stride: The convolution stride.
        dilation: The convolution dilation.
        groups: The convolution groups.

    Returns:
        The output of the convolution, plus the new state tracker.
    """
    pre_x = state[0] if state is not None else None
    pre_t = state[1] if state is not None else 0
    if pre_x is not None:
        x = torch.cat((pre_x, x), dim=-1)
    if pre_t > 0:
        pre_t, x = pre_t - x.shape[-1], x[..., pre_t:]
    (bsz, _, tsz), (chsz_out, _, ksize) = x.shape, weight.shape
    min_tsz = 1 + (ksize - 1) * dilation
    if tsz < min_tsz:
        return x.new_zeros(bsz, chsz_out, 0), (x, pre_t)
    y = F.conv1d(x, weight, bias, stride, 0, dilation, groups)
    t = stride * y.shape[-1]
    return y, (x[:, :, t:], max(0, t - tsz))


def streaming_conv_transpose_1d(
    x: Tensor,
    state: tuple[Tensor, int] | None,
    weight: Tensor,
    bias: Tensor | None,
    stride: int,
    dilation: int,
    groups: int,
) -> tuple[Tensor, tuple[Tensor, int]]:
    """Applies a streaming transposed convolution.

    Args:
        x: The input to the convolution.
        state: The state of the convolution, which is the part of the previous
            input which is left over for computing the current convolution,
            along with an integer tracker for the number of samples to clip
            from the current input.
        weight: The convolution weights.
        bias: The convolution bias.
        stride: The convolution stride.
        dilation: The convolution dilation.
        groups: The convolution groups.

    Returns:
        The output of the convolution, plus the new state tracker.
    """
    y = F.conv_transpose1d(x, weight, bias, stride, 0, 0, groups, dilation)
    post_y = state[0] if state is not None else None
    post_t = state[1] if state is not None else 0
    bsz, chsz_out, tsz = y.shape
    if post_t > 0:
        init_y = y.new_zeros(bsz, chsz_out, post_t)
        if bias is not None:
            init_y += bias[..., None]
        y = torch.cat([init_y, y], dim=-1)
    if post_y is not None:
        n = min(post_y.shape[-1], y.shape[-1])
        init_y = post_y[..., :n] + y[..., :n]
        if bias is not None:
            init_y -= bias[..., None]
        y = torch.cat((init_y, post_y[..., n:], y[..., n:]), dim=-1)
    t = stride * x.shape[-1]
    return y[..., :t], (y[..., t:], max(0, t - tsz))


class StreamingConv1d(nn.Module):
    """Defines a streaming 1D convolution layer.

    This is analogous to streaming RNNs, where a state is maintained going
    forward in time. For convolutions, the state is simply the part of the
    previous input which is left over for computing the current convolution,
    along with an integer tracker for the number of samples to clip from the
    current input.

    Note that this is a drop-in replacement for ``nn.Conv1d`` so far as the
    weights and biases go, but the forward pass takes an additional state
    argument and returns an additional state output.
    """

    __constants__ = ["stride", "dilation", "groups", "in_channels", "out_channels", "kernel_size"]

    def __init__(
        self,
        in_channels: int,
        out_channels: int,
        kernel_size: _size_1_t,
        stride: _size_1_t = 1,
        dilation: _size_1_t = 1,
        groups: int = 1,
        bias: bool = True,
    ) -> None:
        super().__init__()

        self.kernel_size = _single(kernel_size)
        self.stride = _single(stride)
        self.dilation = _single(dilation)
        self.groups = groups
        self.in_channels = in_channels
        self.out_channels = out_channels

        self.weight = nn.Parameter(torch.empty((out_channels, in_channels // groups, *self.kernel_size)))
        if bias:
            self.bias = nn.Parameter(torch.empty(out_channels))
        else:
            self.register_parameter("bias", None)
        self.reset_parameters()

    def reset_parameters(self) -> None:
        nn.init.kaiming_uniform_(self.weight, a=math.sqrt(5))
        if self.bias is not None:
            fan_in, _ = nn.init._calculate_fan_in_and_fan_out(self.weight)
            if fan_in != 0:
                bound = 1 / math.sqrt(fan_in)
                nn.init.uniform_(self.bias, -bound, bound)

    def forward(self, x: Tensor, state: tuple[Tensor, int] | None = None) -> tuple[Tensor, tuple[Tensor, int]]:
        weight, bias, stride, dilation, groups = self.weight, self.bias, self.stride[0], self.dilation[0], self.groups
        return streaming_conv_1d(x, state, weight, bias, stride, dilation, groups)


class StreamingConvTranspose1d(nn.Module):
    __constants__ = ["stride", "dilation", "groups", "in_channels", "out_channels", "kernel_size"]

    def __init__(
        self,
        in_channels: int,
        out_channels: int,
        kernel_size: _size_1_t,
        stride: _size_1_t = 1,
        dilation: _size_1_t = 1,
        groups: int = 1,
        bias: bool = True,
    ) -> None:
        super().__init__()

        self.kernel_size = _single(kernel_size)
        self.stride = _single(stride)
        self.dilation = _single(dilation)
        self.groups = groups
        self.in_channels = in_channels
        self.out_channels = out_channels

        self.weight = nn.Parameter(torch.empty((in_channels, out_channels // groups, *self.kernel_size)))
        if bias:
            self.bias = nn.Parameter(torch.empty(out_channels))
        else:
            self.register_parameter("bias", None)
        self.reset_parameters()

    def reset_parameters(self) -> None:
        nn.init.kaiming_uniform_(self.weight, a=math.sqrt(5))
        if self.bias is not None:
            fan_in, _ = nn.init._calculate_fan_in_and_fan_out(self.weight)
            if fan_in != 0:
                bound = 1 / math.sqrt(fan_in)
                nn.init.uniform_(self.bias, -bound, bound)

    def forward(self, x: Tensor, state: tuple[Tensor, int] | None = None) -> tuple[Tensor, tuple[Tensor, int]]:
        weight, bias, stride, dilation, groups = self.weight, self.bias, self.stride[0], self.dilation[0], self.groups
        return streaming_conv_transpose_1d(x, state, weight, bias, stride, dilation, groups)
