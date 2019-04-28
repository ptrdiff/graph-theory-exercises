import collections
from math import log

import networkx as nx

import utils


def common_neighbors(G, u, v):
    return set(G[u]) & set(G[v])


def jaccard_coefficient(G, u, v):
    union_size = len(set(G[u]) | set(G[v]))
    if union_size == 0:
        return 0
    return len(set(G[u]) & set(G[v])) / union_size


def adamic_adar_index(G, u, v):
    return sum(1 / log(G.degree(w)) for w in set(G[u]) & set(G[v]))


def preferential_attachment(G, u, v):
    return G.degree(u) * G.degree(v)


if __name__ == "__main__":
    raw_data = nx.read_gexf("data/vkdata.gexf").to_undirected()
    graph = raw_data.subgraph(max(utils.connected_components(raw_data)))

    x, y = list(graph)[0], list(graph)[1]

    print(len(common_neighbors(graph, x, y)))
    print(jaccard_coefficient(graph, x, y))
    print(adamic_adar_index(graph, x, y))
    print(preferential_attachment(graph, x, y))
