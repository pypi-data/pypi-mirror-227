import numpy as np
import dgl
import datetime
import statistics
import networkx as nx
import pygraph as gone


def build_graphpy(num_node, file_path):
    ingestion_flag = gone.enumGraph.eUnidir | gone.enumGraph.eDoubleEdge | gone.enumGraph.eCreateEID
    edge_dt = np.dtype([('src', np.int32), ('dst', np.int32), ('edgeid', np.int32)])

    outdir = ""
    graph = gone.init(1, 1, outdir)  # Indicate one pgraph, and one vertex type
    tid0 = graph.init_vertex_type(num_node, True, "gtype")  # initiate the vertex type
    start = datetime.datetime.now()
    pgraph = graph.create_schema(ingestion_flag, tid0, "friend", edge_dt)  # initiate the pgraph
    # creating graph directly from file requires some efforts. Hope to fix that later
    manager = graph.get_pgraph_managerW(0)  # This assumes single weighted graph, edgeid is the weight
    manager.add_edges_from_dir(file_path, ingestion_flag, num_sources)  # ifile has no weights, edgeid will be generated
    pgraph.wait()  # You can't call add_edges() after wait(). The need of it will be removed in future.
    end = datetime.datetime.now()
    manager.run_bfs(1)
    snap_t = gone.create_static_view(pgraph, gone.enumView.eStale)
    difference = (end - start)

    return snap_t, difference


def build_graphpy_plain(num_node, file_path):
    ingestion_flag = gone.enumGraph.eUdir
    edge_dt = np.dtype([('src', np.int32), ('dst', np.int32)])

    outdir = ""
    graph = gone.init(1, 1, outdir)  # Indicate one pgraph, and one vertex type
    tid0 = graph.init_vertex_type(num_node, True, "gtype")  # initiate the vertex type
    start = datetime.datetime.now()
    pgraph = graph.create_schema(ingestion_flag, tid0, "friend", edge_dt)  # initiate the pgraph
    # creating graph directly from file requires some efforts. Hope to fix that later
    manager = graph.get_pgraph_manager(0)  # This assumes single weighted graph, edgeid is the weight
    manager.add_edges_from_dir(file_path, ingestion_flag)  # ifile has no weights, edgeid will be generated
    end = datetime.datetime.now()
    pgraph.wait()  # You can't call add_edges() after wait(). The need of it will be removed in future.
    manager.run_bfs(1)
    snap_t = gone.create_static_view(pgraph, gone.enumView.eStale)
    difference = (end - start)

    return snap_t, difference


def build_graphpy_edge_id_parallel(num_node, file_path, num_sources, num_thread):
    ingestion_flag = gone.enumGraph.eUnidir | gone.enumGraph.eDoubleEdge | gone.enumGraph.eCreateEID
    edge_dt = np.dtype([('src', np.int32), ('dst', np.int32), ('edgeid', np.int32)])

    outdir = ""
    graph = gone.init(1, 1, outdir, num_sources, num_thread)  # Indicate one pgraph, and one vertex type
    tid0 = graph.init_vertex_type(num_node, True, "gtype")  # initiate the vertex type
    start = datetime.datetime.now()
    pgraph = graph.create_schema(ingestion_flag, tid0, "friend", edge_dt)  # initiate the pgraph
    # creating graph directly from file requires some efforts. Hope to fix that later
    manager = graph.get_pgraph_managerW(0)  # This assumes single weighted graph, edgeid is the weight
    manager.add_edges_from_dir(file_path, ingestion_flag)  # ifile has no weights, edgeid will be generated
    #end = datetime.datetime.now()
    pgraph.wait()  # You can't call add_edges() after wait(). The need of it will be removed in future.
    end = datetime.datetime.now()
    manager.run_bfs(1)
    snap_t = gone.create_static_view(pgraph, gone.enumView.eStale)
    difference = (end - start)

    return snap_t, difference


if __name__ == "__main__":
    # fixed the num_thread to 4 and change num_sources to 1,2,4
    times = 10
    num_sources = 4
    num_thread = 4 
    result_cora = []
    result_pubmed = []
    result_amazon = []
    result_patent_citation = []
    # experiment for cora data set
    graph_data_path ="/home/datalab/data/test3/mult_process/multi"
    graph_data_path1 = "/home/datalab/data/test3/mult_process/multi_patent_citation"
    #num_node1 = 99999999
    num_node = 37747700
    graph, difference = build_graphpy_edge_id_parallel(num_node, graph_data_path1, num_sources, num_thread)
    result_patent_citation.append(difference)
    print ('time is:', difference)
