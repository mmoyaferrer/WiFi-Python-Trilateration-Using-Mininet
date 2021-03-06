#!/usr/bin/python

################################################
################################################
################################################
###        TFM Manuel Moya Ferrer            ###
###      -    Mininet Simulation     -       ###
#         Parameters of Simulation             #
################################################
################################################
################################################

positionMobile1='20,20,00'  # x, y, z from 0 to 99 m
positionAP1='00,00,00'
positionAP2='50,00,00'
positionAP3='00,50,00'

antennaGainMobile1='0'
txpowerMobile1='0'
antennaHeightMobile1='2'
channelMobile1='36'
rangeMobile1=100

antennaGainAP1='3'
txpowerAP1='0'
antennaHeightAP1='20'
channelAP1='36'
rangeAP1=100

antennaGainAP2='3'
txpowerAP2='0'
antennaHeightAP2='20'
channelAP2='36'
rangeAP2=100

antennaGainAP3='3'
txpowerAP3='0'
antennaHeightAP3='20'
channelAP3='36'
rangeAP3=100

################################################
################################################
################################################
################################################
################################################


from mininet.node import Controller
from mininet.log import setLogLevel, info
from mininet.wifi.node import OVSKernelAP
from mininet.wifi.link import wmediumd
from mininet.wifi.cli import CLI_wifi
from mininet.wifi.net import Mininet_wifi
from mininet.wifi.wmediumdConnector import interference


def topology():
    "Create a network."
    net = Mininet_wifi(controller=Controller, link=wmediumd,
                       accessPoint=OVSKernelAP, wmediumd_mode=interference,
                       noise_threshold=-91, fading_coefficient=1)

    info("*** Creating nodes\n")

    ap10 = net.addAccessPoint('Mobile1', ssid='Mobile1',
        mode='a', channel=channelMobile1, position=positionMobile1,range=rangeMobile1,antennaGain=antennaGainMobile1,
        txpower=txpowerMobile1, antennaHeight=antennaHeightMobile1)

    ap1 = net.addAccessPoint('ap1', ssid='Antenna1', 
        mode='a', channel=channelAP1, position=positionAP1,range=rangeAP1,antennaGain=antennaGainAP1,
        txpower=txpowerAP1, antennaHeight=antennaHeightAP1)

    ap2 = net.addAccessPoint('ap2', ssid='Antenna2',
        mode='a', channel=channelAP2, position=positionAP2,range=rangeAP2,antennaGain=antennaGainAP2,
        txpower=txpowerAP2, antennaHeight=antennaHeightAP2)

    ap3 = net.addAccessPoint('ap3', ssid='Antenna3',
        mode='a', channel=channelAP3, position=positionAP3,range=rangeAP3,antennaGain=antennaGainAP3,
        txpower=txpowerAP3, antennaHeight=antennaHeightAP3)

    c1 = net.addController('c1', controller=Controller)
    net.propagationModel(model="logNormalShadowing", exp=3)
    info("*** Configuring wifi nodes\n")
    net.configureWifiNodes()

    net.plotGraph(max_x=100, max_y=100)

    info("*** Starting network\n")
    net.build()
    c1.start()
    ap1.start([c1])
    ap2.start([c1])
    ap3.start([c1])
    ap10.start([c1]) #Mobile from ap10 forward

    #AP1 TO MODE MONITOR
    ap1.cmd("ifconfig ap1-wlan1 down")
    ap1.cmd('iwconfig ap1-wlan1 mode monitor')
    ap1.cmd('ifconfig ap1-wlan1 up')

    #AP2 TO MODE MONITOR
    ap2.cmd("ifconfig ap2-wlan1 down")
    ap2.cmd('iwconfig ap2-wlan1 mode monitor')
    ap2.cmd('ifconfig ap2-wlan1 up')
    
    #AP3 TO MODE MONITOR
    ap3.cmd("ifconfig ap3-wlan1 down")
    ap3.cmd('iwconfig ap3-wlan1 mode monitor')
    ap3.cmd('ifconfig ap3-wlan1 up')

    info("*** Running CLI\n")
    CLI_wifi(net)

    info("*** Stopping network\n")
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    topology()
