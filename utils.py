def depth_first_search(graph, start=None):
    if start is None:
        start = list(graph)[0]

    visited_neighbours = set()
    neighbours_stack = [start]

    while neighbours_stack:
        neighbour = neighbours_stack.pop()
        if neighbour not in visited_neighbours:
            visited_neighbours.add(neighbour)
            neighbours_stack.extend(set(graph[neighbour]) - visited_neighbours)
    return visited_neighbours


def breath_first_search(graph, start=None):
    if start is None:
        start = list(graph)[0]

    visited_neighbours = set()
    neighbours_queue = [start]

    while neighbours_queue:
        neighbour = neighbours_queue.pop(0)
        if neighbour not in visited_neighbours:
            visited_neighbours.add(neighbour)
            neighbours_queue.extend(set(graph[neighbour]) - visited_neighbours)
    return visited_neighbours


def dfs_labeled_edges(G, source=None, depth_limit=None):
    if source is None:
        nodes = G
    else:
        nodes = [source]
    visited = set()
    if depth_limit is None:
        depth_limit = len(G)
    for start in nodes:
        if start in visited:
            continue
        yield start, start, 'forward'
        visited.add(start)
        stack = [(start, depth_limit, iter(G[start]))]
        while stack:
            parent, depth_now, children = stack[-1]
            try:
                child = next(children)
                if child in visited:
                    yield parent, child, 'nontree'
                else:
                    yield parent, child, 'forward'
                    visited.add(child)
                    if depth_now > 1:
                        stack.append((child, depth_now - 1, iter(G[child])))
            except StopIteration:
                stack.pop()
                if stack:
                    yield stack[-1][0], parent, 'reverse'
        yield start, start, 'reverse'


def dfs_preorder_nodes(G, source=None, depth_limit=None):
    edges = dfs_labeled_edges(G, source=source, depth_limit=depth_limit)
    return (v for u, v, d in edges if d == 'forward')


def dfs_postorder_nodes(G, source=None, depth_limit=None):
    edges = dfs_labeled_edges(G, source=source, depth_limit=depth_limit)
    return (v for u, v, d in edges if d == 'reverse')


def plain_bfs(G, source):
    Gsucc = G.succ
    Gpred = G.pred

    seen = set()
    nextlevel = {source}
    while nextlevel:
        thislevel = nextlevel
        nextlevel = set()
        for v in thislevel:
            if v not in seen:
                yield v
                seen.add(v)
                nextlevel.update(Gsucc[v])
                nextlevel.update(Gpred[v])


def connected_components(G):
    seen = set()
    for v in G:
        if v not in seen:
            c = set(plain_bfs(G, v))
            yield c
            seen.update(c)
