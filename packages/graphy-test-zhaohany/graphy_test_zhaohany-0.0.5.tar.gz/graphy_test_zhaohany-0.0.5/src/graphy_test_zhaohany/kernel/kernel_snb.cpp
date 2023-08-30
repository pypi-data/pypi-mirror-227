#include <cassert>
#include <iostream>
#include <limits>
#include <omp.h>
#include <algorithm>
#include <list>

#include "kernel.h"
#include "csr.h"

void _spmm_snb(csr_t* snaph, array2d_t<float> & input, array2d_t<float> & output, op_t op,
                    bool reverse, bool norm /*= true*/)
{
    
    vid_t v_count = snaph->v_count;
    int output_dim = input.col_count;
    vid_t num_vertex = snaph->get_vcount();
    vid_t each_degree;

    //cout << "spmm " << op << "reverse = " << reverse << endl;

    //If in backward, normalize it first
    if (reverse == 1 && norm == true) {
        //#pragma omp parallel for 
        for (vid_t v = 0; v < num_vertex; v++) { 
            each_degree = snaph->degrees[v];
            if (each_degree > 1) {
                input.row_normalize(v, each_degree); 
            }
        }
    }


    vid_t nebr_count = 0;
    vid_t* header; 
    vid_t index = 0, m, n, offset;
    snb_t snb;
    vid_t dst1;
    vid_t src1;
    vid_t p = (snaph->v_count >> bit_shift1) + (0 != (snaph->get_vcount() & part_mask1_2));
    for (vid_t i = 0; i < p; ++i) {
        for (vid_t j = 0; j < p; ++j) {
            offset = ((i*p + j) << bit_shift2); 
            for (vid_t s_i = 0; s_i < p_p; s_i++) {
                // #pragma omp parallel for 
                for (vid_t s_j = 0; s_j < p_p; s_j++) {

                    index = offset + ((s_i << bit_shift3) + s_j);
                    m = ((i << bit_shift3) + s_i) << bit_shift2;
                    n = ((j << bit_shift3) + s_j) << bit_shift2; 
                    
                    nebr_count = snaph->get_nebrs(index, header);
                    if (0 == nebr_count) continue;
                    
                    array1d_t<float> message(output_dim);//zero initialized
                    for (vid_t e = 0; e < nebr_count; ++e) {
                        message.reset();
                        // dst = csr.next(header);
                        snb = snaph->get_snb(header, e);
                        if (reverse ==1) {
                            dst1 = snb.src + m;
                            src1 = snb.dst + n;
                        }else {
                            dst1 = snb.dst + n;
                            src1 = snb.src + m;
                        }

                        // update the feature
                        message.add(input[dst1]);
                        output.row_add(message.data_ptr, src1);
                    }
                }
            }
        }
    }
    
    //If in forward, normalize it now.
    for (vid_t v = 0; v < num_vertex; v++) { 
        each_degree = snaph->degrees[v];
        if (each_degree > 1 && reverse == 0 && norm == true) {
            output.row_normalize(v, each_degree); 
        }
    }
}



void _spmmw_snb(csr_t* snaph, array2d_t<float> & input, array1d_t<float>& edge_weight,
             array2d_t<float> & output, op_t op, int64_t reverse)
{
    //cout << "spmm_op is " << op << "reverse="<< reverse << endl;
    vid_t v_count = snaph->get_vcount();
    int output_dim = input.col_count;

    assert(op == eSUM);
    vid_t nebr_count = 0;
    vid_t eid = 0;
    vid_t base_eid = 0;
    vid_t* header; 
    vid_t index = 0, m, n, offset;
    snb_t snb;
    float* message;
    float* input_value;
    vid_t dst1;
    vid_t src1;
    vid_t p = (snaph->v_count >> bit_shift1) + (0 != (snaph->get_vcount() & part_mask1_2));
    for (vid_t i = 0; i < p; ++i) {
        for (vid_t j = 0; j < p; ++j) {
            offset = ((i*p + j) << bit_shift2); 
            for (vid_t s_i = 0; s_i < p_p; s_i++) {
                // #pragma omp parallel for 
                for (vid_t s_j = 0; s_j < p_p; s_j++) {

                    index = offset + ((s_i << bit_shift3) + s_j);
                    m = ((i << bit_shift3) + s_i) << bit_shift2;
                    n = ((j << bit_shift3) + s_j) << bit_shift2; 
                    
                    nebr_count = snaph->get_nebrs(index, header);
                    if (0 == nebr_count) continue;
                    
                    base_eid = snaph->get_first_eid(index);
                    for (vid_t e = 0; e < nebr_count; ++e) {
                        // dst = csr.next(header);
                        snb = snaph->get_snb(header, e);
                        eid = base_eid + e;
                        
                        if (reverse ==1) {
                            dst1 = snb.src + m;
                            src1 = snb.dst + n;
                        }else {
                            dst1 = snb.dst + n;
                            src1 = snb.src + m;
                        }

                        // update the feature
                        // message.add(input[dst1]);
                        // output.row_add(message.data_ptr, src1);
                        message = output[dst1];
                        //message = output[src1];
                        //input_value = input[dst1];
                        input_value = input[src1];
                        for (vid_t h = 0; h < output_dim; ++h) {
                            message[h] += input_value[h]*edge_weight[eid];
                         }
                    }
                }
            }
        }
    }
}




