import boto3
import sys
import logging
import rds_config
import pymysql

rds = boto3.client('rds',region_name='ap-northeast-2')

try:
    dbs = rds.describe_db_instances()
    for db in dbs['DBInstances']:
        print(("%s@%s:%s %s") % (db['MasterUsername'], db['Endpoint']['Address'], db['Endpoint']['Port'], db['DBInstanceStatus']))

except Exception as e:
    print(e)

#print("\n\r Create Database Instance")

#response = rds.create_db_instance(
#        DBInstanceIdentifier = 'newdb', 
#        MasterUsername = 'supermove',
#        MasterUserPassword = 'supermove',
#        DBInstanceClass = 'db.t2.micro',
#        Engine = 'mysql',
#        AllocatedStorage = 5
#    )
#print(response)

#print("Delete database")

#response = rds.delete_db_instance(
#        DBInstanceIdentifier = 'newdb',
#        SkipFinalSnapshot = True
#    )
#print(response)

rds_host = rds_config.db_endpoint
name = rds_config.db_username
password =rds_config.db_password
db_name = rds_config.db_name
port = rds_config.db_port

logger = logging.getLogger()
logger.setLevel(logging.INFO)

try:
    conn = pymysql.connect(rds_host, user=name,
        passwd=password, db=db_name, connect_timeout=10, charset='utf8')

except Exception as e:
#    logger.error("ERROR: Unexpected error: Could not connect to MySQL instance")
    print(e)
    sys.exit()

logger.info("SUCCESS")

def checkEncoding():
    with conn.cursor() as cur:
        cur.execute("show variables like 'c%';")
    for row in cur:
        print(row)


def makeTable():
    with conn.cursor() as cur:
        cur.execute("create table Subway (id int NOT NULL AUTO_INCREMENT, station_cd int NOT NULL, station_nm varchar(255) NOT NULL, line_num int NOT NULL, PRIMARY KEY (id))")
        conn.commit()

def deleteSubwayList():
    with conn.cursor() as cur:
        cur.execute('delete from Subway where 1=1')
    conn.commit()


def insertSubwayList(stationList):
    with conn.cursor() as cur:
        for st in stationList:
            queryStr =  'insert into Subway (station_cd, station_nm, line_num) values(%d,"%s",%d)' % (int(st['STATION_CD']), st['STATION_NM'], int(st['LINE_NUM']))
            cur.execute(queryStr)

    conn.commit()

def getSubwayList():
    subway_list = []
    with conn.cursor() as cur:
        cur.execute("select * from Subway")
        for row in cur:
            subway_list.append(row)

    return subway_list
    
def lambda_handler(event, context):
    
    item_count = 0

    with conn.cursor() as cur:
        cur.execute("create table Test (TestId int NOT NULL AUTO_INCREMENT, TestNum int NOT NULL, TestNm varchar(255) NOT NULL, PRIMARY KEY (TestId))")
        cur.execute('insert into Test (TestNum, TestNm) values(99,Hello)')
        conn.commit()
        cur.execute("select * from Test")
        for row in cur:
            item_count +=1
            logger.info(row)

    return "Added %d items to RDS MySQL table" %(item_count)
