import torch as th
import torch.utils.dlpack
import numpy as np
import ctypes as C
from ctypes.util import find_library
#import pygraph as gone

# importing enum for enumerations 
import enum

# creating enumerations using class 
class enumOP(enum.Enum): 
    eSUM = 0
    eMAX = 1
    eMIN = 2
    eSUB = 3 
    eMUL = 4
    eDIV = 5

#
# __all__ = ['gspmm', 'gsddmm', 'edge_softmax']
#


class GSpmv(th.autograd.Function):
    @staticmethod
    def forward(ctx, graph, X, norm, num_vcount, dim):
        feat = th.utils.dlpack.to_dlpack(X)

        # declare the output tensor here
        res = th.zeros(num_vcount, dim)
        # result = gone.array2d_t(re.data_ptr, num_vcount, dim)
        # result = res.numpy()
        result = th.utils.dlpack.to_dlpack(res)

        graph.spmm(feat, result, 0, norm)  # do not specify the reduce operation

        ctx.backward_cache = graph, norm, num_vcount, dim
        return res

    @staticmethod
    def backward(ctx, dZ):
        graph, norm, num_vcount, dim = ctx.backward_cache
        X = th.utils.dlpack.to_dlpack(dZ)
        # todo convert the dZ to 2d array
        # dt = np.dtype([('src', np.float32), ('dst', np.float32)])
        res = th.zeros(num_vcount, dim)
        # result = res.numpy() #np.zeros((num_vcount, dim), dtype = np.float32)
        result = th.utils.dlpack.to_dlpack(res)

        graph.spmm(X, result, 1, norm)
        return None, res, None, None, None


class EdgeSoftmax(th.autograd.Function):
    @staticmethod
    def forward(ctx, graph, efficient_score, num_vcount, dim):

        feat = th.utils.dlpack.to_dlpack(efficient_score)
        score_max = th.zeros(num_vcount, dim)
        result = th.utils.dlpack.to_dlpack(score_max)
        # todo find max edge value
        # for score_max
        graph.spmmw(feat, result, enumOP.eMAX.value, 0)
        # sub from score_max
        score_max = th.utils.dlpack.to_dlpack(score_max)
        score = th.zeros(num_vcount, dim)
        result = th.utils.dlpack.to_dlpack(score)
        # todo find score - score_max
        # for score
        graph.sddmm(score_max, feat, result, enumOP.eSUB.value, 0)
        # apply expo for score
        score = th.exp(score)
        score = th.utils.dlpack.to_dlpack(score)
        score_sum = th.zeros(num_vcount, dim)
        result = th.utils.dlpack.to_dlpack(score_sum)
        # todo score_sum
        graph.spmmw(score, result, enumOP.eSUM.value, 0)
        score_sum = th.utils.dlpack.to_dlpack(score_sum)
        out = th.zeros(num_vcount, dim)
        result = th.utils.dlpack.to_dlpack(out)
        # todo score % score_sum.out is | E |
        graph.sddmm(score_sum, score, result, enumOP.eDIV.value, 0)
        ctx.backward_cache = graph, num_vcount, dim, out
        return out

    @staticmethod
    def backward(ctx, dZ):
        graph, num_vcount, dim, out = ctx.backward_cache
        sds = out * dZ

        fea = th.utils.dlpack.to_dlpack(sds)
        accum = th.zeros(num_vcount, dim)
        result = th.utils.dlpack.to_dlpack(accum)
        # for accum
        graph.spmmw(fea, result, enumOP.eSUM.value, 0)
        accum = th.utils.dlpack.to_dlpack(accum)
        out = th.utils.dlpack.to_dlpack(out)
        temp = th.zeros(num_vcount, dim)
        result = th.utils.dlpack.to_dlpack(temp)
        temp = graph.sddmm(accum, out, result, enumOP.eMUL.value, 0)
        grad_score = sds - temp

        return None, grad_score, None, None

class EdgeSoftmax_heads(th.autograd.Function):
    @staticmethod
    def forward(ctx, graph, efficient_score, num_vcount, dim):
        heads = efficient_score.size(1)
        feat = th.utils.dlpack.to_dlpack(efficient_score)
        score_max = th.zeros(num_vcount, heads)
        result = th.utils.dlpack.to_dlpack(score_max)
        # todo find max edge value
        # for score_max
        graph.spmmw2d(feat, result, enumOP.eMAX.value, 0)
        # sub from score_max
        score_max = th.utils.dlpack.to_dlpack(score_max)
        score = th.zeros(num_vcount, heads)
        result = th.utils.dlpack.to_dlpack(score)
        # todo find score - score_max
        # for score
        graph.sddmm2d(score_max, feat, result, enumOP.eSUB.value, 0)
        # apply expo for score
        score = th.exp(score)
        score = th.utils.dlpack.to_dlpack(score)
        score_sum = th.zeros(num_vcount, heads)
        result = th.utils.dlpack.to_dlpack(score_sum)
        # todo score_sum
        graph.spmmw(score, result, enumOP.eSUM.value, 0)
        score_sum = th.utils.dlpack.to_dlpack(score_sum)
        out = th.zeros(num_vcount, heads)
        result = th.utils.dlpack.to_dlpack(out)
        # todo score % score_sum.out is | E |
        graph.sddmm2d(score_sum, score, result, enumOP.eDIV.value, 0)
        ## above 2d is the reason why it can work now
        ctx.backward_cache = graph, num_vcount, dim, out, heads
        return out

    @staticmethod
    def backward(ctx, dZ):
        graph, num_vcount, dim, out, heads = ctx.backward_cache
        sds = out * dZ

        fea = th.utils.dlpack.to_dlpack(sds)
        accum = th.zeros(num_vcount, heads)
        result = th.utils.dlpack.to_dlpack(accum)
        # for accum
        graph.spmmw(fea, result, enumOP.eSUM.value, 0)
        accum = th.utils.dlpack.to_dlpack(accum)
        out = th.utils.dlpack.to_dlpack(out)
        temp = th.zeros(num_vcount, heads)
        result = th.utils.dlpack.to_dlpack(temp)
        temp = graph.sddmm(accum, out, result, enumOP.eMUL.value, 0)
        grad_score = sds - temp

        return None, grad_score, None, None



