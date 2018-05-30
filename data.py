class Station:
    def __init__(self,name):
        self.crd = (0,0)
        self.station_nm = name
        self.available_tp_type = []

    def __str__(self):
        return self.station_nm

    def __repr__(self):
        return "St "+self.__str__()

    def __hash__(self):
        return hash(str(self))

class Route:
    def __init__(self, origin, dest, weight):
        self.origin = origin
        self.dest = dest
        self.spending_time = weight
        self.tp_type = []
    def __str__(self):
        return (self.origin, self.dest)
    def __repr__(self):
        return str(self.__str__())

class Transportation:
    def __init__(self):
        self.routeIndex = 0
        self.tp_type = 1
