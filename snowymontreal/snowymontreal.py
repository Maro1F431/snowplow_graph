import osmnx as ox
import networkx as nx
import csv
from itertools import combinations, product

def eulerize_directed_weighted(G):
    '''
    Turn directed graph into eulerian graph, using the length of the edges as
    weights
    '''
    nodesHigherOut = []
    nodesHigherIn = []
    for node in G.nodes():
        if (G.out_degree(node) > G.in_degree(node)):
            nodesHigherOut.append(node)
        elif (G.in_degree(node) > G.out_degree(node)):
            nodesHigherIn.append(node)

    G = nx.MultiDiGraph(G)
    if len(nodesHigherIn) == 0:
        return G

    # get all shortest paths between vertices that are not symmetric
    pathList = [(m,
                    {n: nx.shortest_path(G, source=m, target=n, weight='length')}, n)
                for m, n in product(nodesHigherIn, nodesHigherOut)]

    while nodesHigherIn != []:
        # use sum of weights as weight in a new graph
        # store the paths in the graph for easy indexing later
        Gp = nx.Graph()
        for n, Ps, lol in pathList:
            for m, P in Ps.items():
                weight = 0
                for i in range(len(P) - 1):
                    weight += G.edges[P[i], P[i + 1], 0]['length']
                if n != m:
                    Gp.add_edge(m, n, weight=1/(1 + weight), path=P)

        # find the minimum weight matching of edges in the weighted graph
        best_matching = nx.Graph(list(nx.max_weight_matching(Gp)))

        # duplicate each edge along each path in the set of paths in Gp
        # delete from the list of nodes if the node is now symmetric
        for m, n in best_matching.edges():
            if not m in nodesHigherIn:
                n, m = m, n
            path = Gp[m][n]["path"]
            G.add_edges_from(nx.utils.pairwise(path))
            if G.in_degree(n) == G.out_degree(n):
                nodesHigherOut.remove(n)
                pathList = [q for q in pathList if q[2] != n]
            if G.in_degree(m) == G.out_degree(m):
                nodesHigherIn.remove(m)
                pathList = [q for q in pathList if q[0] != m]
    return G


def montreal_snow_path(district, is_directed):
    # Download graph of district from OSM
    graph = ox.graph_from_place(district + ", Montreal, Canada",
                                network_type='drive', truncate_by_edge=True)

    # Get largest component so that the graph is strongly connected
    graph = ox.utils_graph.get_largest_component(graph, strongly=True)

    # Project the graph and merge intersections that are close to better analyze
    g_proj = ox.project_graph(graph)
    # graph_cons = ox.consolidate_intersections(g_proj, tolerance=10, rebuild_graph=True)

    # Transform the graph into an eulerian graph

    if (not is_directed):
        result = g_proj.to_undirected(g_proj)
        result = nx.eulerize(result)
    else:
        result = eulerize_directed_weighted(g_proj)

    # Find an eulerian circuit, and build the list of tuples 'latitude',
    #                                                        'longitude'

    it = nx.eulerian_circuit(result)
    coordList = []
    i = 0
    for edge in it:
        if i == 0:
            coordList.append((g_proj.nodes[edge[0]]['lat'],
                            g_proj.nodes[edge[0]]['lon']))
        coordList.append((g_proj.nodes[edge[1]]['lat'],
                        g_proj.nodes[edge[1]]['lon']))
        i += 1

    with open(district + '.csv', 'w') as file:
        writer = csv.writer(file)

        writer.writerow(["Index", "Latitude", "Longitude"])
        i = 0
        for lat, lon in coordList:
            writer.writerow([i, lat, lon])
            i += 1

    return len(coordList)


# Graph class useful for our algorithms

class Graph():
    def __init__(self, nb_vertex, edges, directed):
        self.nb_vertex = nb_vertex
        self.edges = edges
        self.directed = directed
        self.adj_mat = self.__build_min_weight_adj_mat()

    def degree(self, node):
        deg_count = 0
        for pair in self.edges:
            if node in pair[:2]:
                deg_count += 1
        return deg_count

    def in_degree(self, node):
        deg_count = 0
        for pair in self.edges:
            if node == pair[1]:
                deg_count += 1
        return deg_count

    def out_degree(self, node):
        deg_count = 0
        for pair in self.edges:
            if node == pair[0]:
                deg_count += 1
        return deg_count

    def __build_min_weight_adj_mat(self):
        adj = [[float('inf') for col in range (self.nb_vertex)] for row in range(self.nb_vertex)]
        for edge in self.edges:
            src = edge[0]
            dst = edge[1]
            weight = min(adj[src][dst], edge[2])
            adj[src][dst] = weight
            if (not self.directed):
                adj[src][dst] = weight
        return adj

    def __smallest_not_visited(self, not_visited, dist_list):
        min = not_visited[0]
        for node in not_visited:
            if (dist_list[node] < min):
                min = node
        return min

    def shortest_path(self, src, dst):
        dist_list = [float('inf') for i in range(self.nb_vertex)]
        dist_list[src] = 0
        previous = [-float('inf') for i in range(self.nb_vertex)]
        not_visited = [i for i in range(self.nb_vertex)]
        while (len(not_visited) != 0):
            u = self.__smallest_not_visited(not_visited, dist_list)
            if (u == dst):
                break
            not_visited.remove(u)
            for v in range(len(self.adj_mat[u])):
                dist = dist_list[u] + self.adj_mat[u][v]
                if (dist < dist_list[v]):
                    dist_list[v] = dist
                    previous[v] = u
        shortest_path = []
        u = dst
        while (previous[u] != -float('inf')):
            shortest_path.insert(0, u)
            u = previous[u]
        shortest_path.insert(0, src)
        return shortest_path

# Function that solves

def solve(is_oriented, num_vertices, edge_list):
    g = nx.MultiGraph()
    if (is_oriented):
        g = nx.MultiDiGraph()
    twoEdgeList = []

    for edge in edge_list:
        g.add_edge(edge[0], edge[1], length=edge[2])
        pair = (edge[0], edge[1])
        twoEdgeList.append(pair)

    if (not is_oriented):
        g = nx.eulerize(g)
    else:
        g = eulerize_directed_weighted(g)

    it = nx.eulerian_path(g)
    path = []
    for edge in it:
        path.append(edge)

    if not is_oriented:
        for i in range(len(path)):
            if path[i] in twoEdgeList:
                path[i] = twoEdgeList.index(path[i])
            else:
                path[i] = twoEdgeList.index((path[i][1], path[i][0]))
    else:
        for i in range(len(path)):
            path[i] = twoEdgeList.index(path[i])

    return path