# Copyright 2023 Huawei Technologies Co., Ltd
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

"""grad_sequence_ops"""

from mindspore.ops.operations import _sequence_ops as seq
from mindspore.ops import operations as P
from mindspore.ops import functional as F
from mindspore.ops.composite.multitype_ops.zeros_like_impl import zeros_like
from mindspore.ops._grad_experimental.grad_base import bprop_getters
from mindspore.ops.primitive import Primitive


tuple_setitem = Primitive("tuple_setitem")
list_setitem = Primitive("list_setitem")


@bprop_getters.register(seq.SequenceCount)
def get_bprop_count(self):
    """Generate bprop for SequenceCount"""

    def bprop(x, y, out, dout):
        return (zeros_like(x), zeros_like(y))

    return bprop


@bprop_getters.register(seq.sequence_len)
def get_bprop_sequence_len(self):
    """Generate bprop for sequence_len"""
    def bprop(x, out, dout):
        return (zeros_like(x),)

    return bprop


@bprop_getters.register(seq.SequenceAdd)
def get_bprop_sequence_add(self):
    """Generate bprop for SequenceAdd"""
    def bprop(x, y, out, dout):
        out_offset = seq.SequenceAddOffset()(x, y)
        dx = seq.SequenceSlice()(dout, out_offset[0], len(x), 1)
        dy = seq.SequenceSlice()(dout, out_offset[1], len(x) + len(y), 1)

        return (dx, dy)

    return bprop


@bprop_getters.register(seq.SequenceUnstack)
def get_bprop_sequence_unstack(self):
    """Generate bprop for SequenceUnstack"""
    axis = self.axis

    def bprop(x, out, dout):
        seq_unstack_grad = seq.SequenceStack(axis)
        out = seq_unstack_grad(dout)
        return (out,)

    return bprop


@bprop_getters.register(seq.SequenceSlice)
def get_bprop_slice(self):
    """Generate bprop for SequenceSlice"""

    def bprop(x, start, stop, step, out, dout):
        dx = seq.SequenceSliceGrad()(dout, x, start, stop, step)
        res = (dx, zeros_like(start), zeros_like(stop), zeros_like(step))
        return res

    return bprop


@bprop_getters.register(seq.SequenceIndex)
def get_bprop_index(self):
    """Generate bprop for SequenceIndex"""

    def bprop(x, y, start, end, out, dout):
        res = (zeros_like(x), zeros_like(y), zeros_like(start), zeros_like(end))
        return res

    return bprop


@bprop_getters.register(seq.InSequence)
def get_bprop_insequence(self):
    """Generate bprop for InSequence"""

    def bprop(x, y, out, dout):
        return (zeros_like(x), seq.SequenceZerosLike()(y))

    return bprop


@bprop_getters.register("tuple_equal")
@bprop_getters.register("list_equal")
def get_bprop_seq_equal(self):
    """Generate bprop for tuple_equal and list_equal"""

    def bprop(x, y, out, dout):
        return (zeros_like(x), zeros_like(y))

    return bprop


@bprop_getters.register("shape_mul")
def get_bprop_shape_mul(self):
    """Generate bprop for tuple_equal and list_equal"""

    def bprop(x, out, dout):
        dx = seq.ShapeMulGrad()(x, dout)
        return (dx,)

    return bprop


@bprop_getters.register("tuple_setitem")
def get_bprop_tuple_setitem(self):
    """Generate bprop for TupleSetItem and ListSetItem"""

    def bprop(x, idx, value, out, dout):
        d_x = tuple_setitem(dout, idx, zeros_like(value))
        d_value = dout[idx]
        d_idx = 0
        return (d_x, zeros_like(d_idx), d_value)

    return bprop


@bprop_getters.register("list_setitem")
def get_bprop_list_setitem(self):
    """Generate bprop for TupleSetItem and ListSetItem"""

    def bprop(x, idx, value, out, dout):
        d_x = list_setitem(dout, idx, zeros_like(value))
        d_value = dout[idx]
        d_idx = 0
        return (d_x, zeros_like(d_idx), d_value)

    return bprop


@bprop_getters.register("ListInplaceReverse")
def get_bprop_list_inplace_reverse(self):
    """Generate bprop for list inplace reverse"""

    def bprop(x, out, dout):
        return (zeros_like(x),)

    return bprop


@bprop_getters.register("ListInplaceExtend")
def get_bprop_list_inplace_extend(self):
    """Generate bprop for list inplace extend"""

    def bprop(x, y, out, dout):
        return (zeros_like(x), zeros_like(y))

    return bprop


@bprop_getters.register("ListInplaceInsert")
def get_bprop_list_inplace_insert(self):
    """Generate bprop for list inplace insert"""

    def bprop(x, index, target, out, dout):
        return (zeros_like(x), zeros_like(index), zeros_like(target))

    return bprop