class GSpmv_op(th.autograd.Function):
    @staticmethod
    def forward(ctx, X, graph, edge_score_by_softmax, num_vcount, dim):
        # input is for each edge, edge_score_by_softmax is also refer to each edge
        feat_X = th.utils.dlpack.to_dlpack(X)
        feat_edge_score_by_softmax = th.utils.dlpack.to_dlpack(edge_score_by_softmax)
        rst = th.zeros(num_vcount, dim)
        result = th.utils.dlpack.to_dlpack(rst)
        graph.spmmw_op(feat_X, feat_edge_score_by_softmax, result, enumOP.eSUM.value, 0)
        ctx.backward_cache = graph, edge_score_by_softmax, num_vcount, dim
        return rst


    @staticmethod
    def backward(ctx, dZ):
        graph, edge_score_by_softmax, num_vcount, dim = ctx.backward_cache
        reverse = 1
        feat_X = th.utils.dlpack.to_dlpack(dZ)
        feat_edge_score_by_softmax = th.utils.dlpack.to_dlpack(edge_score_by_softmax)
        res = th.zeros(num_vcount, dim)
        result = th.utils.dlpack.to_dlpack(res)
        graph.spmmw_op(feat_X, feat_edge_score_by_softmax, result, enumOP.eSUM.value, reverse)
        return res, None, None, None, None

class GSpmv_op_heads(th.autograd.Function):
    @staticmethod
    def forward(ctx, X, graph, edge_score_by_softmax, num_vcount, dim):
        # input is for each edge, edge_score_by_softmax is also refer to each edge
        heads = edge_score_by_softmax.size(1)
        feat_X = th.utils.dlpack.to_dlpack(X)
        feat_edge_score_by_softmax = th.utils.dlpack.to_dlpack(edge_score_by_softmax)
        rst = th.zeros(num_vcount, heads, dim)
        result = th.utils.dlpack.to_dlpack(rst)
        graph.spmmw_op2d(feat_X, feat_edge_score_by_softmax, result, enumOP.eSUM.value, 0)
        ctx.backward_cache = graph, edge_score_by_softmax, num_vcount, dim, heads
        return rst


    @staticmethod
    def backward(ctx, dZ):
        graph, edge_score_by_softmax, num_vcount, dim, heads = ctx.backward_cache
        reverse = 1
        feat_X = th.utils.dlpack.to_dlpack(dZ)
        feat_edge_score_by_softmax = th.utils.dlpack.to_dlpack(edge_score_by_softmax)
        res = th.zeros(num_vcount, heads, dim)
        result = th.utils.dlpack.to_dlpack(res)
        graph.spmmw_op2d(feat_X, feat_edge_score_by_softmax, result, enumOP.eSUM.value, reverse)
        return res, None, None, None, None



# the gspmv has only 1 input, and then apply different operations such as sum, max on it
def run_gspmm(graph, X, norm, num_vcount, dim):
    return GSpmv.apply(graph, X, norm, num_vcount, dim)


# the gspmv_op has 2 inputs, one is edge_score, another one is edge_softmax score
def run_gspmv_op(graph, X, edge_score_by_softmax, num_vcount, dim):
    return GSpmv_op.apply(X, graph, edge_score_by_softmax, num_vcount, dim)


def run_gspmv_op_heads(graph, X, edge_score_by_softmax, num_vcount, dim):
    return GSpmv_op_heads.apply(X, graph, edge_score_by_softmax, num_vcount, dim)

def apply_edge(graph, el, er):
    dim = el.size(1)
    feat_el = th.utils.dlpack.to_dlpack(el)
    feat_er = th.utils.dlpack.to_dlpack(er)
    edge_count = graph.get_edge_count()
    res = th.zeros(edge_count, dim)
    result = th.utils.dlpack.to_dlpack(res)
    graph.apply_edges_op2d(feat_el, feat_er, result)
    return res


def apply_edge_heads(graph, el, er):
    heads = el.size(1)
    feat_el = th.utils.dlpack.to_dlpack(el)
    feat_er = th.utils.dlpack.to_dlpack(er)
    edge_count = graph.get_edge_count()
    res = th.zeros(edge_count, heads)
    result = th.utils.dlpack.to_dlpack(res)
    graph.apply_edges_op2d(feat_el, feat_er, result)
    return res


def edge_softmax(graph, efficient_score, num_vcount, dim):
    result = EdgeSoftmax.apply(graph, efficient_score, num_vcount, dim)
    return result

def edge_softmax_heads(graph, efficient_score, num_vcount, dim):
    result = EdgeSoftmax_heads.apply(graph, efficient_score, num_vcount, dim)
    return result
