#pragma once


#include <stdio.h>
#include "stdint.h"
using namespace std;

#define bit_shift2 16
//For tiles in a physical group
#define p_p 256 
#define bit_shift3 8 
//For physical group count in the graph
#define bit_shift1 24 
#define part_mask1 (-1UL << bit_shift1)
#define part_mask1_2 ~(part_mask1) 

#ifdef B64
typedef uint64_t vid_t;
#elif B32
typedef uint32_t vid_t;
#endif

typedef union __univeral_type {
    vid_t    value_int;

#ifdef B32   
    float    value_float;
#else     
    double   value_float;
    double   value_double;
#endif
}univ_t;

enum enumGraph {
    eCSR = 0,
    eSNB = 1,
    eCreateCOO = 2,
    eReorderEID = 4
};

typedef uint16_t word_t;
struct snb_t {
    word_t src;
    word_t dst;
};

union dst_id_t {
    vid_t sid;
    snb_t snb; 
};

//First can be nebr sid, while the second could be edge id/property
template <class T>
class dst_weight_t {
 public:
    dst_id_t first;
    T        second;
};
/*
template <class T>
inline vid_t get_vid( T* dst) {
    return dst->first.sid;
}


template <>
inline vid_t get_vid<dst_id_t>(dst_id_t* dst) {
    return dst->sid;
}

template <class T>
inline vid_t get_eid( T* dst) {
    return dst->second.value_int;
}

template <>
inline vid_t get_eid<dst_id_t>(dst_id_t* dst) {
    assert(0);
    return 0;
}
*/
typedef dst_weight_t<univ_t> weight_sid_t;

class csr_t {
 public:
    vid_t  actual_vcount; //This is actual vcount in a graph 
    vid_t  e_count;
    vid_t  dst_size;
    vid_t  v_count; //This is SNB tile count, otherwise same as actual vcount
    vid_t* offset;
    char* nebrs;
    union {
        int*  degrees;
        float* n_degree;
    };
    int64_t flag;

 public:
    csr_t() {};
    void init(vid_t a_vcount, vid_t a_dstsize, void* a_offset, void* a_nebrs, int64_t a_flag, vid_t edge_count) {
        v_count = a_vcount;
        dst_size = a_dstsize;
        offset = (vid_t*)a_offset;
        nebrs = (char*)a_nebrs;
        e_count = offset[edge_count];
        //degrees = 0;
        actual_vcount = v_count;//for csr
        flag = a_flag;

    }
    vid_t get_vcount() {
        return actual_vcount;
    }
    void set_vcount(vid_t a_actual_vcount) {
        actual_vcount = a_actual_vcount;
    }
    vid_t get_ecount() {
        return e_count;
    }
    vid_t get_degree(vid_t index) {
        return offset[index + 1] - offset[index];
    }

    vid_t get_first_eid(vid_t index) {
        return offset[index];
    }

    vid_t get_nebrs(vid_t v, vid_t*& ptr) {
        vid_t degree = offset[v+1] - offset[v];
        ptr = (vid_t*)(nebrs + offset[v]*dst_size);
        return degree; 
    }

    vid_t get_vid(vid_t* header, vid_t index) {
        vid_t* h = (vid_t*)((char*)header + index*dst_size);
        return *h;
    }

    vid_t get_eid(vid_t* header, vid_t index) {
        assert(dst_size > sizeof(vid_t));
        weight_sid_t* h = (weight_sid_t*)((char*)header + index*dst_size);
        return h->second.value_int;
    }
    
    snb_t get_snb(vid_t* header, vid_t index) {
        snb_t* h = (snb_t*)((char*)header + index*dst_size);
        return *h;
    }

};

class edge_t {
 public:
     vid_t src;
     vid_t dst;
     //edge properties here if any.
};

class coo_t {
 public:
     edge_t* edges;
     vid_t dst_size;
     vid_t v_count;
     vid_t e_count;
     coo_t() {
         edges = 0;
         dst_size = 0;
         v_count = 0;
         e_count = 0;
     }
     void init(vid_t a_vcount, vid_t a_dstsize, vid_t a_ecount, edge_t* a_edges) {
         v_count = a_vcount;
         e_count = a_ecount;
         dst_size = a_dstsize;
         edges = a_edges;
     }
};

