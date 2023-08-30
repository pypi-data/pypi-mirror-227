#include <cassert>
#include <iostream>
#include <limits>

#include "kernel.h"

using std::cout;
using std::endl;

int THD_COUNT = 1;

//_gspmv ---> spmm
void _spmm(csr_t* snaph, array2d_t<float> & input, array2d_t<float> & output, 
                     op_t op, bool reverse, bool norm /*= true*/)
{
    vid_t v_count = snaph->get_vcount();
    int output_dim = input.col_count;

    //cout << "spmm " << op << "reverse = " << reverse << endl;

    //If in backward, normalize it first
    if (reverse == 1 && norm == true) {
        #pragma omp parallel for 
        for (vid_t v = 0; v < v_count; v++) { 
            vid_t nebr_count = snaph->get_degree(v);
            if (nebr_count > 1) {
                input.row_normalize(v, nebr_count); 
            }
        }
    }
    
    
    //Start of parallelism
    #pragma omp parallel for 
    for (vid_t v = 0; v < v_count; v++) 
    { 
        vid_t nebr_count = 0;
        vid_t* nebrs_reader;
        vid_t sid;
        nebr_count = snaph->get_nebrs(v, nebrs_reader);
        // if one node do not have any neighbor, we do not scatter it's message
        if (nebr_count == 0) {
            //result[v] = input_feature[v];
            continue; 
        }
        
        // the node j scatter it's message to all neighors
        array1d_t<float> message(output_dim);//zero initialized
        //edit here for self loop
        for (vid_t i = 0; i < nebr_count; ++i) {
            sid = snaph->get_vid(nebrs_reader, i);
            message.add(input[sid]);
        }
        //output.row_copy(message.data_ptr, v);
        //If in forward, normalize it now.
        if (nebr_count > 1 && reverse ==0 && norm == true) {
            output.row_copy_norm(message.data_ptr, v, nebr_count);
        } else {
            output.row_copy(message.data_ptr, v);
        }
    }
}



//_gspmvw ---> spmmw
void _spmmw(csr_t* snaph, array2d_t<float> & input, array1d_t<float>& edge_weight,
             array2d_t<float> & output, op_t op, int64_t reverse)
{
    //cout << "spmm_op is " << op << "reverse="<< reverse << endl;
    vid_t v_count = snaph->get_vcount();
    int output_dim = input.col_count;

    assert(op == eSUM);

    //Start of parallelism
    #pragma omp parallel 
    {
        float* message;
        float* input_value;
        vid_t nebr_count = 0;
        vid_t sid;
        vid_t eid = 0;
        vid_t* nebrs_reader;
        #pragma omp for
        for (vid_t v = 0; v < v_count; v++) {
            nebr_count = snaph->get_nebrs(v, nebrs_reader);
            message = output[v];
            // if one node do not have any neighbor, we do not scatter it's message
            
            //edit here for self loop
            for (vid_t i = 0; i < nebr_count; ++i) {
                sid = snaph->get_vid(nebrs_reader, i);
                eid = snaph->get_eid(nebrs_reader, i);
                input_value = input[sid];
                
                for (vid_t h = 0; h < output_dim; ++h) {
                    message[h] += input_value[h]*edge_weight[eid];
                }
            }
        }
    }
}

//only |E| as the input
//_gspmv ---> spmmw
void _spmmw(csr_t* snaph, array1d_t<float>& edge_weight,
             array1d_t<float> & output, op_t op, int64_t reverse)
{
    //cout << "spmm is " << op << "reverse = " << reverse << endl;
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

    //Start of parallelism
    #pragma omp parallel for 
    for (vid_t v = 0; v < v_count; v++) 
    { 
        float message = 0;
        vid_t nebr_count = 0;
        vid_t sid;
        vid_t eid = 0;
        vid_t* nebrs_reader;
        nebr_count = snaph->get_nebrs(v, nebrs_reader);

        if (op == eMAX) message = -std::numeric_limits<float>::infinity();
        if (op == eMIN) message = std::numeric_limits<float>::infinity();
        
        //edit here for self loop
        for (vid_t i = 0; i < nebr_count; ++i) {
            eid = snaph->get_eid(nebrs_reader, i);
            message = op_fn(message, edge_weight[eid]);
        }
        output[v] = message;
    }
}

