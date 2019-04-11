from random import randint

class FlowNetwork:
    """
    Flow-Network data structure.
    """

    def __init__(self):
        """
        Generates a flow network.
        """
        self.adjacent = {}
        self.capacity = {}
        self.flow = {}


    def getCapacity(self, edge):
        """
        Returns edge's capacity.
        """
        return self.capacity.get(edge, 0)


    def getFlow(self, edge):
        """
        Returns edge's flow.
        """
        return self.flow.get(edge,  0)


    def getFlowAcrossVertex(self, vertex):
        """
        Returns the flow crossing vertex
        """
        return sum(self.getFlow((vertex, toVertex)) for toVertex in self.adjacent[vertex]) 


    def getResidualCapacity(self, edge):
        """
        Returns edge's residual capacity.
        """
        return self.getCapacity(edge) - self.getFlow(edge)


    def setFlow(self, edge, value):
        """
        Sets edge's flow to value.
        """
        self.flow[edge] = value
        self.flow[edge[::-1]] = - value


    def increaseFlow(self, edge, value):
        """
        Increases edge's flow value units.
        """
        self.flow[edge] += value
        self.flow[edge[::-1]] -= value


    def vertices(self):
        """
        Returns the set of vertices in the network.
        """
        return self.adjacent.keys()


    def edges(self):
        """
        Returns the set of edges in the network.
        """
        return self.capacity.keys()


    def neighbors(self, u):
        """
        Returns the vertices adjacent to u in the network.
        """
        return filter(lambda v: self.getCapacity((u,v)) > 0, self.adjacent[u])


    def residualNeighbors(self, u):
        """
        Returns the vertices adjacent to u in the resigual network.
        """
        return filter(lambda v: self.getResidualCapacity((u,v)) > 0, self.adjacent[u])


    def loadNetworkFromFile(self, file):
        """
        Loads a flow network from a file containing a list of edges
        of the form: fromVertex, toVertex, capacity
        """
        for line in open(file, 'r'):
            fromVertex, toVertex, capacity = map(int, line.split())
            self.addEdge(fromVertex, toVertex, capacity)


    def randomNetwork(self, numVertices, numEdges, capacityRange):
        """
        Generates a random flow network with the given parameters.
        """
        for _ in range(numEdges):
            fromVertex, toVertex = None, None
            while fromVertex == toVertex or (fromVertex, toVertex) in self.capacity:
                fromVertex = randint(1, numVertices)
                toVertex = randint(1, numVertices)
            capacity = randint(1, capacityRange) 
            self.addEdge(fromVertex, toVertex, capacity)


    def addVertex(self, v):
        """
        Inserts a vertex into the network.
        """
        self.adjacent.setdefault(v, list())


    def addEdge(self, fromVertex, toVertex, capacity):
        """
        Inserts an edge into the network.
        """
        if self.isValidEdge(fromVertex, toVertex, capacity):
            self.adjacent.setdefault(fromVertex, []).append(toVertex)
            self.adjacent.setdefault(toVertex, []).append(fromVertex)
            self.capacity[(fromVertex, toVertex)] = capacity 
            self.flow[(fromVertex, toVertex)] = 0
            self.flow[(toVertex, fromVertex)] = 0


    def isValidEdge(self, fromVertex, toVertex, capacity):
        """
        Verifies the validity of an edge.
        """
        return fromVertex != toVertex \
               and capacity > 0 \
               and (toVertex, fromVertex) not in self.capacity


    def showFlow(self):
        """
        Represents the flow across the network.
        """
        def edgesFromVertex(u):
            """
            Represents the flow across the given vertex.
            """
            edgeRepresentation = lambda v: f"({u}, {v}, {self.getCapacity((u, v))}, {self.getFlow((u,v))})"
            return ", ".join(map(edgeRepresentation, sorted(self.adjacent[u])))

        def adjacencyLists():
            """
            Represents the flow across all relevant vertices.
            """
            anyNeighbor = lambda u: any(self.neighbors(u))
            verticesWithNeighbors = filter(anyNeighbor, sorted(self.vertices()))
            return map(edgesFromVertex, verticesWithNeighbors)

        return print("\n".join(adjacencyLists()))


    def __str__(self):
        """
        Returns a string that represents the network.
        """
        def edgesFromVertex(u):
            """
            Represents edges incident to the given vertex.
            """
            edgeRepresentation = lambda v: f"({u}, {v}, {self.capacity[(u, v)]})"
            return ", ".join(map(edgeRepresentation, self.residualNeighbors(u)))

        def adjacencyLists():
            """
            Represents edges incident to relevant vertices
            """
            anyNeighbor = lambda u: any(self.neighbors(u))
            verticesWithNeighbors = filter(anyNeighbor, sorted(self.vertices()))
            return map(edgesFromVertex, verticesWithNeighbors)

        return "\n".join(adjacencyLists())


    def __repr__(self):
        """
        Represents the flow network.
        """
        return str(self)