class graph_t {
 public:
    csr_t csr;
    csr_t csc;
    coo_t coo;
 public:
    void save_graph(const string& full_path) {
        if (csr.dst_size == sizeof(vid_t)) { //no eid case
            return save_graph_noeid(full_path);
        } else {
            return save_graph_eid(full_path);
        }
    }
    void save_graph_eid(const string& full_path) {
        string file_name;
        string name;
        FILE* fname;

        name = full_path + "_csr.offset";
        fname = fopen(name.c_str(), "wb");
        fwrite(csr.offset, sizeof(vid_t), csr.actual_vcount+1, fname);
        fclose(fname);
        
        name = full_path + "_csr.nebrs";
        fname = fopen(name.c_str(), "wb");
        fwrite(csr.nebrs, csr.dst_size, csr.e_count, fname);
        fclose(fname);
        
        name = full_path + "_csc.offset";
        fname = fopen(name.c_str(), "wb");
        fwrite(csc.offset, sizeof(vid_t), csc.actual_vcount+1, fname);
        fclose(fname);
        
        name = full_path + "_csc.nebrs";
        fname = fopen(name.c_str(), "wb");
        fwrite(csc.nebrs, csc.dst_size, csc.e_count, fname);
        fclose(fname);
        
        name = full_path + "_coo.edge";
        fname = fopen(name.c_str(), "wb");
        fwrite(coo.edges, sizeof(edge_t), coo.e_count, fname);
        fclose(fname);

        name = full_path + "_graph.info";
        fname = fopen(name.c_str(), "w");
        
        int64_t direction = 1;//directed
        #ifdef B32
        fprintf(fname, "v_count=%u\n e_count=%u\n dst_size=%u\n direction=%lu", csc.v_count, csc.e_count, csc.dst_size, direction);
        #else
        fprintf(fname, "v_count=%lu\n e_count=%lu\n dst_size=%lu\n direction=%lu", csc.v_count, csc.e_count, csc.dst_size, direction);
        #endif
        fclose(fname);
    }
    void save_graph_noeid(const string& full_path) {
        string file_name;
        string name;
        FILE* fname;

        name = full_path + "_csr_noeid.offset";
        fname = fopen(name.c_str(), "wb");
        fwrite(csr.offset, sizeof(vid_t), csr.actual_vcount+1, fname);
        fclose(fname);
        
        name = full_path + "_csr_noeid.nebrs";
        fname = fopen(name.c_str(), "wb");
        fwrite(csr.nebrs, csr.dst_size, csr.e_count, fname);
        fclose(fname);
        
        if (csc.nebrs == csr.nebrs) {//undirected graph
            name = full_path + "_graph_noeid.info";
            fname = fopen(name.c_str(), "w");
            int64_t direction = 0;
            #ifdef B32
            fprintf(fname, "v_count=%u\n e_count=%u\n dst_size=%u\n direction=%lu", csc.v_count, csc.e_count, csc.dst_size, direction);
            #else
            fprintf(fname, "v_count=%lu\n e_count=%lu\n dst_size=%lu\n direction=%lu", csc.v_count, csc.e_count, csc.dst_size, direction);
            #endif
            fclose(fname);
            return;
        }
        name = full_path + "_csc_noeid.offset";
        fname = fopen(name.c_str(), "wb");
        fwrite(csc.offset, sizeof(vid_t), csc.actual_vcount+1, fname);
        fclose(fname);
        
        name = full_path + "_csc_noeid.nebrs";
        fname = fopen(name.c_str(), "wb");
        fwrite(csc.nebrs, csc.dst_size, csc.e_count, fname);
        fclose(fname);
        
        name = full_path + "_graph_noeid.info";
        fname = fopen(name.c_str(), "w");
        int64_t direction = 1;
        #ifdef B32
        fprintf(fname, "v_count=%u\n e_count=%u\n dst_size=%u\n direction=%lu", csc.v_count, csc.e_count, csc.dst_size, direction);
        #else
        fprintf(fname, "v_count=%lu\n e_count=%lu\n dst_size=%lu\n direction=%lu", csc.v_count, csc.e_count, csc.dst_size, direction);
        #endif
        fclose(fname);
    }
    void load_graph_noeid(const string& full_path) {
        string file_name;
        string name;
        FILE* fname;
        vid_t  v_count = 0;
        vid_t  e_count = 0;
        vid_t dst_size = 0;
        vid_t*  offset = 0;
        char*    nebrs = 0;
        int64_t   flag = 0;
        int64_t   direction = 0;
        
        name = full_path + "_graph_noeid.info";
        fname = fopen(name.c_str(), "r");
        #ifdef B32
        fscanf(fname, "v_count=%u\n e_count=%u\n dst_size=%u\n direction=%lu\n", &v_count, &e_count, &dst_size, &direction);
        #else
        fscanf(fname, "v_count=%lu\n e_count=%lu\n dst_size=%lu\n direction=%lu\n", &v_count, &e_count, &dst_size, &direction);
        #endif
        fclose(fname);

        if (dst_size != sizeof(vid_t)) {
            cout << "Trying to Load Wrong Graph. Aboring" << endl;
            exit(1);
        }

        offset = (vid_t*)calloc(sizeof(vid_t), v_count + 1);
        nebrs = (char*)calloc(dst_size, e_count);
        name = full_path + "_csr_noeid.offset";
        fname = fopen(name.c_str(), "rb");
        fread(offset, sizeof(vid_t), v_count+1, fname);
        fclose(fname);
        
        name = full_path + "_csr_noeid.nebrs";
        fname = fopen(name.c_str(), "rb");
        fread(nebrs, dst_size, e_count, fname);
        fclose(fname);
        
        csr.init(v_count, dst_size, offset, nebrs, flag, v_count);
        
        if (direction == 0) {//undirected
            csc.init(v_count, dst_size, offset, nebrs, flag, v_count);
            return;
        }

        offset = (vid_t*)calloc(sizeof(vid_t), v_count + 1);
        nebrs = (char*)calloc(dst_size, e_count);
        name = full_path + "_csc_noeid.offset";
        fname = fopen(name.c_str(), "rb");
        fread(offset, sizeof(vid_t), v_count+1, fname);
        fclose(fname);
        
        name = full_path + "_csc_noeid.nebrs";
        fname = fopen(name.c_str(), "rb");
        fread(nebrs, dst_size, e_count, fname);
        fclose(fname);

        csc.init(v_count, dst_size, offset, nebrs, flag, v_count);
    }
    void load_graph(const string& full_path) {
        string file_name;
        string name;
        FILE* fname;
        vid_t  v_count = 0;
        vid_t  e_count = 0;
        vid_t dst_size = 0;
        vid_t*  offset = 0;
        char*    nebrs = 0;
        int64_t   flag = 0;
        int64_t   direction = 0;
        
        name = full_path + "_graph.info";
        fname = fopen(name.c_str(), "r");
        #ifdef B32
        fscanf(fname, "v_count=%u\n e_count=%u\n dst_size=%u\n direction=%lu\n", &v_count, &e_count, &dst_size, &direction);
        #else
        fscanf(fname, "v_count=%lu\n e_count=%lu\n dst_size=%lu\n direction=%lu\n", &v_count, &e_count, &dst_size, &direction);
        #endif
        fclose(fname);

        if (dst_size == sizeof(vid_t)) {
            cout << "Trying to Load Wrong Graph. Aboring" << endl;
            exit(1);
        }

        offset = (vid_t*)calloc(sizeof(vid_t), v_count + 1);
        nebrs = (char*)calloc(dst_size, e_count);
        name = full_path + "_csr.offset";
        fname = fopen(name.c_str(), "rb");
        fread(offset, sizeof(vid_t), v_count+1, fname);
        fclose(fname);
        
        name = full_path + "_csr.nebrs";
        fname = fopen(name.c_str(), "rb");
        fread(nebrs, dst_size, e_count, fname);
        fclose(fname);
        csr.init(v_count, dst_size, offset, nebrs, flag, v_count);
        
        offset = (vid_t*)calloc(sizeof(vid_t), v_count + 1);
        nebrs = (char*)calloc(dst_size, e_count);
        name = full_path + "_csc.offset";
        fname = fopen(name.c_str(), "rb");
        fread(offset, sizeof(vid_t), v_count+1, fname);
        fclose(fname);
        
        name = full_path + "_csc.nebrs";
        fname = fopen(name.c_str(), "rb");
        fread(nebrs, dst_size, e_count, fname);
        fclose(fname);
        csc.init(v_count, dst_size, offset, nebrs, flag, v_count);
        
        name = full_path + "_coo.edge";
        fname = fopen(name.c_str(), "rb");
        fwrite(coo.edges, sizeof(edge_t), e_count, fname);
        fclose(fname);
        coo.init(v_count, dst_size, e_count, coo.edges);

    }

