################################################
################################################
################################################
###        TFM Manuel Moya Ferrer            ###
###      -    Mininet Simulation     -       ###
#             Microservice AP2                 #
################################################
################################################
################################################

from scapy.all import *
import threading
import MySQLdb
from datetime import datetime
import networkFormation

def getAverageSSI():
    global ssiFinal
    return ssiFinal

def setParamsAP2():
    global window
    global timestampAP2
    global datetime
    global iterator1
    global ssiArrayAP2

    window = 1
    timestampAP2 = datetime.now()
    iterator = 0
    ssiArrayAP2 = []

def myPacketHandler(pkt) :
    global timestampAP2
    global iterator
    global ssiArrayAP2

    if pkt.haslayer(Dot11) :

        Conexion = MySQLdb.connect(host='manuelmoyatfmdb.co8n1ozzlu1i.eu-west-3.rds.amazonaws.com', port = 3306,user='manuelmoya',passwd='manuelmoya', db='ManuelMoyaTFMDB')
        cur = Conexion.cursor(MySQLdb.cursors.DictCursor)

        if pkt.type == 0 and pkt.subtype == 8 :

            ssiNew = -(256-ord(pkt.notdecoded[-4:-3]))
            ssiArrayAP2.append(ssiNew)

            SSID = pkt.info;

            if SSID.startswith("Mobile") :

                diffT=(datetime.now()-timestampAP2).seconds
                
                if diffT > window and len(ssiArrayAP2) > 0:

                    query = "START TRANSACTION;"
                    queryBack=cur.execute(query)

                    iterator+=1

                    query = "INSERT INTO RSSI VALUES(%d,\"AP2\",%d);"%(iterator, sum(ssiArrayAP2)/len(ssiArrayAP2))
                    queryBack = cur.execute(query)

                    ssiArrayAP2 = []

                    Conexion.commit()

                    timestampAP2=datetime.now()


                    
setParamsAP2()

try:
    sniff(iface="ap2-wlan1", prn = myPacketHandler, store=0)
except Exception as e:
    print e
    print "Sniff AP2 Off"