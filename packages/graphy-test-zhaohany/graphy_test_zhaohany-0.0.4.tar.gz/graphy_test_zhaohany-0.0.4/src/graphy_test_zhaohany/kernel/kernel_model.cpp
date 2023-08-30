#include <cassert>
#include <iostream>
#include <limits>

#include "kernel.h"

using std::cout;
using std::endl;

void _sddmme_model_csr(csr_t* snaph, array2d_t<float> & input_left, array2d_t<float> & input_right, array1d_t<float> & output, op_t op)
{
    //cout <<"sddmme" <<endl;
    int64_t num_node = input_left.row_count;
    vid_t v_count = input_left.col_count;

    op_scalar_fn op_fn;

    if (op == eDIV) {
        op_fn = div_scalar;
    } else if (op == eSUB) {
        op_fn = sub_scalar;
    } else if (op == eSUM) {
        op_fn = add_scalar;
    } else if (op == eMUL){
        op_fn = mul_scalar;
    } else {
        assert(0);
    }

    //Start of parallelism
    #pragma omp parallel for 
    for (vid_t v = 0; v < v_count; v++)
    {
        vid_t nebr_count = 0;
        vid_t sid, eid;
        vid_t* nebrs_reader;
        float* input_left_per_edge;
        float* input_right_per_edge;

        nebr_count = snaph->get_nebrs(v, nebrs_reader);
        for (vid_t i = 0; i < nebr_count; ++i) {
            sid = snaph->get_vid(nebrs_reader, i);
            eid = snaph->get_eid(nebrs_reader, i);

            for (int64_t h = 0; h < num_node; h++) {
                output[eid] += op_fn(input_right.get_item(h, sid), input_left.get_item(h, v));
            }
        }
    }
}

//This is on CSC
//dW = X^T x dY ==> dW^T = dY^T x X
//X is input left, dY is right
void _sddmme_model(csr_t* snaph, array2d_t<float> & input_left, array2d_t<float> & input_right, array1d_t<float> & output, op_t op)
{
    //cout <<"sddmme" <<endl;
    int64_t num_node = input_left.row_count;
    vid_t v_count = input_right.col_count;

    op_scalar_fn op_fn;

    if (op == eDIV) {
        op_fn = div_scalar;
    } else if (op == eSUB) {
        op_fn = sub_scalar;
    } else if (op == eSUM) {
        op_fn = add_scalar;
    } else if (op == eMUL){
        op_fn = mul_scalar;
    } else {
        assert(0);
    }

    //Start of parallelism
    #pragma omp parallel 
    {
    float* tmp_right = (float*)malloc(sizeof(float)*num_node);
    #pragma omp parallel for 
    for (vid_t v = 0; v < v_count; v++)
    {
        vid_t nebr_count = 0;
        vid_t sid, eid;
        vid_t* nebrs_reader;
        float* input_left_per_edge;
        float* input_right_per_edge;

        nebr_count = snaph->get_nebrs(v, nebrs_reader);
        if (nebr_count >= 2) {
            for (int h = 0; h < num_node; ++h) {
                tmp_right[h] = input_right.get_item(h,v);
            }
        }

        for (vid_t i = 0; i < nebr_count; ++i) {
            sid = snaph->get_vid(nebrs_reader, i);
            eid = snaph->get_eid(nebrs_reader, i);

            for (int64_t h = 0; h < num_node; h++) {
                //output[eid] += op_fn(input_right.get_item(h, v), input_left.get_item(h, sid));
                output[eid] += op_fn(tmp_right[h], input_left.get_item(h, sid));
            }
        }
    }
    free(tmp_right);
    }
}


void _sddmme_model_coo(const coo_t* snaph, array2d_t<float> & input_left, array2d_t<float> & input_right, array1d_t<float> & output, op_t op) 
{

    int64_t num_node = input_left.row_count;
    // vid_t v_count = input_left.col_count;
    
    op_scalar_fn op_fn;

    if (op == eDIV) {
        op_fn = div_scalar;
    } else if (op == eSUB) {
        op_fn = sub_scalar;
    } else if (op == eSUM) {
        op_fn = add_scalar;
    } else if (op == eMUL){
        op_fn = mul_scalar;
    } else {
        assert(0);
    }

    vid_t num_edge_count = snaph -> e_count;

    #pragma omp parallel for 
    for (vid_t eid = 0; eid < num_edge_count; eid++){
        vid_t src = snaph->edges[eid].src; //obj1->get_vid(nebrs, i);
        vid_t dst = snaph->edges[eid].dst;

        for (int64_t h = 0; h < num_node; h++) {
            output[eid] += op_fn(input_right.get_item(h, dst), input_left.get_item(h, src));
        }
    }
}

