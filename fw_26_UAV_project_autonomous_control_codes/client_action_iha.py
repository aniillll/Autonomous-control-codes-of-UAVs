#!/usr/bin/env python3
# -*- coding: utf-8-*-
import rospy
import actionlib
import time
from ogretici_paket.msg import IhaDurumAction,IhaDurumActionGoal #BİZ BURADA bir istek gönderdiğimiz için bununla ilgili mesaja ihtiyacımız var bu da IhaDurumActionGoal oluyor ve IhaDurum.action dosyamızı tanımladık.
from std_msgs.msg import String
from sensor_msgs.msg import BatteryState
from sensor_msgs.msg import FluidPressure
from sensor_msgs.msg import Imu
from sensor_msgs.msg import JointState
from sensor_msgs.msg import NavSatFix
from sensor_msgs.msg import NavSatStatus
from sensor_msgs.msg import Temperature
from mavros_msgs.srv import *
#global variable
latitude =0.0
longitude=0.0
print(time.strftime('%H:%M:%S'))  # saat dakika saniye şeklinde verilmiş

a = int(time.strftime('%M'))  # suan ki zamandaki  dakikayı a değerine atadım
b = a + 15
""""burada bilgisayar satimizi kullanarak oradaki dk bilgisine 15 dk ekleyecek ve şimiki
    zamanı bir b değerine atarak bir işlemin 15dk boyunca yapılmasını sağladım.
"""
def setAUTOMode(mode_uav):
    rospy.wait_for_service('/mavros/set_mode')
    try:
        flightModeService = rospy.ServiceProxy('/mavros/set_mode', mavros_msgs.srv.SetMode)
        # http://wiki.ros.org/mavros/CustomModes for custom modes
        isModeChanged = flightModeService(custom_mode=str(mode_uav))  # return true or false
     except rospy.ServiceException:
        print("service set_mode call failed: GUIDED Mode could not be set. Check that GPS is enabled")
def setStabilizeMode():
    rospy.wait_for_service('/mavros/set_mode')
    try:
        flightModeService = rospy.ServiceProxy('/mavros/set_mode', mavros_msgs.srv.SetMode)
        # http://wiki.ros.org/mavros/CustomModes for custom modes
        isModeChanged = flightModeService(custom_mode='STABILIZE')  # return true or false
    except rospy.ServiceException:
        print("service set_mode call failed:  GUIDED Mode could not be set. Check that GPS is enabled")


def setLandMode():
    rospy.wait_for_service('/mavros/cmd/land')
    try:
        landService = rospy.ServiceProxy('/mavros/cmd/land', mavros_msgs.srv.CommandTOL)
        # http://wiki.ros.org/mavros/CustomModes for custom modes
        isLanding = landService(altitude=0, latitude=0, longitude=0, min_pitch=0, yaw=0)
    except rospy.ServiceException:
        print("service land call failed: The vehicle cannot land " )

def setArm(arm):
    rospy.wait_for_service('/mavros/cmd/arming')
    try:
        armService = rospy.ServiceProxy('/mavros/cmd/arming', mavros_msgs.srv.CommandBool)
        armService(arm)
    except rospy.ServiceException:
        print("Service arm call failed: ")


def setDisarm():
    rospy.wait_for_service('/mavros/cmd/arming')
    try:
        armService = rospy.ServiceProxy('/mavros/cmd/arming', mavros_msgs.srv.CommandBool)
        armService(False)
    except rospy.ServiceException:
        print("Service arm call failed: %s")


def setTakeoffMode(altitude_a):
    rospy.wait_for_service('/mavros/cmd/takeoff')
    try:
        takeoffService = rospy.ServiceProxy('/mavros/cmd/takeoff', mavros_msgs.srv.CommandTOL)
        takeoffService(altitude=altitude_a, latitude=0, longitude=0, min_pitch=0, yaw=0)
    except rospy.ServiceException:
        print("Service takeoff call failed" )


def globalPositionCallback(globalPositionCallback):
    global latitude
    global longitude
    latitude = globalPositionCallback.latitude
    longitude = globalPositionCallback.longitude
    # print ("longitude: %.7f" %longitude)
    # print ("latitude: %.7f" %latitude)

