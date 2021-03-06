import argparse
import json

parser = argparse.ArgumentParser()
parser.add_argument("--input", default="imagenet-induced-graph.json")
parser.add_argument("--output", default="imagenet-dense-grouped-graph.json")
args = parser.parse_args()

js = json.load(open(args.input, "r"))
wnids = js["wnids"]
vectors = js["vectors"]
edges = js["edges"]

n = len(wnids)
adjs = {}
for i in range(n):
    adjs[i] = []
for u, v in edges:
    adjs[u].append(v)

new_edges = [[] for i in range(99)]

for u, wnid in enumerate(wnids):
    q = [u]
    l = 0
    d = {}
    d[u] = 0
    while l < len(q):
        x = q[l]
        l += 1
        for y in adjs[x]:
            if d.get(y) is None:
                d[y] = d[x] + 1
                q.append(y)
    for x, dis in d.items():
        new_edges[dis].append((u, x))

while new_edges[-1] == []:
    new_edges.pop()

json.dump(
    {"wnids": wnids, "vectors": vectors, "edges_set": new_edges}, open(args.output, "w")
)