void _spmmw_model(csr_t* snaph, array2d_t<float> & input, array1d_t<float>& edge_weight, array1d_t<float>& bias_array,
             array2d_t<float> & output, op_t op, int64_t reverse)
{
    //forward: y -> x, backward, x-> y;

    vid_t v_count;
    int num_node = input.row_count;
    v_count = output.col_count;
   
    assert(op == eSUM);

    //Start of parallelism
    //#pragma omp parallel 
    #pragma omp parallel num_threads(4)
    {
        float* input_value;
        vid_t nebr_count = 0;
        vid_t sid;
        vid_t eid = 0;
        vid_t* nebrs_reader;
        float* message;
        float message_per_dim = 0;
        #pragma omp for collapse(2) nowait
        for (vid_t h = 0; h < num_node; h++) {
            //#pragma omp for nowait
            for (vid_t v = 0; v < v_count; v++) {
                message = output[h];
                input_value = input[h];
                nebr_count = snaph->get_nebrs(v, nebrs_reader);
                // if one node do not have any neighbor, we do not scatter it's message
                //edit here for self loop

                message_per_dim = 0;
                for (vid_t i = 0; i < nebr_count; ++i) {
                    sid = *nebrs_reader; ++nebrs_reader;
                    eid = *nebrs_reader; ++nebrs_reader;
                    //sid = snaph->get_vid(nebrs_reader, i);
                    //eid = snaph->get_eid(nebrs_reader, i);
                    //message_per_dim += input.get_item(h, sid) * edge_weight[eid];
                    message_per_dim += input_value[sid] * edge_weight[eid];
                }
                //message[v] = message_per_dim;
                message[v] = message_per_dim + bias_array[v];

            }
        }
    }
}

void _spmmw_model_without_bias(csr_t* snaph, array2d_t<float> & input, array1d_t<float>& edge_weight,
             array2d_t<float> & output, op_t op, int64_t reverse)
{
    //forward: y -> x, backward, x-> y;

    vid_t v_count;
    int num_node = input.row_count;
    v_count = output.col_count;
   
    assert(op == eSUM);

    //Start of parallelism
    //#pragma omp parallel 
    #pragma omp parallel num_threads(4)
    {
        float* input_value;
        vid_t nebr_count = 0;
        vid_t sid;
        vid_t eid = 0;
        vid_t* nebrs_reader;
        float* message;
        float message_per_dim = 0;
        #pragma omp for collapse(2) nowait
        for (vid_t h = 0; h < num_node; h++) {
            //#pragma omp for nowait
            for (vid_t v = 0; v < v_count; v++) {
                message = output[h];
                input_value = input[h];
                nebr_count = snaph->get_nebrs(v, nebrs_reader);
                // if one node do not have any neighbor, we do not scatter it's message
                //edit here for self loop

                message_per_dim = 0;
                for (vid_t i = 0; i < nebr_count; ++i) {
                    sid = *nebrs_reader; ++nebrs_reader;
                    eid = *nebrs_reader; ++nebrs_reader;
                    //sid = snaph->get_vid(nebrs_reader, i);
                    //eid = snaph->get_eid(nebrs_reader, i);
                    //message_per_dim += input.get_item(h, sid) * edge_weight[eid];
                    message_per_dim += input_value[sid] * edge_weight[eid];
                }
                //message[v] = message_per_dim;
                message[v] = message_per_dim;

            }
        }
    }
}

void invoke_spmmw_model_without_bias(graph_t& graph, array2d_t<float> & input_array, array1d_t<float>& edge_weight_array, 
                        array2d_t<float> & output_array, op_t op, int64_t reverse)
{
     if (graph.csr.flag == 0){
        if (reverse) {
            return _spmmw_model_without_bias(&graph.csr, input_array, edge_weight_array, output_array, (op_t)op, reverse);
        } else {
            return _spmmw_model_without_bias(&graph.csc, input_array, edge_weight_array, output_array, (op_t)op, reverse);
        }
     } else{
         // should not execute.
         if (reverse) {
             return _spmmw_snb(&graph.csr, input_array, edge_weight_array, output_array, (op_t)op, reverse);
         } else {
             return _spmmw_snb(&graph.csc, input_array, edge_weight_array, output_array, (op_t)op, reverse);
         }
     }
}

void invoke_spmmw_model(graph_t& graph, array2d_t<float> & input_array, array1d_t<float>& edge_weight_array,
                        array1d_t<float>& bias_array,
                        array2d_t<float> & output_array, op_t op, int64_t reverse)
{
     if (graph.csr.flag == 0){
        if (reverse) {
            return _spmmw_model(&graph.csr, input_array, edge_weight_array, bias_array, output_array, (op_t)op, reverse);
        } else {
            return _spmmw_model(&graph.csc, input_array, edge_weight_array, bias_array, output_array, (op_t)op, reverse);
        }
     } else{
         // should not execute.
         if (reverse) {
             return _spmmw_snb(&graph.csr, input_array, edge_weight_array, output_array, (op_t)op, reverse);
         } else {
             return _spmmw_snb(&graph.csc, input_array, edge_weight_array, output_array, (op_t)op, reverse);
         }
     }
}


void invoke_sddmme_model(graph_t& graph, array2d_t<float> & input_array_left, array2d_t<float> & input_array_right, 
                         array1d_t<float> & output_array, op_t op)
{
     if (graph.csr.flag == 0){
         //return _sddmme_model_csr(&graph.csr, input_array_left, input_array_right, output_array, (op_t)op);
         //return _sddmme_model(&graph.csc, input_array_left, input_array_right, output_array, (op_t)op);
         return _sddmme_model_coo(&graph.coo, input_array_left, input_array_right, output_array, (op_t)op);

     } else {//snb
         // should not execute
         return _sddmme_model(&graph.csr, input_array_left, input_array_right, output_array, (op_t)op);
         //return _sddmme_snb(&graph.csr, input_array_left, input_array_right, output_array, (op_t)op, 0);
     }
}

