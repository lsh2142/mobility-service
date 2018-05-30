import urllib
import datetime
import config
from urllib.parse import quote

class SeoulAPIData:
    def __init__(self):
        self.url = 'http://openAPI.seoul.go.kr:8088/'
        self.auth = config.auth
        self.type = 'json'
        self.service_name=''
        self.start_index='0'
        self.end_index='100'
    
    def setServiceName(serviceNm):
        self.service_name = serviceNm

    def makeBaseString(self):
        string_list = []
        string_list.append(self.url)
        string_list.append(self.auth+'/')
        string_list.append(self.type+'/')
        string_list.append(self.service_name+'/')
        string_list.append(self.start_index+'/')
        string_list.append(self.end_index+'/')

        return string_list


class SubwayListData(SeoulAPIData):
    def __init__(self):
        super().__init__()
        self.service_name='SearchSTNBySubwayLineService'
        self.lineNum='1'

    def setLineNum(self, lineNum):
        self.lineNum= str(lineNum)

    def makeQueryURL(self):
        string_list= super().makeBaseString()
        string_list.append(self.lineNum)

        return ''.join(string_list)

    
class SubwayShortestRouteData(SeoulAPIData):
    def __init__(self):
        super().__init__()  
        self.service_name='shortestRoute'
        self.statnFnm=''
        self.statnTnm=''

    def setStationNames(self, origin, dest):
        self.statnFnm = origin
        self.statnTnm = dest

    def makeQueryURL(self):
        string_list = super().makeBaseString()
        string_list.append(quote(self.statnFnm)+'/')
        string_list.append(quote(self.statnTnm))

        return ''.join(string_list)

class SubwayDetailData(SeoulAPIData):
    def __init__(self):
        super().__init__()
        self.service_name='SearchInfoBySubwayNameService'
        self.station_nm = ''
    
    def makeQueryURL(self):
        string_list = super().makeBaseString()
        string_list.append(self.station_nm)

        return ''.join(string_list)

class CardSubwayStatsData(SeoulAPIData):
    def __init__(self):
        super().__init__()
        self.service_name='CardSubwayStatsNew'
        self.date=''

    def setDate(datestr):
        self.date = datestr

    def makeQueryURL(self):
        string_list = super().makeBaseString()
        string_list.append(self.date)

        return ''.join(string_list)

class StationDistanceTimeData(SeoulAPIData):
    def __init__(self):
        super().__init__()
        self.service_name='StationDstncReqreTimeHm'
        self.line_num = '1'
        #optional
        self.station_cd=None

    def setLineNum(line):
        self.line_num = line

    def setStation(station):
        self.station_cd = station

    def makeQueryURL(self):
        string_list = super().makeBaseString()
        string_list.append(self.line_num)
        if self.station_cd is not None:
            string_list.append('/'+self.station_cd)

        return ''.join(string_list)

class SearchTimeTableById(SeoulAPIData):
    def __init__(self):
        super().__init__()
        self.service_name='SearchSTNTimeTableByIDService'
        self.station_cd = ''
        self.week = 1
        self.inout_tag = 1

    def makeQueryURL(self):
        string_list = super().makeBaseString()
        string_list.append(self.station_cd+'/')
        string_list.append(self.week+'/')
        string_list.append(self.inout_tag)

        return ''.join(string_list)


#Without CompanyCode query start_dt is limited to 3 months from end_date
def makeDateText(y,m,d):
    d = datetime.date(y,m,d)

    return d.strftime('%Y%m%d')

def getCompanyDataFromFile(filename):
    crp_data = []
    f = open(filename,'r')
    while True:
        datum = {}
        isFinish = False
        for i in range(6):
            line = f.readline()
            if not line:
                isFinish = True
                break;                              
            datum[crp_keys[i]] = line.split(":")[1].strip()
        
        if isFinish:
            break
        else:
            crp_data.append(datum)

    return crp_data
