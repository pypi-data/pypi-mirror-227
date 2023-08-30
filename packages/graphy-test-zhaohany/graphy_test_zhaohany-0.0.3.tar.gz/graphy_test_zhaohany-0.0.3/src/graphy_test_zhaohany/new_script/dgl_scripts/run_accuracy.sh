python3 GCN_dgl.py --gdir /mnt/huge_26TB/data/test2/cora/ --category 7
python3 GCN_dgl.py --gdir /mnt/huge_26TB/data/test2/citeseer/ --category 6
python3 GCN_dgl.py --gdir /mnt/huge_26TB/data/test2/pubmed/ --category 3
python3 GCN_dgl.py --gdir /mnt/huge_26TB/data/test2/reddit/ --category 41 --graph binary --feature binary
python3 GCN_dgl.py --gdir /mnt/huge_26TB/data/test2/ogb-product/ --category 47 --graph binary --feature binary

python3 GIN_dgl.py --gdir /mnt/huge_26TB/data/test2/cora/ --category 7
python3 GIN_dgl.py --gdir /mnt/huge_26TB/data/test2/citeseer/ --category 6
python3 GIN_dgl.py --gdir /mnt/huge_26TB/data/test2/pubmed/ --category 3
python3 GIN_dgl.py --gdir /mnt/huge_26TB/data/test2/reddit/ --category 41 --graph binary --feature binary
python3 GCN_dgl.py --gdir /mnt/huge_26TB/data/test2/ogb-product/ --category 47 --graph binary --feature binary

python3 GAT_dgl.py --gdir /mnt/huge_26TB/data/test2/cora/ --category 7
python3 GAT_dgl.py --gdir /mnt/huge_26TB/data/test2/citeseer/ --category 6
python3 GAT_dgl.py --gdir /mnt/huge_26TB/data/test2/pubmed/ --category 3
python3 GAT_dgl.py --gdir /mnt/huge_26TB/data/test2/reddit/ --category 41 --graph binary --feature binary
python3 GAT_dgl.py --gdir /mnt/huge_26TB/data/test2/ogb-product/ --category 47 --graph binary --feature binary

python3 GAT_dgl.py --gdir /mnt/huge_26TB/data/test2/cora/ --category 7 --head 3
python3 GAT_dgl.py --gdir /mnt/huge_26TB/data/test2/citeseer/ --category 6 --head 3
python3 GAT_dgl.py --gdir /mnt/huge_26TB/data/test2/pubmed/ --category 3 --head 3
python3 GAT_dgl.py --gdir /mnt/huge_26TB/data/test2/reddit/ --category 41 --graph binary --feature binary --head 3
python3 GAT_dgl.py --gdir /mnt/huge_26TB/data/test2/ogb-product/ --category 47 --graph binary  --feature binary --head 3
