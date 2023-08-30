#pragma once

#include "csr.h"
#include "op.h"

extern int THD_COUNT;
    
void run_bfs(graph_t& g, vid_t root);

//_gspmv ---> spmm
void _spmm_snb(csr_t* snaph, array2d_t<float> & input, array2d_t<float> & output, op_t op, bool reverse, bool norm = true);


void _spmmw_snb(csr_t* snaph, array2d_t<float> & input, array1d_t<float>& edge_weight, array2d_t<float> & output, op_t op, int64_t reverse);


void _spmmw_snb(csr_t* snaph, array1d_t<float>& edge_weight, array1d_t<float> & output, op_t op, int64_t reverse);


void _sddmm_snb(csr_t* snaph, array1d_t<float> & input_left, array1d_t<float> & input_right, array1d_t<float> & output, op_t op, int64_t reverse);


void _sddmme_snb(csr_t* snaph, array2d_t<float> & input_left, array2d_t<float> & input_right, array1d_t<float> & output, op_t op, int64_t reverse);


void _sddmme2d_snb(csr_t* snaph, array3d_t<float> & input_left, array3d_t<float> & input_right, array2d_t<float> & output, op_t op, int64_t reverse);


void _spmmw2d_snb(csr_t* snaph, array2d_t<float>& edge_weight, array2d_t<float> & output, op_t op, int64_t reverse);


void _sddmm2d_snb(csr_t* snaph, array2d_t<float> & input_left, array2d_t<float> & input_right, array2d_t<float> & output, op_t op, int64_t reverse);


void _spmmw2d_snb(csr_t* snaph, array3d_t<float> & input, array2d_t<float>& edge_weight, array3d_t<float> & output, op_t op, int64_t reverse);