void _spmmw_snb(csr_t* snaph, array1d_t<float>& edge_weight,
             array1d_t<float> & output, op_t op, int64_t reverse)
{


    vid_t v_count = snaph->get_vcount();
    op_scalar_fn op_fn;
    
    if (op == eMIN) {
        op_fn = min_scalar;
    } else if (op == eSUM) {
        op_fn = add_scalar; 
    } else if (op == eMAX){
        op_fn = max_scalar; 
    } else {
        assert(0);
    }

    vid_t nebr_count = 0;
    vid_t eid = 0;
    vid_t base_eid = 0;
    vid_t* header; 
    vid_t index = 0, m, n, offset;
    snb_t snb;
    vid_t dst1;
    vid_t src1;
    vid_t p = (snaph->v_count >> bit_shift1) + (0 != (snaph->get_vcount() & part_mask1_2));
    //initilize the message arrary
    array1d_t<float> message(v_count);
    if (op == eMAX){
        for (vid_t k = 0; k < v_count; ++k){
            message[k] = -std::numeric_limits<float>::infinity();

        }
    }
    if  (op == eMIN){
        for (vid_t m = 0; m < v_count; ++m){
                    message[m] = std::numeric_limits<float>::infinity();

                }

    }


    for (vid_t i = 0; i < p; ++i) {
        for (vid_t j = 0; j < p; ++j) {
            offset = ((i*p + j) << bit_shift2); 
            for (vid_t s_i = 0; s_i < p_p; s_i++) {
                // #pragma omp parallel for 
                for (vid_t s_j = 0; s_j < p_p; s_j++) {

                    index = offset + ((s_i << bit_shift3) + s_j);
                    m = ((i << bit_shift3) + s_i) << bit_shift2;
                    n = ((j << bit_shift3) + s_j) << bit_shift2; 
                    
                    nebr_count = snaph->get_nebrs(index, header);
                    if (0 == nebr_count) continue;
                    
                    base_eid = snaph->get_first_eid(index);
                    for (vid_t e = 0; e < nebr_count; ++e) {
                        // dst = csr.next(header);
                        snb = snaph->get_snb(header, e);
                        eid = base_eid + e;
                        
                        if (reverse ==1) {
                            dst1 = snb.src + m;
                            src1 = snb.dst + n;
                        }else {
                            dst1 = snb.dst + n;
                            src1 = snb.src + m;
                        }

                        // update the feature
                        message[dst1] = op_fn(message[dst1], edge_weight[eid]);
                        
                    }
                }
            }
        }
    }
    // update the results after we loop all edges
    for (vid_t h = 0; h < v_count; ++h) {
        output[h] = message[h];
    }

}


