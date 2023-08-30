#pragma once

#include "csr.h"
#include "op.h"

extern int THD_COUNT;

inline float add_scalar(float x, float y) {
    return x + y;
}

inline float sub_scalar(float x, float y) {
    return x - y;
}

inline float max_scalar(float x, float y) {
    return std::max(x, y);
}

inline float min_scalar(float x, float y) {
    return std::min(x, y);
}

inline float mul_scalar(float x, float y) {
    return x*y;
}

inline float div_scalar(float x, float y) {
    return x/y;
}

typedef float (*op_scalar_fn)(float, float);
//op_scalar_fn op_fn = mul_scalar;
    
void run_bfs(graph_t& g, vid_t root);

//_gspmv ---> spmm
void invoke_spmm(graph_t& graph, array2d_t<float> & input, array2d_t<float> & output, 
                 bool reverse, bool norm);

//_gspmvw ---> spmmw
void invoke_spmmw_op(graph_t& graph, array2d_t<float> & input, array1d_t<float>& edge_weight,
             array2d_t<float> & output, op_t op, int64_t reverse);

//_gspmv ---> spmmw
void invoke_spmmw(graph_t& graph, array1d_t<float>& edge_weight,
             array1d_t<float> & output, op_t op, int64_t reverse);

//only |E| as the input
// _gspmvw2d ---> _spmmw2d
void invoke_spmmw2d(graph_t& graph, array2d_t<float>& edge_weight,
             array2d_t<float> & output, op_t op, int64_t reverse);


// _gspmvw2d ---> _spmmw2d
void invoke_spmmw_op2d(graph_t& graph, array3d_t<float> & input, array2d_t<float>& edge_weight,
             array3d_t<float> & output, op_t op, int64_t reverse);

// calcuate the feature by edge, left is vertex, right is edge
// _gsddmm ----> _sddmm
void invoke_sddmm(graph_t& graph, 
        array1d_t<float> & input_left, array1d_t<float> & input_right,
        array1d_t<float> & output, op_t op, int64_t reverse);

// _gsddmm2d ----> _sddmm2d
void invoke_sddmm2d(graph_t& graph, 
        array2d_t<float> & input_left, array2d_t<float> & input_right,
        array2d_t<float> & output, op_t op, int64_t reverse);


void invoke_sddmme(graph_t& graph, 
        array2d_t<float> & input_left, array2d_t<float> & input_right,
        array1d_t<float> & output, op_t op, int64_t reverse);

void invoke_sddmme2d(graph_t& graph, 
        array3d_t<float> & input_left, array3d_t<float> & input_right,
        array2d_t<float> & output, op_t op, int64_t reverse);


void invoke_sddmme_model(graph_t& graph, array2d_t<float> & input_left, array2d_t<float> & input_right, array1d_t<float> & output, op_t op);

void invoke_spmmw_model(graph_t& graph, array2d_t<float> & input, array1d_t<float>& edge_weight, array1d_t<float>& bias_array, array2d_t<float> & output, op_t op, int64_t reverse);

void invoke_spmmw_model_without_bias(graph_t& graph, array2d_t<float> & input, array1d_t<float>& edge_weight, array2d_t<float> & output, op_t op, int64_t reverse);




void invoke_spmmw_model_without_bias(graph_t& graph, array2d_t<float> & input, array1d_t<float>& edge_weight, array2d_t<float> & output, op_t op, int64_t reverse);



void _spmm_snb(csr_t* snaph, array2d_t<float> & input, array2d_t<float> & output, op_t op, bool reverse, bool norm = true);


void _spmmw_snb(csr_t* snaph, array2d_t<float> & input, array1d_t<float>& edge_weight, array2d_t<float> & output, op_t op, int64_t reverse);


void _spmmw_snb(csr_t* snaph, array1d_t<float>& edge_weight, array1d_t<float> & output, op_t op, int64_t reverse);


void _sddmm_snb(csr_t* snaph, array1d_t<float> & input_left, array1d_t<float> & input_right, array1d_t<float> & output, op_t op, int64_t reverse);


void _sddmme_snb(csr_t* snaph, array2d_t<float> & input_left, array2d_t<float> & input_right, array1d_t<float> & output, op_t op, int64_t reverse);


void _sddmme2d_snb(csr_t* snaph, array3d_t<float> & input_left, array3d_t<float> & input_right, array2d_t<float> & output, op_t op, int64_t reverse);


void _spmmw2d_snb(csr_t* snaph, array2d_t<float>& edge_weight, array2d_t<float> & output, op_t op, int64_t reverse);


void _sddmm2d_snb(csr_t* snaph, array2d_t<float> & input_left, array2d_t<float> & input_right, array2d_t<float> & output, op_t op, int64_t reverse);


void _spmmw2d_snb(csr_t* snaph, array3d_t<float> & input, array2d_t<float>& edge_weight, array3d_t<float> & output, op_t op, int64_t reverse);

void _sddmme_model_csr(csr_t* snaph, array2d_t<float> & input_left, array2d_t<float> & input_right, array1d_t<float> & output, op_t op);

void _sddmme_model_coo(const coo_t* snaph, array2d_t<float> & input_left, array2d_t<float> & input_right, array1d_t<float> & output, op_t op);

