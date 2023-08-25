# Copyright 2021 Huawei Technologies Co., Ltd
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ============================================================================

"""inner_ops"""
from __future__ import absolute_import

from mindspore.ops.operations.comm_ops import _VirtualPipelineEnd
from mindspore.ops.operations import _inner_ops as inner
from mindspore.ops.operations import _grad_ops as G
from mindspore.ops import functional as F
from mindspore.ops import operations as P
from mindspore.ops.composite.multitype_ops.zeros_like_impl import zeros_like
from mindspore.ops.primitive import _primexpr
from mindspore.ops._grad_experimental.grad_base import bprop_getters, sum_grad_reduce_axis
import mindspore as ms

reshape = P.Reshape()


@bprop_getters.register(inner.TensorCopySlices)
def get_bprop_tensor_copy_slices(self):
    """Generate bprop for TensorCopySlices"""
    tensor_copy_slices = inner.TensorCopySlices()

    def bprop(x, update, begin, end, stride, out, dout):
        x_grad = tensor_copy_slices(dout, zeros_like(update), begin, end, stride)
        update_grad = F.strided_slice(dout, begin, end, stride)
        res = (x_grad, update_grad, zeros_like(begin), zeros_like(end), zeros_like(stride))
        return res

    return bprop


@bprop_getters.register(_VirtualPipelineEnd)
def get_bprop_virtual_pipeline_end(self):
    """Backpropagator for _VirtualPipelineEnd."""
    grad = _VirtualPipelineEnd()

    def bprop(x, out, dout):
        dx = grad(dout)
        return (dx,)
    return bprop


@bprop_getters.register(inner.DynamicResizeNearestNeighbor)
def get_bprop_dynamic_resize_nearest_neighbor(self):
    """Generate bprop for DynamicResizeNearestNeighbor"""
    op = G.ResizeNearestNeighborGrad(self.align_corners)
    shape_op = P.Shape()

    def bprop(inputs, size, out, dout):
        shp = shape_op(inputs)
        # 2 and 3 represent the height and width
        shp = (shp[2:])
        return (op(dout, shp), zeros_like(size))

    return bprop


@bprop_getters.register(inner.ParallelResizeBilinear)
def get_bprop_parallel_resize_bilinear(self):
    """Grad definition for `ParallelResizeBilinear` operation."""
    grad = G.ParallelResizeBilinearGrad(self.ori_image_size, self.src_start_w, self.dst_start_w,
                                        self.align_corners)

    def bprop(x, size, out, dout):
        dx = grad(dout, x, size)
        return dx, zeros_like(size)

    return bprop


@bprop_getters.register(inner.ConvertToDynamic)
def get_bprop_gpu_convert_to_dynamic_rank(self):
    """Get backprop for ConvertToDynamic."""

    def bprop(x, out, dout):
        return (dout,)
    return bprop


def _get_matrix_diag_assist(x_shape, x_dtype):
    base_eye = P.Eye()(x_shape[-1], x_shape[-1], x_dtype).flatten()
    tile = P.Tile()(base_eye, x_shape[:-1])
    assist = P.Reshape()(tile, x_shape + (x_shape[-1],))
    return assist


def _get_matrix_diag_part_assist(x_shape, x_dtype):
    base_eye = P.Eye()(x_shape[-2], x_shape[-1], x_dtype).flatten()
    tile = P.Tile()(base_eye, x_shape[:-2])
    assist = P.Reshape()(tile, x_shape)
    return assist


@_primexpr
def _get_min(x):
    return min(x)


@bprop_getters.register(inner.MatrixDiag)
def get_bprop_matrix_diag(self):
    """Generate bprop for MatrixDiag"""
    get_dtype = P.DType()

    def bprop(x, y, out, dout):
        shape = F.shape(dout)
        dtype = get_dtype(dout)
        assist = _get_matrix_diag_part_assist(shape, dtype)
        dx = inner.MatrixDiagPart()(dout, assist)
        return dx, zeros_like(y)

    return bprop


@bprop_getters.register(inner.MatrixDiagPart)
def get_bprop_matrix_diag_part(self):
    """Generate bprop for MatrixDiagPart"""
    get_dtype = P.DType()

    def bprop(x, y, out, dout):
        x_shape = F.shape(x)[-2:]
        if x_shape[0] == x_shape[1]:
            shape = F.shape(dout)
            dtype = get_dtype(dout)
            assist = _get_matrix_diag_assist(shape, dtype)
            return inner.MatrixDiag()(dout, assist), zeros_like(y)
        shape = F.shape(x)
        dtype = get_dtype(x)
        assist = _get_matrix_diag_part_assist(shape, dtype)
        return inner.MatrixSetDiag()(zeros_like(x), dout, assist), zeros_like(y)

    return bprop


