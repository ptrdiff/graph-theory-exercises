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
        depth_limit = G.order()
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


def plain_bfs_directed(G, source):
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


def plain_bfs_undirected(G, source):
    G_adj = G.adj
    seen = set()
    nextlevel = {source}
    while nextlevel:
        thislevel = nextlevel
        nextlevel = set()
        for v in thislevel:
            if v not in seen:
                yield v
                seen.add(v)
                nextlevel.update(G_adj[v])


def connected_components(G):
    seen = set()
    for v in G:
        if v not in seen:
            c = set(plain_bfs_undirected(G, v))
            yield c
            seen.update(c)


def single_source_shortest_path_length(G, source):
    nextlevel = {source: 1}
    return dict(single_shortest_path_length(G.adj, nextlevel))


def single_shortest_path_length(adj, firstlevel):
    seen = {}
    level = 0
    nextlevel = firstlevel

    while nextlevel:
        thislevel = nextlevel
        nextlevel = {}
        for v in thislevel:
            if v not in seen:
                seen[v] = level
                nextlevel.update(adj[v])
                yield (v, level)
        level += 1
    del seen


def eccentricity(G, v=None, sp=None):
    e = {}
    for n in G.nbunch_iter(v):
        if sp is None:
            length = single_source_shortest_path_length(G, n)
        else:
            length = sp[n]

        e[n] = max(length.values())

    if v in G:
        return e[v]
    else:
        return e


def single_source_shortest_path_basic(G, s):
    S = []
    P = {}
    for v in G:
        P[v] = []
    sigma = dict.fromkeys(G, 0.0)
    D = {}
    sigma[s] = 1.0
    D[s] = 0
    Q = [s]
    while Q:
        v = Q.pop(0)
        S.append(v)
        Dv = D[v]
        sigmav = sigma[v]
        for w in G[v]:
            if w not in D:
                Q.append(w)
                D[w] = Dv + 1
            if D[w] == Dv + 1:
                sigma[w] += sigmav
                P[w].append(v)
    return S, P, sigma


def accumulate_edges(betweenness, S, P, sigma, s):
    delta = dict.fromkeys(S, 0)
    while S:
        w = S.pop()
        coeff = (1 + delta[w]) / sigma[w]
        for v in P[w]:
            c = sigma[v] * coeff
            if (v, w) not in betweenness:
                betweenness[(w, v)] += c
            else:
                betweenness[(v, w)] += c
            delta[v] += c
        if w != s:
            betweenness[w] += delta[w]
    return betweenness


def accumulate_basic(betweenness, S, P, sigma, s):
    delta = dict.fromkeys(S, 0)
    while S:
        w = S.pop()
        coeff = (1 + delta[w]) / sigma[w]
        for v in P[w]:
            delta[v] += sigma[v] * coeff
        if w != s:
            betweenness[w] += delta[w]
    return betweenness
