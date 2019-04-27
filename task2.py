import matplotlib.pyplot as plt
import networkx as nx
import collections

import utils


def connected_components(G):
    seen = set()
    for v in G:
        if v not in seen:
            c = set(utils.plain_bfs_undirected(G, v))
            yield c
            seen.update(c)


def draw_degree_density_hist(G):
    degree_sequence = sorted([d for n, d in G.degree()], reverse=True)
    degreeCount = collections.Counter(degree_sequence)
    deg, cnt = zip(*degreeCount.items())

    fig, ax = plt.subplots(figsize=(10, 6))
    plt.bar(deg, [x/G.order() for x in cnt], width=0.80, color='b')

    plt.title("Degree probability density histogram")
    plt.ylabel("Probability density")
    plt.xlabel("Degree")

    ax.set_xticks(deg)
    ax.set_xticklabels(deg)
    ax.set_yticks(list(set(x/G.order() for x in cnt)))

    return fig


def diameter(G, e=None):
    if e is None:
        e = utils.eccentricity(G)
    return max(e.values())


def periphery(G, e=None):
    if e is None:
        e = utils.eccentricity(G)
    diameter = max(e.values())
    p = [v for v in e if e[v] == diameter]
    return p


def radius(G, e=None):
    if e is None:
        e = utils.eccentricity(G)
    return min(e.values())


def center(G, e=None):
    if e is None:
        e = utils.eccentricity(G)
    radius = min(e.values())
    p = [v for v in e if e[v] == radius]
    return p


def average_shortest_path_length(G):
    n = G.order()

    s = sum(l for u in G for l in
            utils.single_source_shortest_path_length(G, u).values())
    return s / (n * (n - 1))


if __name__ == "__main__":
    raw_data = nx.read_gexf("data/vkdata.gexf").to_undirected()
    graph = raw_data.subgraph(max(connected_components(raw_data)))

    fig = draw_degree_density_hist(graph)
    fig.savefig("hist.png")
    plt.show()

    degree_sequence = sorted([d for n, d in graph.degree()], reverse=True)
    print('Average degree of vertices: {}'
          .format(sum(degree_sequence)/len(degree_sequence)))

    print('Diameter of the graph: {}'.format(diameter(graph)))

    print('Radius of the graph: {}'.format(radius(graph)))

    print('Central vertices of the graph: {}'.format(center(graph)))

    print('Peripheral vertices of the graph: {}'.format(periphery(graph)))

    print('Average path length in the graph: {}'
          .format(average_shortest_path_length(graph)))
