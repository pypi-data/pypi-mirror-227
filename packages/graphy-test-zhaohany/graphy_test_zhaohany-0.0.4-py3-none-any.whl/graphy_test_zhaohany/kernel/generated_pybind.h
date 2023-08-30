//#include <pybind11/pybind11.h>
//#include "dlpack.h"
//#include "kernel.h"
//#include "csr.h"

//namespace py = pybind11;

inline void export_kernel(py::module &m) { 
    //gspmv ---> spmm
    m.def("spmm",
        [](graph_t& graph, py::capsule& input, py::capsule& output, bool reverse, bool norm) {
            array2d_t<float> input_array = capsule_to_array2d(input);
            array2d_t<float> output_array = capsule_to_array2d(output);
            return invoke_spmm(graph, input_array, output_array, reverse, norm);
        }
    );


     //gspmvw -----> _spmmw     
     m.def("gspmmw",
         [](graph_t& graph, py::capsule& input, py::capsule& output, op_t op, bool reverse) {
             array1d_t<float> input_array = capsule_to_array1d(input);
             array1d_t<float> output_array = capsule_to_array1d(output);
             return invoke_spmmw(graph, input_array, output_array, (op_t)op, reverse);
        }
    );

    //spmmw_op --> spmmw_op
    m.def("gspmmw_op",
         [](graph_t& graph, py::capsule& input, py::capsule& edge_weight, py::capsule& output, op_t op, bool reverse) {
             array2d_t<float> input_array = capsule_to_array2d(input);
             array2d_t<float> output_array = capsule_to_array2d(output);
             array1d_t<float> edge_weight_array = capsule_to_array1d(edge_weight);
             return invoke_spmmw_op(graph, input_array, edge_weight_array, output_array, (op_t)op, reverse);
       }
    );

    //gspmvw2d ------> _spmmw2d
    m.def("spmmw2d",
         [](graph_t& graph, py::capsule& input, py::capsule& output, op_t op, bool reverse) {
             array2d_t<float> input_array = capsule_to_array2d(input);
             array2d_t<float> output_array = capsule_to_array2d(output);
             return invoke_spmmw2d(graph, input_array, output_array, (op_t)op, reverse);
        }
    );

    //spmmw_op2d ------>.  _spmmw2d
    m.def("spmmw_op2d",
         [](graph_t& graph, py::capsule& input, py::capsule& edge_weight, py::capsule& output, op_t op, bool reverse) {
             array3d_t<float> input_array = capsule_to_array3d(input);
             array3d_t<float> output_array = capsule_to_array3d(output);
             array2d_t<float> edge_weight_array = capsule_to_array2d(edge_weight);
             return invoke_spmmw_op2d(graph, input_array, edge_weight_array, output_array, (op_t)op, reverse);

       }
    );
      
    //gsddmm ---->. _sddmm
    m.def("gsddmm",
        [](graph_t& graph, py::capsule& input_left, py::capsule& input_right, py::capsule& output, op_t op, bool reverse) {
             //cout << "pybind sddmm" << op << endl;
             array1d_t<float> input_array_left = capsule_to_array1d(input_left);
             array1d_t<float> input_array_right = capsule_to_array1d(input_right);
             array1d_t<float> output_array = capsule_to_array1d(output);
             return invoke_sddmm(graph, input_array_left, input_array_right, output_array, (op_t)op, reverse);
       }
    );
      
    m.def("gsddmme",
         [](graph_t& graph, py::capsule& input_left, py::capsule& input_right, py::capsule& output, op_t op, bool reverse) {
             array2d_t<float> input_array_left = capsule_to_array2d(input_left);
             array2d_t<float> input_array_right = capsule_to_array2d(input_right);
             array1d_t<float> output_array = capsule_to_array1d(output);
             return invoke_sddmme(graph, input_array_left, input_array_right, output_array, (op_t)op, reverse);
       }
    );

    m.def("gsddmme2d",
         [](graph_t& graph, py::capsule& input_left, py::capsule& input_right, py::capsule& output, op_t op, bool reverse) {
             array3d_t<float> input_array_left = capsule_to_array3d(input_left);
             array3d_t<float> input_array_right = capsule_to_array3d(input_right);
             array2d_t<float> output_array = capsule_to_array2d(output);
             return invoke_sddmme2d(graph, input_array_left, input_array_right, output_array, (op_t)op, reverse);
        }
    );

    //. gsddmm2d  ---------> _sddmm2d
    m.def("sddmm2d",
         [](graph_t& graph, py::capsule& input_left, py::capsule& input_right, py::capsule& output, op_t op, bool reverse) {
             array2d_t<float> input_array_left = capsule_to_array2d(input_left);
             array2d_t<float> input_array_right = capsule_to_array2d(input_right);
             array2d_t<float> output_array = capsule_to_array2d(output);
             return invoke_sddmm2d(graph, input_array_left, input_array_right, output_array, (op_t)op, reverse);
       }
    );

    // the binding code for model compression
    m.def("gspmmw_model",
         [](graph_t& graph, py::capsule& input, py::capsule& edge_weight, py::capsule& bias, py::capsule& output, op_t op, bool reverse) {
             array2d_t<float> input_array = capsule_to_array2d(input);
             array2d_t<float> output_array = capsule_to_array2d(output);
             array1d_t<float> edge_weight_array = capsule_to_array1d(edge_weight);
             array1d_t<float> bias_array = capsule_to_array1d(bias);

             return invoke_spmmw_model(graph, input_array, edge_weight_array, bias_array, output_array, (op_t)op, reverse);

        }
    );


 m.def("gspmmw_model_without_bias",
         [](graph_t& graph, py::capsule& input, py::capsule& edge_weight, py::capsule& output, op_t op, bool reverse) {
             array2d_t<float> input_array = capsule_to_array2d(input);
             array2d_t<float> output_array = capsule_to_array2d(output);
             array1d_t<float> edge_weight_array = capsule_to_array1d(edge_weight);
             return invoke_spmmw_model_without_bias(graph, input_array, edge_weight_array, output_array, (op_t)op, reverse);

        }
    );




    m.def("gsddmme_model",
         [](graph_t& graph, py::capsule& input_left, py::capsule& input_right, py::capsule& output, op_t op) {
             array2d_t<float> input_array_left = capsule_to_array2d(input_left);
             array2d_t<float> input_array_right = capsule_to_array2d(input_right);
             array1d_t<float> output_array = capsule_to_array1d(output);
             return invoke_sddmme_model(graph, input_array_left, input_array_right, output_array, (op_t)op);
        }
    );


}
