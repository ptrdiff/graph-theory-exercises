import collections
import csv
from math import log

import networkx as nx

import utils


def common_neighbors(G, u, v):
    return len(set(G[u]) & set(G[v]))


def jaccard_coefficient(G, u, v):
    union_size = len(set(G[u]) | set(G[v]))
    if union_size == 0:
        return 0
    return len(set(G[u]) & set(G[v])) / union_size


def adamic_adar_index(G, u, v):
    return sum(1 / log(G.degree(w)) for w in set(G[u]) & set(G[v]))


def preferential_attachment(G, u, v):
    return G.degree(u) * G.degree(v)


def print_result_csv(G, filename, function):
    with open(filename, mode='w') as tmp_file:
        tmp_file = csv.writer(tmp_file, delimiter=',',
                              quotechar='"', quoting=csv.QUOTE_MINIMAL)
        tmp_file.writerow([None] + list(G.nodes))
        for x in G.nodes:
            tmp_file.writerow([x] + [function(graph, x, y)if x is not y
                                     else '' for y in G.nodes])


if __name__ == "__main__":
    raw_data = nx.read_gexf("data/vkdata.gexf").to_undirected()
    graph = raw_data.subgraph(max(utils.connected_components(raw_data)))

    x, y = list(graph)[0], list(graph)[1]

    print('Common neighbors measure for {} and {}: {}'
          .format(x, y, common_neighbors(graph, x, y)))
    print('Jaccard\'s coefficient measure for {} and {}: {}'
          .format(x, y, jaccard_coefficient(graph, x, y)))
    print('Adamic adar index measure for {} and {}: {}'
          .format(x, y, adamic_adar_index(graph, x, y)))
    print('Preferential attachment measure for {} and {}: {}'
          .format(x, y, preferential_attachment(graph, x, y)))

    print_result_csv(graph, 'common_neighbors.csv', common_neighbors)
    print_result_csv(graph, 'jaccard_coefficient.csv', jaccard_coefficient)
    print_result_csv(graph, 'adamic_adar_index.csv', adamic_adar_index)
    print_result_csv(graph, 'preferential_attachment.csv',
                     preferential_attachment)