void _sddmm_snb(csr_t* snaph, 
        array1d_t<float> & input_left, array1d_t<float> & input_right,
        array1d_t<float> & output, op_t op, int64_t reverse)
{

    vid_t v_count = snaph->get_vcount();
    
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


    vid_t p = (snaph->v_count >> bit_shift1) + (0 != (snaph->get_vcount() & part_mask1_2));
    #pragma omp parallel 
    {
    vid_t nebr_count = 0;
    vid_t eid = 0;
    vid_t base_eid = 0;
    vid_t* header; 
    vid_t index = 0, m, n, offset;
    snb_t snb;
    vid_t dst1;
    vid_t src1;
    for (vid_t i = 0; i < p; ++i) {
        for (vid_t j = 0; j < p; ++j) {
            offset = ((i*p + j) << bit_shift2); 
            for (vid_t s_i = 0; s_i < p_p; s_i++) {
                
                for (vid_t s_j = 0; s_j < p_p; s_j++) {

                    index = offset + ((s_i << bit_shift3) + s_j);
                    m = ((i << bit_shift3) + s_i) << bit_shift2;
                    n = ((j << bit_shift3) + s_j) << bit_shift2; 
                    
                    nebr_count = snaph->get_nebrs(index, header);
                    if (0 == nebr_count) continue;
                    
                    base_eid = snaph->get_first_eid(index);
                    #pragma omp for nowait
                    for (vid_t e = 0; e < nebr_count; ++e) {
                        snb = snaph->get_snb(header, e);
                        eid = base_eid + e;
                        if (reverse ==1) {
                            dst1 = snb.src + m;
                            src1 = snb.dst + n;
                        }else {
                            dst1 = snb.dst + n;
                            src1 = snb.src + m;
                        }

                        // update the feature
                        output[eid] = op_fn(input_right[eid], input_left[dst1]);

                    }
                }
            }
        }
    }
    }
}


void _sddmme_snb(csr_t* snaph, 
        array2d_t<float> & input_left, array2d_t<float> & input_right,
        array1d_t<float> & output, op_t op, int64_t reverse)
{

    int output_dim = input_left.col_count;
    vid_t v_count = snaph->get_vcount();
    
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

    vid_t p = (snaph->v_count >> bit_shift1) + (0 != (snaph->get_vcount() & part_mask1_2));
    #pragma omp parallel 
    {
    vid_t nebr_count = 0;
    vid_t* header; 
    vid_t index = 0, m, n, offset;
    float* input_left_per_edge;
    float* input_right_per_edge;
    vid_t base_eid = 0;
    vid_t eid = 0;
    snb_t snb;
    vid_t dst1;
    vid_t src1;
    for (vid_t i = 0; i < p; ++i) {
        for (vid_t j = 0; j < p; ++j) {
            offset = ((i*p + j) << bit_shift2); 
            for (vid_t s_i = 0; s_i < p_p; s_i++) {
                for (vid_t s_j = 0; s_j < p_p; s_j++) {

                    index = offset + ((s_i << bit_shift3) + s_j);
                    m = ((i << bit_shift3) + s_i) << bit_shift2;
                    n = ((j << bit_shift3) + s_j) << bit_shift2; 
                    
                    nebr_count = snaph->get_nebrs(index, header);
                    if (0 == nebr_count) continue;
                    base_eid = snaph->get_first_eid(index);
                    #pragma omp for nowait
                    for (vid_t e = 0; e < nebr_count; ++e) {
                        eid = e + base_eid;
                        snb = snaph->get_snb(header, e);
                        
                        if (reverse ==1) {
                            dst1 = snb.src + m;
                            src1 = snb.dst + n;
                        }else {
                            dst1 = snb.dst + n;
                            src1 = snb.src + m;
                        }

                        // update the feature
                        input_left_per_edge = input_left[src1];
                        input_right_per_edge = input_right[dst1];
                        for (int64_t h = 0; h < output_dim; h++) {
                                output[eid] += op_fn(input_right_per_edge[h], input_left_per_edge[h]);
                        }
                    }
                }
            }
        }
    }
    }

}