@bprop_getters.register(inner.MatrixSetDiag)
def get_bprop_matrix_set_diag(self):
    """Generate bprop for MatrixSetDiag"""
    get_dtype = P.DType()

    def bprop(x, y, z, out, dout):
        input_shape = F.shape(x)
        batch_shape = input_shape[:-2]
        matrix_shape = input_shape[-2:]
        diag_shape = batch_shape + (_get_min(matrix_shape),)

        grad_shape = F.shape(dout)
        grad_dtype = get_dtype(dout)
        assist = _get_matrix_diag_part_assist(grad_shape, grad_dtype)
        dx = inner.MatrixSetDiag()(dout, P.Zeros()(diag_shape, grad_dtype), assist)
        dy = inner.MatrixDiagPart()(dout, assist)
        dz = zeros_like(z)
        return dx, dy, dz

    return bprop


@bprop_getters.register(inner.DSDMatmul)
def get_dsd_matmul_bprop(self):
    def bprop(w1_gm, w2_gm, v_gm, out, dout):
        d_w1_gm, d_w2_gm, d_v_gm = inner.DSDGrad()(w1_gm, w2_gm, v_gm, out, dout)
        return d_w1_gm, d_w2_gm, d_v_gm

    return bprop


@bprop_getters.register(inner.MatmulDDS)
def get_bprop(self):
    """brop of the matmulDDS operator"""

    def bprop(q, k, local_mask, global_mask, out, d_out):
        lc, gc = out
        d_lc, d_gc = d_out
        dq, dk = inner.MatmulDDSGrad()(q, k, lc, gc, d_lc, d_gc)
        dk = P.Transpose()(dk, (1, 0, 3, 2))
        all_d = (dq, dk, zeros_like(local_mask), zeros_like(global_mask))
        return all_d

    return bprop


@bprop_getters.register(inner.PsROIPooling)
def get_bprop_ps_roi_pooling(self):
    """Grad definition for `PsROIPooling` operation."""
    shape_op = P.Shape()
    pooled_height = self.pooled_height
    pooled_width = self.pooled_width
    spatial_scale = self.spatial_scale
    out_dim = self.out_dim
    num_rois = self.num_rois

    def bprop(inputs, rois, out, dout):
        mapping_channel = out[1]
        inputs_shape = shape_op(inputs)
        batch_size = inputs_shape[0]
        channels = inputs_shape[1]
        height = inputs_shape[2]
        width = inputs_shape[3]

        dx = G.PsROIPoolingGrad(
            batch_size,
            channels,
            height,
            width,
            num_rois,
            pooled_height,
            pooled_width,
            spatial_scale,
            out_dim
        )(dout[0], rois, mapping_channel)

        return dx, zeros_like(rois)

    return bprop


@bprop_getters.register(inner.DynamicBroadcastTo)
def get_bprop_dynamic_broadcast_to(self):
    """Generate bprop for DynamicBroadcastTo"""
    shape_op = P.Shape()

    def bprop(x, shp, out, dout):
        x_shape = shape_op(x)
        broadcast_shape = shape_op(out)

        _, reduction_axes = inner.DynamicBroadcastGradientArgs()(broadcast_shape, x_shape)
        out_type = dout.dtype
        if out_type in (ms.int16, ms.int32, ms.int64):
            dout = P.Cast()(dout, ms.float32)
            reduced_grad = sum_grad_reduce_axis(dout, reduction_axes, keep_dims=True)
            reduced_grad = P.Cast()(reduced_grad, out_type)
        else:
            reduced_grad = sum_grad_reduce_axis(dout, reduction_axes, keep_dims=True)
        dx = reshape(reduced_grad, x_shape)
        return dx, zeros_like(shp)

    return bprop


@bprop_getters.register(inner.ConvertToAdapterTensor)
def get_bprop_convert_to_adapter_tensor(self):
    """Generate bprop for ConvertToAdapterTensor"""

    def bprop(x, out, dout):
        return (dout,)

    return bprop


@bprop_getters.register(inner.ConvertToMsTensor)
def get_bprop_convert_to_ms_tensor(self):
    """Generate bprop for ConvertToMsTensor"""

    def bprop(x, out, dout):
        return (dout,)

    return bprop


@bprop_getters.register(inner.SiLU)
def get_bprop_silu(self):
    """Generate bprop for SiLU"""
    sigmoid_grad = G.SigmoidGrad()
    mul_func = P.Mul()

    def bprop(x, out, dout):
        sigmoid_input = P.Sigmoid()(x)
        bc_dx = mul_func(x, dout)
        bc_dy = mul_func(sigmoid_input, dout)
        dx = sigmoid_grad(sigmoid_input, bc_dx)
        return (dx+bc_dy,)

    return bprop