@bprop_getters.register("ListInplacePop")
def get_bprop_list_inplace_pop(self):
    """Generate bprop for list inplace pop"""

    def bprop(x, index, out, dout):
        return (zeros_like(x), zeros_like(index))

    return bprop


@bprop_getters.register(seq.ListAppend)
def get_bprop_list_append(self):
    """Generate bprop for ListAppend"""

    def bprop(x, value, out, dout):
        d_x = seq.ListAppendAndInsertGrad()(dout, -1)
        return (d_x, zeros_like(value))

    return bprop


@bprop_getters.register(seq.ListInsert)
def get_bprop_list_insert(self):
    """Generate bprop for ListInsert"""

    def bprop(x, idx, value, out, dout):
        d_x = seq.ListAppendAndInsertGrad()(dout, idx)
        return (d_x, zeros_like(idx), zeros_like(value))

    return bprop


@bprop_getters.register(seq.TupleToTensor)
def get_bprop_tuple_to_tensor(self):
    """Generate bprop for TupleToTensor"""

    def bprop(x, dtype, out, dout):
        tuple_type = F.typeof(x)
        dout = P.Cast()(dout, tuple_type)
        d_x = seq.TensorToTuple()(dout)
        return (d_x, zeros_like(dtype))

    return bprop


@bprop_getters.register(seq.ListToTensor)
def get_bprop_list_to_tensor(self):
    """Generate bprop for ListToTensor"""

    def bprop(x, dtype, out, dout):
        tuple_type = F.typeof(x)
        dout = P.Cast()(dout, tuple_type)
        d_x = seq.TensorToList()(dout)
        return (d_x, zeros_like(dtype))

    return bprop


@bprop_getters.register(P.ScalarToTensor)
def get_bprop_scalar_to_tensor(self):
    """Generate bprop for ScalarToTensor"""

    def bprop(x, dtype, out, dout):
        scalar_type = F.typeof(x)
        dout = P.Cast()(dout, scalar_type)
        d_x = seq.TensorToScalar()(dout)
        return (d_x, zeros_like(dtype))

    return bprop


@bprop_getters.register(seq.TensorToTuple)
def get_bprop_tensor_to_tuple(self):
    """Generate bprop for TensorToTuple"""

    def bprop(x, out, dout):
        dtype = F.typeof(x)
        d_x = seq.TupleToTensor()(dout, dtype)
        return (d_x,)

    return bprop


@bprop_getters.register(seq.TensorToList)
def get_bprop_tensor_to_list(self):
    """Generate bprop for TensorToList"""

    def bprop(x, out, dout):
        dtype = F.typeof(x)
        d_x = seq.ListToTensor()(dout, dtype)
        return (d_x,)

    return bprop


@bprop_getters.register(seq.TensorToScalar)
def get_bprop_tensor_to_scalar(self):
    """Generate bprop for TensorToScalar"""

    def bprop(x, out, dout):
        dtype = F.typeof(x)
        d_x = P.ScalarToTensor()(dout, dtype)
        return (d_x,)

    return bprop


@bprop_getters.register("tuple_le")
@bprop_getters.register("tuple_lt")
@bprop_getters.register("list_le")
@bprop_getters.register("list_lt")
def get_bprop_less(self):
    """Generate bprop for SequenceLessThan and SequenceLessEqual"""

    def bprop(x, y, out, dout):
        return (zeros_like(x), zeros_like(y))

    return bprop


@bprop_getters.register(seq.SequenceMul)
def get_bprop_mul(self):
    """Generate bprop for SequenceMul"""

    def bprop(x, y, out, dout):
        dx = x
        if isinstance(x, tuple):
            for i in range(len(x)):
                dx = tuple_setitem(dx, i, dout[i])
        else:
            for i in range(len(x)):
                dx = list_setitem(dx, i, dout[i])
        return (dx, zeros_like(y))

    return bprop


@bprop_getters.register(seq.SequenceMin)
@bprop_getters.register(seq.SequenceMax)
def get_bprop_max_min(self):
    """Generate bprop for SequenceMax and SequenceMax"""

    def bprop(x, out, dout):
        index = x.index(out)
        if isinstance(x, tuple):
            dx = tuple_setitem(zeros_like(x), index, dout)
        else:
            dx = list_setitem(zeros_like(x), index, dout)
        return (dx,)

    return bprop


@bprop_getters.register("tuple_greater_than")
@bprop_getters.register("list_greater_than")
@bprop_getters.register("tuple_greater_equal")
@bprop_getters.register("list_greater_equal")
def get_bprop_greater(self):
    """Generate bprop for tuple_greater_than, list_greater_than,
    tuple_greater_equal, list_greater_equal.
    """

    def bprop(x, y, out, dout):
        return (zeros_like(x), zeros_like(y))

    return bprop
