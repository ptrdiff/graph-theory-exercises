import networkx as nx
import utils


def strongly_connected_components(G, source=None):
    post = list(utils.dfs_postorder_nodes(G.reverse(copy=False),
                                          source=source))

    seen = {}
    while post:
        r = post.pop()
        if r not in seen:
            c = utils.dfs_preorder_nodes(G, r)
            new = [v for v in c if v not in seen]
            seen.update([(u, True) for u in new])
            yield new


def is_strongly_connected(G):
    return len(list(strongly_connected_components(G))[0]) == len(G)


def number_strongly_connected_components(G):
    return sum(1 for scc in strongly_connected_components(G))


def weakly_connected_components(G):
    seen = set()
    for v in G:
        if v not in seen:
            c = set(utils.plain_bfs_directed(G, v))
            yield c
            seen.update(c)


def is_weakly_connected(G):
    return len(list(weakly_connected_components(G))[0]) == len(G)


def number_weakly_connected_components(G):
    return sum(1 for wcc in weakly_connected_components(G))


def percentage_nodes_largest_weakly_connected_component(G):
    return (len(max(weakly_connected_components(graph))) / len(graph)) * 100


if __name__ == "__main__":
    graph = nx.read_gexf("vkdata.gexf")

    print('Is graph strongly connected: {}'
          .format(is_strongly_connected(graph)))
    print('Is graph weakly connected: {}'
          .format(is_weakly_connected(graph)))

    print('Number of strongly connected components: {}'
          .format(number_strongly_connected_components(graph)))
    print('Number of weakly connected components: {}'
          .format(number_weakly_connected_components(graph)))

    print('Size of all strongly connected components: {}'
          .format([len(v) for v in strongly_connected_components(graph)]))
    print('Size of all weakly connected components: {}'
          .format([len(v) for v in weakly_connected_components(graph)]))

    print('Percentage of largest weakly connected component: {}'
          .format(percentage_nodes_largest_weakly_connected_component(graph)))
