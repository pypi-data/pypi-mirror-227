#python3 GCN_graphpy.py --gdir /mnt/huge_26TB/data/test2/cora/ --category 7 --graph binary
#python3 GCN_graphpy.py --gdir /mnt/huge_26TB/data/test2/citeseer/ --category 6 --graph binary
#python3 GCN_graphpy.py --gdir /mnt/huge_26TB/data/test2/pubmed/ --category 3 --graph binary
#python3 GCN_graphpy.py --gdir /mnt/huge_26TB/data/test2/reddit/ --category 41 --graph binary --feature binary
#python3 GCN_graphpy.py --gdir /mnt/huge_26TB/data/test2/ogb-product/ --category 47 --graph binary --feature binary

python3 GAT_graphpy.py --gdir /mnt/huge_26TB/data/test2/cora/ --category 7 --graph binary  >> temp1.txt
python3 GAT_graphpy.py --gdir /mnt/huge_26TB/data/test2/citeseer/ --category 6 --graph binary >> temp1.txt
python3 GAT_graphpy.py --gdir /mnt/huge_26TB/data/test2/pubmed/ --category 3 --graph binary  >> temp1.txt
python3 GAT_graphpy.py --gdir /mnt/huge_26TB/data/test2/reddit/ --category 41 --graph binary --feature binary  >> temp1.txt
python3 GAT_graphpy.py --gdir /mnt/huge_26TB/data/test2/ogb-product/ --category 47 --graph binary --feature binary  >> temp1.txt
