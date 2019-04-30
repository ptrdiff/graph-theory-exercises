from math import log, sqrt

import networkx as nx

import utils


def degree_centrality(G):
    if len(G) <= 1:
        return {n: 1 for n in G}

    s = 1.0 / (len(G) - 1.0)
    centrality = {n: d * s for n, d in G.degree()}
    return centrality


def closeness_centrality(G):
    nodes = G.nodes()

    closeness_centrality = {}
    for n in nodes:
        sp = dict(utils.single_source_shortest_path_length(G, n))
        totsp = sum(sp.values())
        if totsp > 0.0 and len(G) > 1:
            closeness_centrality[n] = (len(sp) - 1.0) / totsp
            s = (len(sp) - 1.0) / (len(G) - 1)
            closeness_centrality[n] *= s
        else:
            closeness_centrality[n] = 0.0
    return closeness_centrality


def betweenness_centrality(G):
    betweenness = dict.fromkeys(G, 0.0)
    nodes = G.nodes()
    order = G.order()

    for s in nodes:
        S, P, sigma = utils.single_source_shortest_path_basic(G, s)
        betweenness = utils.accumulate_basic(betweenness, S, P, sigma, s)

    if order <= 2:
        scale = None
    else:
        scale = 1 / ((order - 1) * (order - 2))
        for v in betweenness:
            betweenness[v] *= scale
    return betweenness


def eigenvector_centrality(G, max_iter=100, tol=1.0e-6):
    nstart = {v: 1 for v in G}

    nstart_sum = sum(nstart.values())
    x = {k: v / nstart_sum for k, v in nstart.items()}
    nnodes = G.number_of_nodes()

    for i in range(max_iter):
        xlast = x
        x = xlast.copy()
        for n in x:
            for nbr in G[n]:
                x[nbr] += xlast[n]
        norm = sqrt(sum(z ** 2 for z in x.values())) or 1
        x = {k: v / norm for k, v in x.items()}
        if sum(abs(x[n] - xlast[n]) for n in x) < nnodes * tol:
            return x
    raise Exception("Iteration failed!")


def edge_betweenness(G):
    betweenness = dict.fromkeys(G, 0.0)
    betweenness.update(dict.fromkeys(G.edges(), 0.0))
    nodes = G.nodes()
    order = G.order()

    for s in nodes:
        S, P, sigma = utils.single_source_shortest_path_basic(G, s)
        betweenness = utils.accumulate_edges(betweenness, S, P, sigma, s)
    for n in G:
        del betweenness[n]

    if order <= 1:
        scale = None
    else:
        scale = 1 / (order * (order - 1))
        for v in betweenness:
            betweenness[v] *= scale
    return betweenness


if __name__ == "__main__":
    raw_data = nx.read_gexf("data/vkdata.gexf").to_undirected()
    graph = raw_data.subgraph(max(utils.connected_components(raw_data)))

    print('Degree centrality: {}'.format(degree_centrality(graph)))
    print('Closeness centrality: {}'.format(closeness_centrality(graph)))
    print('Betweenness centrality: {}'.format(betweenness_centrality(graph)))
    print('Eigenvector centrality: {}'.format(eigenvector_centrality(graph)))
    print('Edge betweenness: {}'.format(edge_betweenness(graph)))
