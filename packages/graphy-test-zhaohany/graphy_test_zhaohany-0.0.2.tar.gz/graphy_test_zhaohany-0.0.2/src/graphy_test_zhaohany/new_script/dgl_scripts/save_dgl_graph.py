import sys
import dgl
from dgl.data.utils import save_graphs
import numpy as np
import argparse
import os

def read_graph_data(file_path, line_needed_to_skip):
    crs = open(file_path, "r")
    #print ("Output of Read function is ")
    # print (crs.read())
    a = [line.split() for line in crs]
    comment = a[0:line_needed_to_skip]
    array = a[line_needed_to_skip:]
    
    # convert the edge to src and dst
    src = []
    dst = []
    for each_edge in array:
        if each_edge[0] == '#' or each_edge[0] == '%':
            continue;
        src.append(int(each_edge[0]))
        dst.append(int(each_edge[1]))
    return src, dst, comment

def build_dgl_graph(src, dst):
    # while the other for destination endpoints.
    src = np.array(src)
    dst = np.array(dst)
    # Edges are directional in DGL; Make them bi-directional.
    u = np.concatenate([src, dst])
    v = np.concatenate([dst, src])
    # Construct a DGLGraph
    return dgl.graph((u, v))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Pick text file name')
    parser.add_argument('--gdir', type=str,  help='pick the file name of saved dgl graph')
    parser.add_argument('--odir', type=str,  help='pick the dir of saved dgl graph')
    
    args = parser.parse_args()
    graph_data_path = args.gdir + "graph.txt"
    odir = args.odir
    line_needed_to_skip = 0

    src, dst, comment = read_graph_data(graph_data_path, line_needed_to_skip)
    graph = build_dgl_graph(src, dst)
 
    is_exist = os.path.exists(odir)
    if not is_exist:
        os.makedirs(odir)
    save_graphs(odir + "graph.dgl", graph)
    