// calcuate the feature by edge, left is vertex, right is edge
// _gsddmm ----> _sddmm
void _sddmm(csr_t* snaph, 
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

    //Start of parallelism
    #pragma omp parallel for 
    for (vid_t v = 0; v < v_count; v++) 
    {
        vid_t nebr_count = 0;
        vid_t sid, eid;
        vid_t* nebrs_reader;
        nebr_count = snaph->get_nebrs(v, nebrs_reader);

        float result_score = 0;
        for (vid_t i = 0; i < nebr_count; ++i) {
            sid = snaph->get_vid(nebrs_reader, i);
            eid = snaph->get_eid(nebrs_reader, i);
            output[eid] = op_fn(input_right[eid], input_left[v]);
        }
    }
}

void _sddmme(csr_t* snaph, 
        array2d_t<float> & input_left, array2d_t<float> & input_right,
        array1d_t<float> & output, op_t op, int64_t reverse)
{
    //cout <<"sddmme" <<endl;
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
            input_left_per_edge = input_left[sid];
            input_right_per_edge = input_right[v];

            for (int64_t h = 0; h < output_dim; h++) {
                output[eid] += op_fn(input_right_per_edge[h], input_left_per_edge[h]);
            }
        }
    }
}


void _sddmme2d(csr_t* snaph, 
        array3d_t<float> & input_left, array3d_t<float> & input_right,
        array2d_t<float> & output, op_t op, int64_t reverse)
{
    //cout <<"sddmme" <<endl;
    int heads = input_left.row_count;
    int output_dim = input_left.col_count;

    //cout << "sddmme2d: dim:" <<  heads << output_dim << endl;

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

    //Start of parallelism
    #pragma omp parallel 
    {
        vid_t nebr_count = 0;
        vid_t sid, eid;
        vid_t* nebrs_reader;
        float result_score;
        float* input_left_per_edge_per_head; 
        float* input_right_per_edge_per_head; 
        float* message_per_edge;
        #pragma omp for 
        for (vid_t v = 0; v < v_count; v++) {
            nebr_count = snaph->get_nebrs(v, nebrs_reader);
            for (vid_t i = 0; i < nebr_count; ++i) {
                sid = snaph->get_vid(nebrs_reader, i);
                eid = snaph->get_eid(nebrs_reader, i);
                message_per_edge = output[eid];
                
                for (int64_t j = 0; j < heads; j++){
                    input_left_per_edge_per_head = input_left.get_row_ptr(sid, j);
                    input_right_per_edge_per_head = input_right.get_row_ptr(v,j);

                    //backward kernels have > 1 as output_dim, and  = 1 in forward.
                    for (int64_t h = 0; h < output_dim; h++){
                        message_per_edge[j] += op_fn(input_right_per_edge_per_head[h], 
                                                     input_left_per_edge_per_head[h]);
                    }
                }
            }
        }
    }
}


//only |E*head| as the input
void _spmmw2d(csr_t* snaph, array2d_t<float>& edge_weight,
             array2d_t<float> & output, op_t op, int64_t reverse)
{
    //cout << "spmmw2d" <<endl; 
    vid_t v_count = snaph->get_vcount();
    int output_dim = edge_weight.col_count;
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
    
    //Start of parallelism
    #pragma omp parallel for 
    for (vid_t v = 0; v < v_count; v++)
    {
        float* message = output[v]; //it is 1D tensor
        vid_t nebr_count = 0;
        vid_t sid;
        vid_t eid = 0;
        vid_t* nebrs_reader;
        float* edge_weight_per_edge;// edge_weight is 2d tensor
        nebr_count = snaph->get_nebrs(v, nebrs_reader);
        
        // if one node do not have any neighbor, we do not scatter it's message
        if (op == eMAX){
            for (int64_t h = 0; h < output_dim; h++){
                message[h] = -std::numeric_limits<float>::infinity();
            }
        } else if (op == eMIN) {
            for (int64_t h = 0; h < output_dim; h++){
                message[h] = std::numeric_limits<float>::infinity();
            }
        }

        //edit here for self loop
        /*for (int64_t h = 0; h < output_dim; h++){//loop for the num_heads dim
            for (vid_t i = 0; i < nebr_count; ++i) {
                eid = snaph->get_eid(nebrs_reader, i);
                edge_weight_per_edge = edge_weight[eid];// edge_weight is 2d tensor
                message[h] = op_fn(message[h], edge_weight_per_edge[h]);
            }
        }*/
        for (vid_t i = 0; i < nebr_count; ++i) {
            eid = snaph->get_eid(nebrs_reader, i);
            edge_weight_per_edge = edge_weight[eid];// edge_weight is 2d tensor
            for (int64_t h = 0; h < output_dim; h++) {//loop for the num_heads dim
                message[h] = op_fn(message[h], edge_weight_per_edge[h]);
            }
        }
    }
}

