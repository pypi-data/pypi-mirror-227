#include <cassert>
#include <iostream>

#include "kernel.h"

using std::cout;
using std::endl;

typedef uint8_t level_t;


void print_bfs_summary(level_t* status, vid_t v_count)
{
    vid_t vid_count = 0;
    int l = 0;
    do {
        vid_count = 0;
        #pragma omp parallel for reduction (+:vid_count) 
        for (vid_t v = 0; v < v_count; ++v) {
            if (status[v] == l) {
                ++vid_count;
                /*if (l == 0) {
                    cerr << v << endl;
                }*/
            }
        }
        cout << " Level = " << l << " count = " << vid_count << endl;
        ++l;
    } while (vid_count !=0);
}

#define MAX_LEVEL 255
void run_bfs(graph_t& g, vid_t root)
{
    csr_t* csr = &g.csr;
    csr_t* csc = &g.csc;

	int		level      = 0;
	int		top_down   = 1;
	vid_t	frontier   = 0;
    vid_t   v_count    = csr->get_vcount();
    
    level_t* status = (level_t*)calloc(sizeof(level_t), v_count); 
    
    memset(status, 255, v_count*sizeof(level_t));
    
    status[root] = level;

    
	do {
		frontier = 0;
		#pragma omp parallel num_threads(THD_COUNT) reduction(+:frontier)
		{
            vid_t sid;
            int nebr_count = 0;
            vid_t* local_adjlist;
		    
            if (top_down) {
                #pragma omp for nowait
				for (vid_t v = 0; v < v_count; v++) {
					if (status[v] != level) continue;

                    nebr_count = csr->get_nebrs(v, local_adjlist);
                    for (int i = 0; i < nebr_count; ++i) {
                        sid = csr->get_vid(local_adjlist,i);
                        if (status[sid] == MAX_LEVEL) {
                            status[sid] = level + 1;
                            ++frontier;
                            //cout << " " << sid << endl;
                        }
                    }
				}
			} else {//bottom up
				#pragma omp for nowait
				for (vid_t v = 0; v < v_count; v++) {
					if (status[v] != MAX_LEVEL) continue;
                    
                    nebr_count = csc->get_nebrs(v, local_adjlist);
                    for (int i = 0; i < nebr_count; ++i) {
                        sid = csc->get_vid(local_adjlist,i);
                        if (status[sid] == level) {
                            status[v] = level + 1;
                            ++frontier;
                            break;
                        }
                    }
				}
		    }
        }
        //Point is to simulate bottom up bfs, and measure the trade-off    
		if (((frontier >= 0.002*v_count) /*|| level == 2*/)) {
			top_down = false;
		} else {
            top_down = true;
        }
		++level;
	} while (frontier);
		
    cout << "root = " << root << endl; 
    print_bfs_summary(status, v_count);
}
