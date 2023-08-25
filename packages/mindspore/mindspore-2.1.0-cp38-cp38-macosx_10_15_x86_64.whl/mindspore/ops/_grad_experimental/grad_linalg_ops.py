# Copyright 2022 Huawei Technologies Co., Ltd
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

"""Define the grad rules of linalg related operations."""
from __future__ import absolute_import

import mindspore

from mindspore.ops import Tensor
from mindspore.ops import functional as F
from mindspore.ops import operations as P
from mindspore.ops.composite.multitype_ops.zeros_like_impl import zeros_like
from mindspore.ops.operations import math_ops as math
from mindspore.ops.operations import linalg_ops as linalg
from mindspore.ops.operations import array_ops as arrays
from mindspore.ops.primitive import constexpr, _primexpr
from mindspore.ops._grad_experimental.grad_base import bprop_getters

_shape = arrays.Shape()

_dtype = arrays.DType()
_cast = arrays.Cast()
_transpose = arrays.Transpose()

_conj = math.Conj()
_reciprocal = math.Reciprocal()

_k_0 = Tensor(0, mindspore.int32)


@_primexpr
def _check_dim(dim):
    if dim < 2:
        raise ValueError(f"The dim can not be less than 2, which is {dim}.")


@_primexpr
def generate_perm_for_matrix_transpose(input_dim):
    perm = tuple(range(input_dim - 2))
    perm = perm + (input_dim - 1, input_dim - 2)
    return perm


def _matrix_transpose(a):
    """Transpose last two axes"""
    a_shape = _shape(a)
    if F.is_sequence_value_unknown(a_shape):
        dim = P.Rank()(a)
        perm = P.Range()(P.Cast()(0, mindspore.int64), P.Cast()(dim, mindspore.int64), P.Cast()(1, mindspore.int64))
        perm = P.Concat(axis=-1)((perm[:-2], perm[-1:], perm[-2:-1]))
    else:
        dim = P.Rank()(a)
        _check_dim(dim)
        perm = generate_perm_for_matrix_transpose(dim)
    return _transpose(a, perm)


def _adjoint(a):
    return _matrix_transpose(_conj(a))


def _safe_reciprocal(x, epsilon=1e-20):
    return x * _reciprocal(x * x + epsilon)


@constexpr
def _make_tensor(value, dtype):
    return Tensor(value, dtype)


def _matrix_diag(diagonal):
    """Do matrix diagnoal"""
    diagonal_shape = _shape(diagonal)
    if F.is_sequence_value_unknown(diagonal_shape):
        row = P.Cast()(diagonal_shape[-1], mindspore.int32)
        return arrays.MatrixDiagV3()(diagonal, _k_0, row, row, P.Cast()(0, _dtype(diagonal)))

    row = _make_tensor(diagonal_shape[-1], mindspore.int32)
    return arrays.MatrixDiagV3()(diagonal, _k_0, row, row, _make_tensor(0, _dtype(diagonal)))


def _mat_mul(x, y):
    """Do matmul"""
    tensor_rank = P.Rank()(x)
    if tensor_rank > 2:
        return math.BatchMatMul()(x, y)
    return math.MatMul()(x, y)


@bprop_getters.register(linalg.Svd)
def get_bprop_svd(self):
    """Generate bprop for Svd"""
    full_matrices = self.full_matrices
    compute_uv = self.compute_uv

    svd = linalg.Svd(compute_uv=True)
    square = math.Square()
    matrix_set_diag = arrays.MatrixSetDiagV3()
    expand_dims = arrays.ExpandDims()

    def bprop(a, out, dout):
        if not compute_uv:
            s, u, v = svd(a)
            da = _mat_mul(u, _mat_mul(_matrix_diag(dout[0]), _adjoint(v)))
            return (da,)

        a_shape = _shape(a)
        tensor_rank = P.Rank()(a)
        _check_dim(tensor_rank)
        m = a_shape[-2]
        n = a_shape[-1]
        s, u, v = out
        ds, du, dv = dout
        use_adjoint = False
        if m > n:
            use_adjoint = True
            m, n = n, m
            u, v = v, u
            du, dv = dv, du

        if full_matrices and abs(m - n) > 1:
            raise ValueError("For 'Svd' gradient, not support for abs(m - n) > 1 with full_matrices is True.")

        s_mat = _matrix_diag(s)
        s2 = square(s)

        f = matrix_set_diag(_safe_reciprocal(expand_dims(s2, -2) - expand_dims(s2, -1)), zeros_like(s), _k_0)
        s_inv_mat = _matrix_diag(_safe_reciprocal(s))

        v1 = v[..., :, :m]
        dv1 = dv[..., :, :m]

        u_gu = _mat_mul(_adjoint(u), du)
        v_gv = _mat_mul(_adjoint(v1), dv1)

        f_u = f * u_gu
        f_v = f * v_gv
        ds_mat = _matrix_diag(_cast(ds, _dtype(a)))
        term1_nouv = (ds_mat + _mat_mul(f_u + _adjoint(f_u), s_mat) + _mat_mul(s_mat, f_v + _adjoint(f_v)))

        term1 = _mat_mul(u, _mat_mul(term1_nouv, _adjoint(v1)))

        if m == n:
            da_before_transpose = term1
        else:
            gv1t = _matrix_transpose(dv1)
            gv1t_v1 = _mat_mul(gv1t, v1)
            term2_nous = gv1t - _mat_mul(gv1t_v1, _adjoint(v1))

            if full_matrices:
                v2 = v[..., :, m:n]
                d_v2 = dv[..., :, m:n]

                v1t_gv2 = _mat_mul(_adjoint(v1), d_v2)
                term2_nous -= _mat_mul(v1t_gv2, _adjoint(v2))

            u_s_inv = _mat_mul(u, s_inv_mat)
            term2 = _mat_mul(u_s_inv, term2_nous)

            da_before_transpose = term1 + term2

        if use_adjoint:
            da = _matrix_transpose(da_before_transpose)
        else:
            da = da_before_transpose

        return (da,)

    return bprop