void _sddmm2d(csr_t* snaph, 
        array2d_t<float> & input_left, array2d_t<float> & input_right,
        array2d_t<float> & output, op_t op, int64_t reverse)
{
    //cout <<"sddmm2d" <<endl;
    //output_dim is actually head.
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

    //Start of parallelism
    #pragma omp parallel for 
    for (vid_t v = 0; v < v_count; v++)
    {
        vid_t nebr_count = 0;
        vid_t sid, eid;
        vid_t* nebrs_reader;
        nebr_count = snaph->get_nebrs(v, nebrs_reader);
        for (vid_t i = 0; i < nebr_count; ++i) {
            sid = snaph->get_vid(nebrs_reader, i);
            eid = snaph->get_eid(nebrs_reader, i);
            float* input_right_per_edge = input_right[eid];
            float* input_left_per_edge = input_left[v];
            float* output_per_edge = output[eid];

            for (int64_t h = 0; h < output_dim; h++) {
                output_per_edge[h] = op_fn(input_right_per_edge[h], input_left_per_edge[h]);
            }
        }
    }
}

void _spmmw_op2d(csr_t* snaph, array3d_t<float> & input, array2d_t<float>& edge_weight,
             array3d_t<float> & output, op_t op, int64_t reverse)
{
    //cout <<"spmmw2d" <<endl;
    vid_t v_count = snaph->get_vcount();
    int output_dim = input.col_count;
    int num_head = input.row_count;
    assert(op == eSUM);

    //Start of parallelism
    #pragma omp parallel 
    {
        array1d_t<float> input_per_head = 0;
        vid_t nebr_count = 0;
        vid_t sid;
        vid_t eid = 0;
        vid_t* nebrs_reader;
        #pragma omp for
        for (vid_t v = 0; v < v_count; v++) 
        { 
            nebr_count = snaph->get_nebrs(v, nebrs_reader);
            // if one node do not have any neighbor, we do not scatter it's message
            if (nebr_count == 0) {
                //result[v] = input_feature[v];
                continue; 
            }

            // a loop for 2nd dim, H
            // the node j scatter it's message to all neighors
            //edit here for self loop
            for (vid_t i = 0; i < nebr_count; ++i) {
                sid = snaph->get_vid(nebrs_reader, i);
                eid = snaph->get_eid(nebrs_reader, i);
                float* edge_weight_edge = edge_weight.data_ptr + eid*num_head;//get_item(eid, h);
                for (int64_t h = 0; h < num_head; h++) {
                    float* message_per_head = output.data_ptr + v * num_head * output_dim + h*output_dim;
                    float* input_per_head = input.data_ptr + sid*num_head * output_dim + h*output_dim;
                    for (int j = 0; j < output_dim; ++j) {
                        message_per_head[j] += input_per_head[j] * edge_weight_edge[h];
                    }
                }
            }
        }
    }
}

void _spmmw_op2d_11(csr_t* snaph, array3d_t<float> & input, array2d_t<float>& edge_weight,
             array3d_t<float> & output, op_t op, int64_t reverse)
{
    //cout <<"spmmw2d" <<endl;
    vid_t v_count = snaph->get_vcount();
    int output_dim = input.col_count;
    int num_head = input.row_count;
    assert(op == eSUM);

    //Start of parallelism
    #pragma omp parallel 
    {
        array1d_t<float> input_per_head = 0;
        vid_t nebr_count = 0;
        vid_t sid;
        vid_t eid = 0;
        vid_t* nebrs_reader;
        #pragma omp for
        for (vid_t v = 0; v < v_count; v++) 
        { 
            nebr_count = snaph->get_nebrs(v, nebrs_reader);
            // if one node do not have any neighbor, we do not scatter it's message
            if (nebr_count == 0) {
                //result[v] = input_feature[v];
                continue; 
            }

            // a loop for 2nd dim, H
            for (int64_t h = 0; h < num_head; h++) {
                array1d_t<float> message_per_head = output.get_row(v, h);
                float edge_weight_edge = 0;
                // the node j scatter it's message to all neighors
                //edit here for self loop
                for (vid_t i = 0; i < nebr_count; ++i) {
                    sid = snaph->get_vid(nebrs_reader, i);
                    eid = snaph->get_eid(nebrs_reader, i);
                    float* input_per_head = input.get_row_ptr(sid, h);
                    float edge_weight_edge = edge_weight.get_item(eid, h);
                    message_per_head.addw(input_per_head, edge_weight_edge);
                }
                output.row_copy(message_per_head.data_ptr, v, h);
            }
        }
    }
}


