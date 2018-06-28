from collections import defaultdict
import csv
import time

## DEFINITIONS OF CONSTANTS
INFINITE = 999999
#TRANSIT_THRESHOLD = 6
TRANSIT_THRESHOLD = 10
WALK_THRESHOLD = 6
DIRECTION_TO = 1
DIRECTION_FROM = 0
MAX_TRANSFER = 3

# TIME CONSUME OF TRANSPORTATIONS
WEIGHT_BUS = 1
WEIGHT_WALK = 2

# DOES TRAVERSE INVOLVES TRANSIT
WEIGHT_NOTRANSIT = 0
WEIGHT_TRANSIT = 5

# TYPE OF EDGE
EDGE_NORMAL = 0
EDGE_TRANSIT = 1
EDGE_LASTMILE = 2

# NODE STYLE
NODE_END = -1
NODE_START = -2

TIME_GRAPH = 0
TIME_DIJKSTRA = 0

# NODE STATUS
VERTEX_OPENED = 0
VERTEX_CLOSED = 1

# Counter
#global VERTEX_COUNT
#global EDGE_COUNT

class Vertex:
    def __init__(self, seq, line):
        self.cost = INFINITE
        self.edge = []
        self.seq = seq
        self.line = line
        self.status = VERTEX_OPENED
        self.origin = set()

    def setCost(self, val):
        self.cost = val

    def setOrigin(self, origin):
        self.origin.clear()
        self.origin.add(origin)

    def addOrigin(self, origin):
        self.origin.add(origin)

    def addEdge(self, edge):
        self.edge.append(edge)

    def setStatus(self, status):
        self.status = status

    def getStatus(self):
        return self.status

    def getEdge(self):
        return self.edge

    def getOrigin(self):
        return self.origin

    def getSeq(self):
        return self.seq

    def getLine(self):
        return self.line

    def getCost(self):
        return self.cost

    def getEdgeBasis(self):
        refine = []
        for aedge in self.edge:
            if (aedge.getType() == EDGE_NORMAL):
                refine.append(aedge)

        return refine

class Edge:
    def __init__(self, edge_type, to, weight):
        self.to = to
        self.weight = weight
        self.edge_type = edge_type

    def setType(self, edge_type):
        self.edge_type = edge_type

    def getType(self):
        return self.edge_type

    def getWeight(self):
        return self.weight

    def getDestination(self):
        return self.to

def parseXY(coord):
    coordX = str(coord)[0] + str(coord)[1]
    coordY = str(coord)[2] + str(coord)[3]
    retX = int(coordX)
    retY = int(coordY)

    return retX, retY

def distance(origin, dest):
    parsedOrigin = parseXY(origin)
    parsedDest = parseXY(dest)

    xo = parsedOrigin[0]
    xd = parsedOrigin[1]
    yo = parsedDest[0]
    yd = parsedDest[1]

    return abs(xo - yo) + abs(xd - yd)

