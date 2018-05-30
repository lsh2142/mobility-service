import collections

class SimpleGraph:
	def __init__(self):
		self.edges = {}
	
	def neighbors(self, id):
		return self.edges[id]

class SquareGrid:
	def __init__(self, width, height):
		self.width = width
		self.height = height
		self.walls = []
	
	def isInBound(self, id):
		(x,y) = id
		return 0 <= x < self.width and 0 <= y < self.height

	def passable(self, id):
		return id not in self.walls

	def neighbors(self, id):
		(x,y) = id
		results = [(x+1, y),

class GraphWithWeights(SimpleGraph):
	def __init__(self):
		

class Queue:
	def __init__(self):
		self.elements = collections.deque()

	def empty(self):
		return len(self.elements) == 0
	
	def put(self,x):
		self.elements.append(x)
	
	def get(self):
		return self.elements.popleft()



example_graph = SimpleGraph()
example_graph.edges = {
	'A':['B'],
	'B':['A','C','D'],
	'C':['A'],
	'D':['E','A'],
	'E':['B']
}

def bfs_1(graph, start):
	frontier = Queue()
	frontier.put(start)
	visited = {}
	visited[start] = True

	while not frontier.empty():
		current = frontier.get()
		print("Visiting %r" % current)
		for next in graph.neighbors(current):
			if next not in visited:
				frontier.put(next)
				visited[next] = True

bfs_1(example_graph, 'B')