void invoke_spmm(graph_t& graph, array2d_t<float> & input_array, array2d_t<float> & output_array,
                 bool reverse, bool norm /*= true*/)
{
    if (reverse) {
         return _spmm(&graph.csr, input_array, output_array, eSUM, reverse, norm);
    } else {
         return _spmm(&graph.csc, input_array, output_array, eSUM, reverse, norm);
    }
}

void invoke_spmmw(graph_t& graph, array1d_t<float>& input_array,
             array1d_t<float> & output_array, op_t op, int64_t reverse)
{
    if (reverse) {
        return _spmmw(&graph.csr, input_array, output_array, (op_t)op, reverse);
     } else {
        return _spmmw(&graph.csc, input_array, output_array, (op_t)op, reverse);
    }
}

void invoke_spmmw_op(graph_t& graph, array2d_t<float> & input_array, array1d_t<float>& edge_weight_array,
             array2d_t<float> & output_array, op_t op, int64_t reverse)
{
    if (reverse) {
        return _spmmw(&graph.csr, input_array, edge_weight_array, output_array, (op_t)op, reverse);
    } else {
        return _spmmw(&graph.csc, input_array, edge_weight_array, output_array, (op_t)op, reverse);
    }
}

void invoke_spmmw2d(graph_t& graph, array2d_t<float>& input_array,
             array2d_t<float> & output_array, op_t op, int64_t reverse)
{
    if (reverse) {
        return _spmmw2d(&graph.csr, input_array, output_array, (op_t)op, reverse);
    } else {
        return _spmmw2d(&graph.csc, input_array, output_array, (op_t)op, reverse);
    }
}

void invoke_spmmw_op2d(graph_t& graph, array3d_t<float> & input_array, array2d_t<float>& edge_weight_array,
             array3d_t<float> & output_array, op_t op, int64_t reverse)
{
    if (reverse) {
        return _spmmw_op2d(&graph.csr, input_array, edge_weight_array, output_array, (op_t)op, reverse);

    } else {
        return _spmmw_op2d(&graph.csc, input_array, edge_weight_array, output_array, (op_t)op, reverse);
    }
}

void invoke_sddmm(graph_t& graph, 
        array1d_t<float> & input_array_left, array1d_t<float> & input_array_right,
        array1d_t<float> & output_array, op_t op, int64_t reverse)
{
    if (reverse) {
        return _sddmm(&graph.csr, input_array_left, input_array_right, output_array, (op_t)op, reverse);
    } else {
        return _sddmm(&graph.csc, input_array_left, input_array_right, output_array, (op_t)op, reverse);
    }
}

void invoke_sddmme(graph_t& graph, 
        array2d_t<float> & input_array_left, array2d_t<float> & input_array_right,
        array1d_t<float> & output_array, op_t op, int64_t reverse)
{
    if (reverse) {
        return _sddmme(&graph.csr, input_array_left, input_array_right, output_array, (op_t)op, reverse);
    } else {
        return _sddmme(&graph.csc, input_array_left, input_array_right, output_array, (op_t)op, reverse);
    }
}

void invoke_sddmme2d(graph_t& graph, 
        array3d_t<float> & input_array_left, array3d_t<float> & input_array_right,
        array2d_t<float> & output_array, op_t op, int64_t reverse) 
{
    if (reverse) {
        return _sddmme2d(&graph.csr, input_array_left, input_array_right, output_array, (op_t)op, reverse);
    } else {
        return _sddmme2d(&graph.csc, input_array_left, input_array_right, output_array, (op_t)op, reverse);
    }
}
    
void invoke_sddmm2d(graph_t& graph, 
        array2d_t<float> & input_array_left, array2d_t<float> & input_array_right,
        array2d_t<float> & output_array, op_t op, int64_t reverse)
{
    if (reverse) {
        return _sddmm2d(&graph.csr, input_array_left, input_array_right, output_array, (op_t)op, reverse);
    } else {
        return _sddmm2d(&graph.csc, input_array_left, input_array_right, output_array, (op_t)op, reverse);
    }
}