def bildirimfonksiyonu(bilgi):#serverdan gelen feed back ile ne yapacağımızı tanımladığımız fonksiyon
    print("Görev tamamlama Durumu:",bilgi.gecen_sure)#geri bildirimimizi bilgi altındaki oran bölümünden bastır dedik:
                                               #GorevDurum.action dosyasındaki en alt satırda bulunan  string tipindeki oran adındaki değişkenimizi kullanrak bastırdık
    c=int(time.strftime('%M'))
    mod_param=setAUTOMode("AUTO")
    arm_param=setArm(True)
    print_message_func()
    while (c < bilgi.gecen_sure):
        if(mod_param==True):
            if (arm_param== True):
                took_off=setTakeoffMode(10)#kaç metre yükseleceğinibelirttik.
                if took_off==True:
                    print_message_func()

                else:
                    took_off=setTakeoffMode(10)

            else:
                arm_param=setArm(True)

        else:
            mod_param=setAUTOMode("AUTO")
def print_message_func(battey,fluid_pressure,ımu,joınt_state,navsatfix,navsat_status,temperature) :
    print(battey.percentage)
    print(fluid_pressure.percentage)
    print(ımu.orientation_covariance)
    print(ımu.angular_velocity_covariance)
    print(ımu.linear_acceleration_covariance)
    print(joınt_state.position)
    print(joınt_state.velocity)
    print(joınt_state.effort)
    print(navsatfix.latitude)
    print(navsatfix.longitude)
    print(navsatfix.altitude)
    print(navsat_status)
    print(temperature)


def subscirber_func():
    rospy.init_node("iha_abone_dugumu", anonymous=True)#subscirber node defined
    rospy.Subscriber("/mavros/battey/fluid_presuure/Imu/joint_state/NavSatFix/NavSatStatus/Temperature",BatteryState,FluidPressure,Imu,JointState,NavSatFix,NavSatFix,Temperature,print_message_func)

def istekteBulun():
    rospy.init_node("iha_istemci_dugumu")
    istemci=actionlib.SimpleActionClient("görev",IhaDurumAction)#action client tanımladık serverdan gelen cevabı alacak ve GorevDurumAction tipinde olacak actionlib.SimpleActionClient("görev(bunu server da tanımladık bunun aracılığı ile haberleşecek server-client)",GorevDurumAction)

    istemci.wait_for_server()#servis aktif olana kadar bekle dedik

    istek1=IhaDurumActionGoal() #SERVER A gönderilecek ilk istek için istek tipinde IhaDurumActionGoal() fonksiyonunu kullanarak istek oluşturduk.
    istek1.iha_flight_start_time=b#IhaDurum.action dosyasında istemcinin göndereceği mesajı tanımladık orada int32 tipinde iha_flight_start_time adında istek oluşturma parametremizi kullandık.
    istemci.send_goal(istek1,feedback_cb=bildirimfonksiyonu)#ilk istegimizi servera istemci.send_goal(istek) fonksiyonu ile gönderdik;istemci.send_goal(istek,feedback_cb=bildirimfonksiyonu) nunda ayrıca bir
                                                           #geri bildirim alacaksak bu geri bildirimle ne yapayım kısmında feedback_cb=bildirimfonksiyonu tanımlamasıyla oluşturduğumuz
                                                           #bildirimfonksiyonu ile ne yapacağımızı tanımlayacağız

    """
    burada istemci 2 tane istek bilgisi gönderiyor server a ilki ihanın real time kalkış  dakikası,ikinci istek bilgisi ise ihanın real time inmesi gereken süreyi gönderiyor
    istemciye.
    İlk istek bilgimi alan server feedback oluşturacak son istemci bilgisi süresine kadar.
    """

    istemci.wait_for_result()#sonuc gelene kadar bekleyeceğiz
    x=istemci.get_result().sonuc #eğer bir sonuç varsa istemci.get_result().sonuc bu fonksiyonla sonucu alacağım yani serverin döndürdüğü cevabı alacağız (buradaki .sonuc ifadesi GorevDurum.action dosyasındaki
                               #ikinci satırda bulunan string tipindeki sonuc parametresidir,cevap bu yolla iletilir.
    return x


result=istekteBulun()
print("Görevin son durumu :",result)