def ready(linebase):
    global VERTEX_ALLCOUNT
    global EDGE_ALLCOUNT
    VERTEX_ALLCOUNT = 0
    EDGE_ALLCOUNT = 0
    with open('../test-cases/bus64.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='\"')
        node = None
        readHeader = False

        for row in spamreader:
            if (readHeader == False):
                readHeader = True
                continue

            stations = row[2]
            station = stations.split(",")

            node = Vertex(station[0], row[1])
            prev = node
            VERTEX_ALLCOUNT += 1

            linebase.append(node)

            for es in station:
                if (station.index(es) == 0):
                    continue

                node = Vertex(es, row[1])
                edge = Edge(EDGE_NORMAL, node,
                            WEIGHT_BUS * distance(prev.getSeq(), node.getSeq()))
                prev.addEdge(edge)
                prev = node
                VERTEX_ALLCOUNT += 1
                EDGE_ALLCOUNT += 1
    #print("# OF VERTICES : %d / # OF EDGES : %d" %(VERTEX_ALLCOUNT, EDGE_ALLCOUNT))

    setBasicTransit(linebase)


def setBasicTransit(linebase):
    for node in linebase:
        linkAdjacent(linebase, node, WEIGHT_WALK, EDGE_TRANSIT, DIRECTION_FROM, TRANSIT_THRESHOLD)
        edges = [] + node.getEdgeBasis()

        while edges:
            temp = edges[0].getDestination()
            linkAdjacent(linebase, temp, WEIGHT_WALK, EDGE_TRANSIT, DIRECTION_FROM, TRANSIT_THRESHOLD)

            edges += temp.getEdgeBasis()
            edges.remove(edges[0])

def linkAdjacent(linebase, target, tWeight, edge_type, direction, threshold):
    global EDGE_ALLCOUNT
    global VERTEX_ALLCOUNT
    for node in linebase:
        if (node.getLine() == target.getLine()):
            continue

        temp = node
        coord = node.getSeq()
        temp_edges = temp.getEdgeBasis()

        dist = tWeight * distance(coord, target.getSeq())
        if(edge_type == EDGE_TRANSIT):
            dist += WEIGHT_TRANSIT

        if (dist < threshold):
            EDGE_ALLCOUNT += 1
            if (direction == DIRECTION_FROM):
                edge = Edge(EDGE_TRANSIT, temp, dist)
                target.addEdge(edge)
            elif (direction == DIRECTION_TO):
                edge = Edge(EDGE_TRANSIT, target, dist)
                temp.addEdge(edge)

        edges = [] + temp_edges
        while edges:
            if (edges[0].getDestination() == target):
                edges.remove(edges[0])
                continue

            temp = edges[0].getDestination()
            coord = temp.getSeq()
            dist = tWeight * distance(coord, target.getSeq())
            if (edge_type == EDGE_TRANSIT):
                dist += WEIGHT_TRANSIT

            if (dist < threshold):
                EDGE_ALLCOUNT += 1
                if (direction == DIRECTION_FROM):
                    edge = Edge(EDGE_TRANSIT, temp, dist)
                    target.addEdge(edge)
                elif (direction == DIRECTION_TO):
                    edge = Edge(EDGE_TRANSIT, target, dist)
                    temp.addEdge(edge)

            edges.remove(edges[0])
            edges += temp.getEdgeBasis()

# Input  : 개별 노선의 첫 정류장 리스트
# Output : None
# linebase에 등록된 모든 정류장들을 탐색하여 전체 그래프에 있는 Vertex들을 출력
def inspectGraph(linebase):
    seq = 0
    for node in linebase:
        print("== Linebase ", str(seq), " inspection start ==")
        tempedge = []
        for edge in node.getEdge():
            tempedge.append(hex(id(edge.getDestination())))

        print("[", hex(id(node)), "]", node.getSeq(), "/", node.getLine(), "/", tempedge)
        seq += 1

        edges = [] + node.getEdgeBasis()

        while edges:
            temp = edges[0].getDestination()

            tempedge.clear()
            for edge in temp.getEdge():
                tempedge.append(hex(id(edge.getDestination())))

            print("[", hex(id(temp)), "] ", temp.getSeq(), "/", temp.getLine(), "/", tempedge)

            edges.remove(edges[0])
            edges += temp.getEdgeBasis()

# Input  : 탐색을 시작할 Vertex
# Output : 탐색을 종료할 Vertex
# Dijkstra 알고리즘을 수행함
def dijkstra(start, end):
	# Dijkstra algorithm
	# Visit -> Select the smallest cost -> Expand and repeat until
	# the program tries to expand the end vertex.
    VERTEX_COUNT = 0
    EDGE_COUNT = 0

	# 시작 Vertex 초기화
	# 시작 Vertex까지 걸리는 시간은 0, 출발점이므로 기점이 없다.
    start.setCost(0)
    start.addOrigin(None)
    visited = []
    visited.append(start)

    isFound = False

	# 이미 Expand된 친구들을 다시 꺼내보지 않기 위해 리스트 선언
    # closed = []
    while visited:
        # select minimal
        min_val = INFINITE
        min_node = None
        VERTEX_COUNT += 1
        for node in visited:
            if node.getCost() < min_val:
                min_val = node.getCost()
                min_node = node

        # before expansion, check it is the end node.
        if (end == min_node):
            isFound = True
            break

        # expand
        for edge in min_node.getEdge():
            EDGE_COUNT += 1
            # Dijkstra
            cost = min_node.getCost() + edge.getWeight()
            # A star
            #cost = min_node.getCost() + edge.getWeight() + distance(end.getSeq(), edge.getDestination().getSeq())
            if (cost < edge.getDestination().getCost()):
                # minimum, renew
                edge.getDestination().setCost(cost)
                edge.getDestination().setOrigin(min_node)
            elif (cost == edge.getDestination().getCost()):
                edge.getDestination().addOrigin(min_node)

            if(edge.getDestination() not in visited and edge.getDestination().getStatus() != VERTEX_CLOSED):
                visited.append(edge.getDestination())

        # erase
        visited.remove(min_node)
        min_node.setStatus(VERTEX_CLOSED)
        #closed.append(min_node)

    if (isFound):
        print("====================================================")
        print("[지성] 대장님 " + str(end.getCost()) + "분이 걸린답니다!")
        print("====================================================")
        walkOptimal(start, end)
    else:
        print("====================================================")
        print("[기술대장] 아니 지성아 내 말 좀 들어봐")
        print(end.getSeq(), "로 가는 경로를 찾을 수 없습니다.")
        print("====================================================")

    print("Vertex 접근 : ", VERTEX_COUNT, " Edge 접근 : ", EDGE_COUNT)

def walkOptimal(start, end):
    stacks = []
    stack = []
    transfers = []

    stack.append(end)
    stacks.append(stack)
    transfers.append(int(1))

    while True:
        if stacks[0][-1] == start:
            break

        stack = stacks.pop(0)
        transfer = transfers.pop(0)
        temp = stack[-1]

        for origins in temp.getOrigin():
            transfer_temp = transfer
            stack_expand = []
            stack_expand += stack
            stack_expand.append(origins)
            stacks.append(stack_expand)
            if(origins.getLine() != temp.getLine()):
                transfer_temp += 1
            transfers.append(transfer_temp)

    order = 1
    minimal = []
    min_transfer = 999

    for stack in stacks:
        trans = transfers.pop() - 3
        if(min_transfer > trans):
            min_transfer = trans
            minimal.clear()
            minimal.append(int(order))
        elif(min_transfer == trans):
            minimal.append(int(order))

        print("> 최단경로 Trace#", order)
        print("> 환승 #", str(trans))
        way = ">> "
        while stack:
            item = stack.pop()
            line = ""
            if item.getLine() == str(NODE_START):
                line = "시작"
            elif item.getLine() == str(NODE_END):
                line = "종료"
            else:
                line = item.getLine() + "호선"

            way += "[" + str(item.getCost()) + "분]" + item.getSeq() + "정류장/" + line + " "
        print(way)
        print()
        order += 1

    print()
    print("최단 경로 추천 : " + str(minimal))

VERTEX_COUNT = 0
EDGE_COUNT = 0

lines = []
print("좌표를 입력하세요: 예시- (04,03) = 0403")
start = input("시작 좌표: ")
end = input("종료 좌표: ")

# 그래프 그리는 루틴 #
time1 = time.time()
ready(lines)
startVertex = Vertex(str(start), str(NODE_START))
endVertex = Vertex(str(end), str(NODE_END))

linkAdjacent(lines, startVertex, WEIGHT_WALK, EDGE_LASTMILE, DIRECTION_FROM, WALK_THRESHOLD)
linkAdjacent(lines, endVertex, WEIGHT_WALK, EDGE_LASTMILE, DIRECTION_TO, WALK_THRESHOLD)

lines.append(startVertex)
lines.append(endVertex)
TIME_GRAPH = time.time() - time1
# 그래프 그리는 루틴 끝 #

## 그래프 검사 루틴 (디버그 용도)
#inspectGraph(lines)

# 다익스트라 루틴 #
time1 = time.time()
dijkstra(startVertex, endVertex)
TIME_DIJKSTRA = time.time() - time1
	# 다익스트라 루틴 끝 #

VERTEX_ALLCOUNT += 2
print("============ PERFORMANCE ESTIMATION ===================")
print("# of Vertices : %d, # of Edges : %d" %(VERTEX_ALLCOUNT, EDGE_ALLCOUNT))
print("그래프 생성 시간 : " + str(TIME_GRAPH * 1000) + "ms 다익스트라 탐색시간 : " + str(TIME_DIJKSTRA * 1000) + "ms")