void _sddmme2d_snb(csr_t* snaph, 
        array3d_t<float> & input_left, array3d_t<float> & input_right,
        array2d_t<float> & output, op_t op, int64_t reverse)
{

    int heads = input_left.row_count;
    int output_dim = input_left.col_count;

    vid_t v_count = snaph->get_vcount();
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


    vid_t nebr_count = 0;
    vid_t* header; 
    vid_t index = 0, m, n, offset;
    snb_t snb;
    vid_t dst1;
    vid_t src1;
    float* input_left_per_edge_per_head; 
    float* input_right_per_edge_per_head; 
    float* message_per_edge;
    vid_t eid = 0;
    vid_t base_eid = 0;
    vid_t p = (snaph->v_count >> bit_shift1) + (0 != (snaph->get_vcount() & part_mask1_2));
    for (vid_t i = 0; i < p; ++i) {
        for (vid_t j = 0; j < p; ++j) {
            offset = ((i*p + j) << bit_shift2); 
            for (vid_t s_i = 0; s_i < p_p; s_i++) {
                // #pragma omp parallel for 
                for (vid_t s_j = 0; s_j < p_p; s_j++) {

                    index = offset + ((s_i << bit_shift3) + s_j);
                    m = ((i << bit_shift3) + s_i) << bit_shift2;
                    n = ((j << bit_shift3) + s_j) << bit_shift2; 
                    
                    nebr_count = snaph->get_nebrs(index, header);
                    if (0 == nebr_count) continue;
                    base_eid = snaph->get_first_eid(index);
                    for (vid_t e = 0; e < nebr_count; ++e) {
                        eid = e + base_eid;
                        snb = snaph->get_snb(header, e);
                        if (reverse ==1) {
                            dst1 = snb.src + m;
                            src1 = snb.dst + n;
                        }else {
                            dst1 = snb.dst + n;
                            src1 = snb.src + m;
                        }

                        // update the feature
                        message_per_edge = output[eid];
                
                        for (int64_t z = 0; z < heads; z++){
                            input_left_per_edge_per_head = input_left.get_row_ptr(dst1, z);
                            input_right_per_edge_per_head = input_right.get_row_ptr(src1,z);

                            for (int64_t h = 0; h < output_dim; h++){
                            message_per_edge[z] += op_fn(input_right_per_edge_per_head[h], input_left_per_edge_per_head[h]);
                            }

                        }

                        
                    }
                }
            }
        }
    }

}


void _spmmw2d_snb(csr_t* snaph, array2d_t<float>& edge_weight,
             array2d_t<float> & output, op_t op, int64_t reverse)
{

    vid_t v_count = snaph->get_vcount();
    int output_dim = edge_weight.col_count;
    float* message_per_node;
    op_scalar_fn op_fn;
    float* message;
    
    if (op == eMIN) {
        op_fn = min_scalar;
    } else if (op == eSUM) {
        op_fn = add_scalar; 
    } else if (op == eMAX){
        op_fn = max_scalar; 
    } else {
        assert(0);
    }


    for (vid_t k = 0; k < v_count; ++k){
        message = output[k];
        for (int64_t h = 0; h < output_dim; h++){
            if (op == eMAX){
                message[h] = -std::numeric_limits<float>::infinity();

            }else if (op == eMIN) {
                message[h] = std::numeric_limits<float>::infinity();
            }

        }
    }

    //cout << "init" << endl;
    //loop for every edge
    vid_t nebr_count = 0;
    vid_t* header; 
    vid_t index = 0, m, n, offset;
    snb_t snb;
    vid_t dst1;
    float* edge_weight_per_edge;
    vid_t eid = 0;
    vid_t src1;
    vid_t base_eid = 0;
    vid_t p = (snaph->v_count >> bit_shift1) + (0 != (snaph->get_vcount() & part_mask1_2));
    for (vid_t i = 0; i < p; ++i) {
        for (vid_t j = 0; j < p; ++j) {
            offset = ((i*p + j) << bit_shift2); 
            for (vid_t s_i = 0; s_i < p_p; s_i++) {
                // #pragma omp parallel for 
                for (vid_t s_j = 0; s_j < p_p; s_j++) {

                    index = offset + ((s_i << bit_shift3) + s_j);
                    m = ((i << bit_shift3) + s_i) << bit_shift2;
                    n = ((j << bit_shift3) + s_j) << bit_shift2; 
                    
                    nebr_count = snaph->get_nebrs(index, header);
                    if (0 == nebr_count) continue;
                    base_eid = snaph->get_first_eid(index);
                    for (vid_t e = 0; e < nebr_count; ++e) {
                        eid = e + base_eid;
                        snb = snaph->get_snb(header, e);
                        if (reverse ==1) {
                            dst1 = snb.src + m;
                            src1 = snb.dst + n;
                        }else {
                            dst1 = snb.dst + n;
                            src1 = snb.src + m;
                        }

                        // update the feature
                        //cout << "init1" << endl;
                        edge_weight_per_edge = edge_weight[eid];// edge_weight is 2d tensor
                        //cout << "init2" << endl;
                        message = output[src1];
                        for (int64_t s_h = 0; s_h < output_dim; s_h++){
                            //cout << "init4" << endl;
                            message[s_h] = op_fn(message[s_h], edge_weight_per_edge[s_h]);
                            //cout << "init5" << endl;

                        }
                    }
                }
            }
        }
    }
}