    void init(vid_t a_vcount, vid_t a_dstsize, void* a_offset, void* a_nebrs, void* a_offset1, void* a_nebrs1, int64_t flag, int64_t num_vcount) {
        csr.init(num_vcount, a_dstsize, a_offset, a_nebrs, flag, a_vcount);
        csc.init(num_vcount, a_dstsize, a_offset1, a_nebrs1, flag, a_vcount);

        if(csr.flag == eSNB) {
            int* degree = (int*)calloc(sizeof(int), num_vcount);
            csr.degrees = degree;
            csc.degrees = degree;

            vid_t nebr_count = 0;
            vid_t* header; 
            vid_t index = 0, m, n, offset;
            snb_t snb;
            vid_t p = (csr.v_count >> bit_shift1) + (0 != (csr.get_vcount() & part_mask1_2));
            for (vid_t i = 0; i < p; ++i) {
                for (vid_t j = 0; j < p; ++j) {
                    offset = ((i*p + j) << bit_shift2); 
                    for (vid_t s_i = 0; s_i < p_p; s_i++) {
                        for (vid_t s_j = 0; s_j < p_p; s_j++) {

                            index = offset + ((s_i << bit_shift3) + s_j);
                            m = ((i << bit_shift3) + s_i) << bit_shift2;
                            n = ((j << bit_shift3) + s_j) << bit_shift2; 
                            
                            nebr_count = csr.get_nebrs(index, header);
                            if (0 == nebr_count) continue;
                            for (vid_t e = 0; e < nebr_count; ++e) {
                                // dst = csr.next(header);
                                snb = csr.get_snb(header, e);
                                ++degree[m+snb.src];
                                //cout<<"degree"<<degree[m+snb.src]<<endl;
                            }
                        }
                    }
                }
            }
        } else { //rearrange CSR eid. Works 5%-10%. comment it out later. TODO
        //better use some flag to dictate it.
         
        if (a_dstsize == sizeof(vid_t)) { //useful for GCN only
            float* n_degree = (float*)malloc(a_vcount*sizeof(float));
            #pragma omp parallel for
            for (vid_t u = 0; u < a_vcount; u++) {
                vid_t degree = csr.get_degree(u);
                if(degree > 1) {
                    n_degree[u] = 1.0f/degree;
                } else {
                    n_degree[u] = 1.0f;
                }
                //printf("%d %f \n",degree, n_degree[u]);
            }
            csr.n_degree = n_degree;
            csc.n_degree = n_degree;
        } 
        if (a_dstsize != sizeof(vid_t) +sizeof(vid_t)) {
                return;
        }

        //rearrange CSR eid. Works 5%-10%. comment it out later. TODO
        //Let us also generate coo format.
        coo.v_count = a_vcount;
        coo.dst_size = a_dstsize;
        coo.e_count = 0;
        coo.edges  = 0;

        
        coo.e_count = csr.get_ecount();
        coo.edges = (edge_t*)malloc(csr.get_ecount()*sizeof(edge_t));
        #pragma omp parallel
        {
            vid_t sid, eid, old_eid;
            vid_t nebr_count, dst_nebr_count;
            vid_t* nebrs;
            vid_t* dst_nebrs;
            #pragma omp for
            for (vid_t u = 0; u < a_vcount; u++) {
                nebr_count = csc.get_nebrs(u, nebrs);
                eid = csc.get_first_eid(u);

                for (vid_t i = 0; i <  nebr_count; i++) {
                    sid = *nebrs; ++nebrs;
                    old_eid = *nebrs;

                    //assign new eid
                    //*nebrs = eid;//b
                    ++nebrs;
                    
                    eid = old_eid;//a
                    //Find and edit the eid of csr.//b
                    /*dst_nebr_count = csr.get_nebrs(sid, dst_nebrs);
                    for (vid_t j = 0; j < dst_nebr_count; ++j) {
                        ++dst_nebrs;
                        if (old_eid == *dst_nebrs) {
                            *dst_nebrs = eid;
                            break;
                        }
                        ++dst_nebrs;
                    }*/
                    
                    //let us generate coo.
                    coo.edges[eid].src = sid;
                    coo.edges[eid].dst = u;
                    
                    ++eid;
                }
            }
        }

        }
    }

    void set_vcount(vid_t a_actual_vcount){
        csr.set_vcount(a_actual_vcount);
        csc.set_vcount(a_actual_vcount);
    }
    vid_t get_vcount() {
        return csr.actual_vcount;
    }
    vid_t get_edge_count() {
        return csr.e_count;
    }
};

