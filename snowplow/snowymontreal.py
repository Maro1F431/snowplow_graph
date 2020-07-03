
import networkx as nx


def degree(node, adjList):
    deg_count = 0
    for pair in adjList:
        if node in pair[:2]:
            deg_count += 1
    return deg_count

def in_degree(node, adjList):
    deg_count = 0
    for pair in adjList:
        if node == pair[1]:
            deg_count += 1
    return deg_count

def out_degree(node, adjList):
    deg_count = 0
    for pair in adjList:
        if node == pair[0]:
            deg_count += 1
    return deg_count


# Undirected = MultiGraph
def solveNxUndir(g):
    # Store nodes having incidence degree that is odd
    nodesDegOdd = []
    for node, degree in g.degree():
        if degree % 2 == 1:
            nodesDegOdd.append(node)

    # Find shortest path between each nodes

    shortPathList = []

    for i in range(len(nodesDegOdd)):
        u = nodesDegOdd[i]
        for v in nodesDegOdd[i:]:
            elm = (nx.shortest_path(g, u, v, weight='weight'), -nx.shortest_path_length(g,u,v,weight='weight'))
            shortPathList.append(elm)


    # Make a graph of the odd nodes that links the nodes  by their shortest path
    #   each edge will have the shortest path as weight

    nG = nx.Graph()

    edgeToPath = {}

    for path in shortPathList:
        edge = (path[0][0], path[0][-1])
        otherEdge = (path[0][-1], path[0][0])
        edgeToPath[edge] = path[0]
        edgeToPath[otherEdge] = path[0]
        nG.add_edge(edge[0], edge[1], weight=path[1])

    # Do the MINIMAL matching weighted matching

    matching = nx.max_weight_matching(nG, True, weight='weight')

    # We have all the edges that represent the minimum paths

    for edge in matching:
        path = edgeToPath[edge]
        for i in range(len(path) - 1):
            src = path[i]
            dst = path[i + 1]
            weight = g.edges[src, dst, 0]['weight']
            g.add_edge(src, dst, weight=weight)

    # Find all paths using edges to add to the original graph for it to be an eulerian cycle

    it = nx.eulerian_circuit(g)
    edgeList = []
    for edge in it:
        edgeList.append(edge)
    return edgeList


#Directed
def solveNxDir(g):
    while (not nx.is_eulerian(g)):
       # Store nodes having incidence degree that is different from out degree
        nodesHigherOut = []
        nodesHigherIn = []
        for node in g.nodes():
            if (g.out_degree(node) > g.in_degree(node)):
                nodesHigherOut.append(node)
            elif (g.in_degree(node) > g.out_degree(node)):
                nodesHigherIn.append(node)

        # Find shortest path between each nodes

        shortPathList = []

        for src in nodesHigherIn:
            for dst in nodesHigherOut:
                elm = (nx.shortest_path(g, src, dst, weight='weight'), -nx.shortest_path_length(g,src,dst,weight='weight'))
                shortPathList.append(elm)


        # Make a graph of the odd nodes that links the nodes  by their shortest path
        #   each edge will have the shortest path as weight

        nG = nx.Graph()

        edgeToPath = {}

        for path in shortPathList:
            edge = (path[0][0], path[0][-1])
            edgeToPath[edge] = path[0]
            nG.add_edge(edge[0], edge[1], weight=path[1])

        # Do the MINIMAL matching weighted matching

        matching = nx.max_weight_matching(nG, True, weight='weight')

        # We have all the edges that represent the minimum paths

        for edge in matching:
            path = edgeToPath[edge]
            for i in range(len(path) - 1):
                src = path[i]
                dst = path[i + 1]
                weight = g.edges[src, dst, 0]['weight']
                g.add_edge(src, dst, weight=weight)

    # Find all paths using edges to add to the original graph for it to be an eulerian cycle

    it = nx.eulerian_circuit(g)
    edgeList = []
    for edge in it:
        edgeList.append(edge)
    return edgeList


def solve(is_oriented, num_vertices, edge_list):
    g = nx.MultiGraph()
    twoEdgeList = []

    for edge in edge_list:
        g.add_edge(edge[0], edge[1], weight=edge[2])
        twoEdgeList.append(edge[0], edge[1])

    if (not is_oriented):
        path = solveNxUndir(g)
    else:
        path = solveNxDir(g)

    for i in range(len(path)):
        path[i] = twoEdgeList.index(path[i])

    return path