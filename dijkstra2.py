from collections import defaultdict, deque
from data import *

class Graph:
    def __init__(self):
        self.nodes = set()
        self.edges = defaultdict(list)
        self.distances = {}

    def add_node(self, value):
        self.nodes.add(value)

    def add_edge(self, from_node, to_node, distance):
        self.edges[from_node].append(to_node)
        self.distances[(from_node, to_node)] = distance

    def add_nodes_all(self, stationList):
        self.nodes.update(stationList)

    def add_edges_all(self, routeDict):
        self.edges = routeDict

    def setStationList(self, stationList):
        self.stationList = stationList

def dijsktra(graph, initial):
    stationList = graph.stationList
    visited = {initial:0}
    path = {}

    nodes = set(graph.nodes)

    while nodes:
        min_node = None
        for node in nodes:
            if node in visited:
                if min_node is None:
                    min_node = node
                elif visited[node] < visited[min_node]:
                    min_node = node

        if min_node is None:
            break;

        nodes.remove(min_node)
        current_weight = visited[min_node]

#        for key in graph.edges.keys():
#            print("key : %s" % key )
#            print(graph.edges[key])

        for edge in graph.edges[min_node]:
            dest_station = getStationByName(stationList, edge['dest'])
            weight = current_weight + edge['weight']

            if dest_station not in visited or weight < visited[dest_station]:
                visited[dest_station] = weight
                path[dest_station] = min_node

    return visited, path

def shortest_path(graph, origin, destination):
    origin_station = getStationByName(graph.stationList,origin)
    dest_station = getStationByName(graph.stationList,destination)

    visited, paths = dijsktra(graph, origin_station)
    full_path = deque()
    _destination = paths[dest_station]

   
    while _destination != origin_station:
        full_path.appendleft(_destination)
        _destination = paths[_destination]

    full_path.appendleft(origin_station)
    full_path.append(dest_station)

    return visited[dest_station], list(full_path)

def getStationByName(stationList, name):
    for station in stationList:
        if station.station_nm == str(name):
            return station
    else:
        raise Exception("Station is not exist")

g = Graph()

stationList = []
stationList.append(Station('A'))
stationList.append(Station('B'))
stationList.append(Station('C'))
stationList.append(Station('D'))

g.add_nodes_all(stationList)
g.setStationList(stationList)

routeList = []
routeList.append(Route('A','B',5))
routeList.append(Route('B','A',7))
routeList.append(Route('A','C',9))
routeList.append(Route('C','A',8))
routeList.append(Route('B','C',10))
routeList.append(Route('C','B',8))
routeList.append(Route('A','D',26))
routeList.append(Route('D','A',24))
routeList.append(Route('B','D',15))
routeList.append(Route('C','D',14))
routeList.append(Route('D','C',9))

routeDict = {}

for route in routeList:
    origin = getStationByName(stationList, route.origin)

    if origin is None:
        print("origin is none, continue")
        continue
    try:
        if origin not in routeDict:
            routeDict[origin] = []
    except KeyError as ke:
        print(ke)

    routeDict[origin].append({'dest':getStationByName(stationList,route.dest),'weight':route.spending_time})

g.add_edges_all(routeDict)

print(shortest_path(g,'A','D')) 
