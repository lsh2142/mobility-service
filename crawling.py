#-*- coding: utf-8 -*-

from urllib import request
import json
import re
from bs4 import BeautifulSoup
import testutil
import sys
import python_rdb as db

class Subway():
    def setData(self, tup):
        self.id, self.station_cd, self.station_nm, self.line_num = tup
    def __repr__(self):
        return self.station_nm
    def __str__(self):
        return self.station_nm


#python_rdb.makeTable()

def insertSubwayListToDB():
    for i in range(1,10):
        subwayListQuery = testutil.SubwayListData()
        subwayListQuery.setLineNum(i)

        u = request.urlopen(subwayListQuery.makeQueryURL())
        data = u.read()
        encoding = u.info().get_content_charset('utf-8')

        json_data = json.loads(data.decode(encoding))
        stationList = json_data[subwayListQuery.service_name]['row']
        #    db.insertSubwayList(stationList)

def getShortestRoute(origin,dest):
    shortestRouteQuery = testutil.SubwayShortestRouteData()
    shortestRouteQuery.setStationNames(origin,dest)

    u = request.urlopen(shortestRouteQuery.makeQueryURL())
    data = u.read()
    encoding = u.info().get_content_charset('utf-8')
    json_data = json.loads(data.decode(encoding))
    print(json_data)
#    shortestRoute = json_data[subwayListQuery.service_name]['row']v

subway_list = []
i = 0
for tup in db.getSubwayList():
    s = Subway()
    s.setData(tup)
    subway_list.append(s)
    i+=1
    
origin = subway_list[2]
dest = subway_list[20]

print(origin)
print(dest)
print(i)

getShortestRoute(subway_list[2].station_nm,subway_list[420].station_nm)

#print(str(data,"utf-8"))
