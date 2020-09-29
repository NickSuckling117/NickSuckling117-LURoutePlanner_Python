#This statement imports the required module for this program to run
import SQLHandler as sql

#This section of code defines the node class and defines its attributes and runs some subroutines
class Node:
    def __init__(self, StationID):
        self.id = StationID
        self.name = ""
        self.numberOfConnections = 0
        self.appearsOn = []
        self.adjacent = {}
        self.open = False
        self.visited = False
        self.distanceFromStart = float('inf')

        self.AddNodeName()
        self.AddNumberOfConnections()
        self.AddLines()
        self.AddAdjacentStations()
        self.GetOpenValue()

#This subroutine changes the print output of the node object
    def __str__(self):
        return str("Node: {0} - Open = {1}".format(self.id, self.open))

#This subroutine is used to retrieve the name of the node based on its ID
    def AddNodeName(self):
        self.name = sql.GetCurrentNodeName(self.id)

#This subroutine calculates the amount connection from that node to adjacent stations
    def AddNumberOfConnections(self):
        allConnections = sql.GetCurrentNodeAdjacentConnections(self.id)
        for record in allConnections:
            for field in record:
                if field == "0":
                    pass
                else:
                    self.numberOfConnections += 1

#This subroutine retrieves all of the lines that this node appears on
    def AddLines(self):
        self.appearsOn = sql.GetLinesOnCurrentNode(self.id)

#This subroutine retrieves all of the stations that are adjacent to that node
    def AddAdjacentStations(self):
        self.adjacent = sql.GetStationsAdjacentToCurrentNode(self.id)

#This subroutine gets teh status value of the node
    def GetOpenValue(self):
        self.open = sql.GetOpenClosedValueForCurrentNode(self.id)

#This section of code defines the graph class and defines its attributes.
class Graph:
    def __init__(self):
        self.nodes = {}
        self.existingNodes = []
        self.numberOfNodes = 0
        self.edges = {}
        self.numberOfEdges = 0

#This subroutine allows for a new node to be created. The station id is passed to the node so it can collect its attributes
#itself
    def AddNewNode(self, StationID):
        newNode = Node(StationID)
        self.nodes[StationID] = newNode
        self.existingNodes.append(StationID)
        self.numberOfNodes +=1

#This subroutine adds a new edge between two nodes bu getting the node its going to, the node its going from and then the weight of that node
    def AddNewEdge(self, frm, to, time):
        for line in frm.adjacent:
            for station in frm.adjacent[line]:
                if station == to.id:
                    key = frm.id+"-"+to.id
                    self.edges[key] = frm, to, line, time
                    self.numberOfEdges += 1
                    
        for line in to.adjacent:
            for station in to.adjacent[line]:
                if station == frm.id:
                    key = to.id+"-"+frm.id
                    self.edges[key] = to, frm, line, time
                    self.numberOfEdges += 1

#this subroutine retrieves and displays a specific edge in the shell
    def GetEdge(self, edgeKey):
        edgeRetrieved = g.edges[edgeKey]
        print("{0} is ({1}) connected to ({2}) on line {3} with a time of {4}".format(edgeKey, edgeRetrieved[0], edgeRetrieved[1], edgeRetrieved[2], edgeRetrieved[3]))
        return edgeRetrieved

#This subroutine completely resets the graph so it is completely empty.
    def ResetGraph(self):
        self.nodes = {}
        self.existingNodes = []
        self.numberOfNodes = 0
        self.edges = {}
        self.numberOfEdges = 0
        print("Graph Cleared")

#This subroutine create the first node that will be added to the graph using values from the GUI
    def CreateStartingNode(self, startName, endName):
        self.ResetGraph()
        startID = sql.GetStationIDFromStationName(startName)
        endID = sql.GetStationIDFromStationName(endName)
        g.AddNewNode(startID)
        g.nodes[startID].distanceFromStart = 0
        self.Dijkstra(startID, startID, endID)
        sql.addNewRoute(startID, endID, self.fullRouteNames)
        return self.fullRouteNames