void _sddmm2d_snb(csr_t* snaph, 
        array2d_t<float> & input_left, array2d_t<float> & input_right,
        array2d_t<float> & output, op_t op, int64_t reverse)
{
    int output_dim = input_left.col_count;
    vid_t v_count = snaph->get_vcount();

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


    vid_t nebr_count = 0;
    vid_t* header; 
    vid_t index = 0, m, n, offset;
    snb_t snb;
    vid_t dst1;
    vid_t eid = 0;
    vid_t src1;
    vid_t base_eid = 0;
    vid_t p = (snaph->v_count >> bit_shift1) + (0 != (snaph->get_vcount() & part_mask1_2));
    for (vid_t i = 0; i < p; ++i) {
        for (vid_t j = 0; j < p; ++j) {
            offset = ((i*p + j) << bit_shift2); 
            for (vid_t s_i = 0; s_i < p_p; s_i++) {
                // #pragma omp parallel for 
                for (vid_t s_j = 0; s_j < p_p; s_j++) {

                    index = offset + ((s_i << bit_shift3) + s_j);
                    m = ((i << bit_shift3) + s_i) << bit_shift2;
                    n = ((j << bit_shift3) + s_j) << bit_shift2; 
                    
                    nebr_count = snaph->get_nebrs(index, header);
                    if (0 == nebr_count) continue;
                    base_eid = snaph->get_first_eid(index);
                    for (vid_t e = 0; e < nebr_count; ++e) {
                        eid = e + base_eid;
                        // dst = csr.next(header);
                        snb = snaph->get_snb(header, e);
                        if (reverse ==1) {
                            dst1 = snb.src + m;
                            src1 = snb.dst + n;
                        }else {
                            dst1 = snb.dst + n;
                            src1 = snb.src + m;
                        }

                        // update the feature
                        float* input_right_per_edge = input_right[eid];
                        float* input_left_per_edge = input_left[src1];
                        float* output_per_edge = output[eid];

                        for (int64_t h = 0; h < output_dim; h++){
                            output_per_edge[h] = op_fn(input_right_per_edge[h], input_left_per_edge[h]);
                        }

                    }
                }
            }
        }
    }
}



void _spmmw2d_snb(csr_t* snaph, array3d_t<float> & input, array2d_t<float>& edge_weight,
             array3d_t<float> & output, op_t op, int64_t reverse)
{
    vid_t v_count = snaph->get_vcount();
    int output_dim = input.col_count;
    int num_head = input.row_count;
    assert(op == eSUM);

    //loop for every edge
    vid_t nebr_count = 0;
    vid_t* header; 
    vid_t index = 0, m, n, offset;
    snb_t snb;
    vid_t dst1;
    float* input_per_head;
    float edge_weight_edge;
    vid_t eid = 0;
    vid_t base_eid = 0;
    vid_t src1;
    vid_t p = (snaph->v_count >> bit_shift1) + (0 != (snaph->get_vcount() & part_mask1_2));

        for (vid_t i = 0; i < p; ++i) {
            for (vid_t j = 0; j < p; ++j) {
                offset = ((i*p + j) << bit_shift2); 
                for (vid_t s_i = 0; s_i < p_p; s_i++) {
                    // #pragma omp parallel for 
                    for (vid_t s_j = 0; s_j < p_p; s_j++) {

                        index = offset + ((s_i << bit_shift3) + s_j);
                        m = ((i << bit_shift3) + s_i) << bit_shift2;
                        n = ((j << bit_shift3) + s_j) << bit_shift2; 
                        
                        nebr_count = snaph->get_nebrs(index, header);
                        if (0 == nebr_count) continue;
                        base_eid = snaph->get_first_eid(index);
                        for (vid_t e = 0; e < nebr_count; ++e) {
                            eid = e + base_eid;
                            snb = snaph->get_snb(header, e);
                            if (reverse ==1) {
                                dst1 = snb.src + m;
                                src1 = snb.dst + n;
                            }else {
                                dst1 = snb.dst + n;
                                src1 = snb.src + m;
                            }

                            // update the feature  
                            for (int64_t s_h = 0; s_h < num_head; s_h++){

                                array1d_t<float> message_per_head = output.get_row(src1, s_h);
                                float edge_weight_edge = 0;
                                input_per_head = input.get_row_ptr(dst1, s_h);
                                edge_weight_edge = edge_weight.get_item(eid, s_h);
                                message_per_head.addw(input_per_head, edge_weight_edge); 
                                output.row_copy(message_per_head.data_ptr, src1, s_h);

                            }            

                        }
                    }
                }
            }
        }
}
