import cv2
#!/usr/bin/env python3
# -*- coding: utf-8-*-
import rospy
import time
from std_msgs.msg import String
from sensor_msgs.msg import BatteryState
from sensor_msgs.msg import FluidPressure
from sensor_msgs.msg import Imu
from sensor_msgs.msg import NavSatFix
from sensor_msgs.msg import Temperature
from mavros_msgs.srv import *
#global variable
#latitude =0.0
#longitude=0.0
#a = int(time.strftime('%M'))  # suan ki zamandaki  dakikayı a değerine atadım
#b = a+ 15

class deneme():
    def __init__(self):

        #publisher node
        rospy.init_node("İha_İHA_Durum_ügümü", anonymous=True)
        Publisher_NavSatFix=rospy.Publisher("mavros/global_position/global",NavSatFix)1
        global_pos=NavSatFix()


        # subscriber node

        Subscriber_battery= rospy.Subscriber("mavros/battery ",BatteryState,self.battery_prınt)
        Subscriber_fluid_pressure=rospy.Subscriber("mavros/imu/diff_pressure",FluidPressure,self.fluıd_pressure_prınt)
        Subscriber_NavSatFix=rospy.Subscriber("mavros/global_position/global",NavSatFix,self.global_pos_print)


        while(a<=b):

            Publisher_NavSatFix.publish(global_pos)


    def battery_prınt(self,battery_message):
        print(battery_message.percentage)


    def fluıd_pressure_prınt(self,compass):
        print(compass.fluid_pressure)


    def global_pos_print(self,coordinate):
        print(coordinate.longitude)
        print(coordinate.altitude)
        print(coordinate.longitude)