#This subroutine works out if the end station has been created or if new nodes need to be created and searched through tpo find the end station
    def Dijkstra(self, startID, currentNode, endID):
        self.nodes[currentNode].visited = True
        if self.nodes[currentNode].id == endID:
            self.nextNodeToTrace = endID
            self.fullRouteIDs = []
            self.fullRouteNames = []
            while self.nextNodeToTrace != startID:
                self.TraceRouteBack(self.nextNodeToTrace)
            self.fullRouteIDs.reverse()
            previous = None
            for i in self.fullRouteIDs:
                fullRouteNamesSegment = []
                fromStationName = sql.GetStationNameFromStationID(i[0])
                toStationName = sql.GetStationNameFromStationID(i[1])
                lineName = sql.GetLineNameFromLineID(i[2])
                time = i[3]
                fullRouteNamesSegment.append(fromStationName)
                fullRouteNamesSegment.append(toStationName)
                fullRouteNamesSegment.append(lineName)
                fullRouteNamesSegment.append(time)
                if fullRouteNamesSegment != previous:
                    previous = fullRouteNamesSegment
                    self.fullRouteNames.append(fullRouteNamesSegment)
        else:
            self.CreateAdjacentNodes(currentNode)
            nextNode = self.GetNextNode()
            self.Dijkstra(startID, nextNode, endID)

#This subroutine creates any nodes that should be adjacent to this node.
    def CreateAdjacentNodes(self, currentNode):
        for line in self.nodes[currentNode].adjacent:
            for adjacentStation in self.nodes[currentNode].adjacent[line]:
                exist = False
                for existingStation in self.existingNodes:
                    if existingStation == adjacentStation:
                        exist = True
                    else:
                        pass
                if exist == False:
                    self.AddNewNode(adjacentStation)
                else:
                    pass
                self.AddEdgeBetweenCurrentNew(line, currentNode, adjacentStation)

#This subroutine creates a new edge between the current node and one of the new stations.
    def AddEdgeBetweenCurrentNew(self, line, currentNode, adjacentStation):
        time = self.nodes[currentNode].adjacent[line][adjacentStation]
        self.AddNewEdge(self.nodes[currentNode], self.nodes[adjacentStation], time)
        self.CalculateDistanceFromStart(currentNode, adjacentStation, time)

#This subroutine is used to calculate the distance from the starting node and then applies it to that node.
    def CalculateDistanceFromStart(self, currentNode, adjacentStation, time):
        calculatedTime = self.nodes[currentNode].distanceFromStart + time
        if calculatedTime < self.nodes[adjacentStation].distanceFromStart:
            self.nodes[adjacentStation].distanceFromStart = calculatedTime

#This subroutine gets the next node that needs to be visited by looking for the node that has not been visited with the lowest distance from start.
    def GetNextNode(self):
        lowestTime = float('inf')
        nextNode = None
        for node in self.nodes:
            if self.nodes[node].distanceFromStart < lowestTime and self.nodes[node].visited != True:
                lowestTime = self.nodes[node].distanceFromStart
                nextNode = node
        return nextNode

#This node is used to trace through the generated graph and retrieve all of the data that is needed to create instructions for the user.
    def TraceRouteBack(self, currentNode):
        routeSegment = []
        for edge in self.edges:
            if self.edges[edge][0].id == currentNode:
                if self.edges[edge][0].distanceFromStart - self.edges[edge][1].distanceFromStart == self.edges[edge][3]:
                    routeSegment.append(self.edges[edge][1].id)
                    routeSegment.append(self.edges[edge][0].id)
                    routeSegment.append(self.edges[edge][2])
                    routeSegment.append(self.edges[edge][3])
                    self.fullRouteIDs.append(routeSegment)
                    self.nextNodeToTrace = routeSegment[0]
                


g = Graph()
print("Graph made")
