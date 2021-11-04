import cv2
"""import numpy       #ros ile çalıştığımız için numpy lib import ettik
import actionlib  #aksiyonlarla çalıştığımız için action lib import ettik
import rospy
import time
from mavros_msgs.srv import *
from ogretici_paket.msg import IhaDurumAction,IhaDurumFeedback,IhaDurumResult
from sensor_msgs.msg import BatteryState
from sensor_msgs.msg import FluidPressure
from sensor_msgs.msg import Imu
from sensor_msgs.msg import JointState
from sensor_msgs.msg import NavSatFix
from sensor_msgs.msg import NavSatStatus
from sensor_msgs.msg import Temperature
from std_msgs.msg import String


"""action mesajlarını kullanabilmek için ogretici_paket altındaki .msg mesajlarından IhaDurumAction mesaşlarını kullancağız
#Aksiyon dosyaları oluşturulurken 7 tane mesaj oluşturulur otomatik olarak GorevDurum mesajı en temel mesajdır bu mesajlar arasındaki
şimdi server a  mesaj gelecek ve bunu feedback verbilmem için IhaDurumFeedback mesajına ihtiyacım var birde GorevDurumResult mesajlarına ihtiyacımız var"""
class Actionserver():
    def __init__(self):
        rospy.init_node("iha_action_server_dügümü")#düğümümüzü oluşturduk
        self.a_server=actionlib.SimpleActionServer("görev",IhaDurumAction,execute_cb=self.cevapUret) #action server oluşturduk action lib kullanarak ve bunuda self.a_server'a atadık  actionlib.SimpleActionServer("server_name",IhaDurumAction(hangi tipteki mesajı kullanıcaz onu yaz yukarıda import ettik bunu),execute_cb=self.cevapUret(mesaj geldiğinde ne yap bunu tanımladık,bu tanımlama özel bir tanımlama))
        #execute_cb=self.cevapUret bu işlem bizim feedback bölümümüzü oluşturuyor,sürekli bir geri bildirim verebilmek için kullanıyoruz.
        self.a_server.start()#bu oluşturduğumuz server ı başlattık.
        rospy.spin()#bu komutla bu başlatma işlemin sürekli yapılmasını sağladık

    def mesajYayınla(self):  # tüm işlemlerimizi yapacağımız bir ana fonksiyon tanımladım.
        rospy.init_node("İha_yayinci_dügümü",anonymous=True)  # yayıncı düğümü adı verdiğim bir düğüm başlattım.Düğüm başlatma fonsiyonu: rospy.init_node("düğüm adı",anonymous=True) ,sodaki ifade fonksiyondaki düğümü benzersiz hale getirdik.(başka bir düğüm bu isimde tanımlanamazdedik)
        self.Publisher= rospy.Publisher("/mavros/battey/fluid_presuure/Imu/joint_state/NavSatFix/NavSatStatus/Temperature",BatteryState,FluidPressure,Imu,JointState,NavSatFix,NavSatFix,Temperature)  # Publisher adında BİR YAYINCI OLUŞTURDUK rospy.Publisher("YAYINCI KONUSUNU YAZIYORUZ BURAYA",Buraya yayınlayacağımız mesajın adını yazıyoruz(yukarıda import ettiğimiz)) FONKSİYONUNU KULLANARAK
    def cevapUret(self,istek):#bir istek geldiğinde bu işlemi yapacak bu yüzden istek diye parametremizi tanımladık
        #biz burada bir istek geldiğinde yüzde olarak sürekli ne kadar mesafe gidildiğini feedback vericez ve birde Result ,vericez bu işemi yapmak istiyoruz
        geri_bildirim=IhaDurumActionFeedback()  #feedback verme işlemimizi tanımlıyoruz
        sonuc=IhaDurumResult()          #sonuç verme işlemimizi tanımlıyoruz
        rate=rospy.Rate(1)#sonuc ve geri bildirim verme işlemini sn de 1 kere vermesini istiyoruz istemciye
        #şimdiki zamanın dakikasını alıyoruz pc den
        print(time.strftime('%H:%M:%S'))  # saat dakika saniye şeklinde verilmiş
        c= int(time.strftime('%M'))  # suan ki zamandaki  dakikayı a değerine atadım

        for i in range(c,istek.iha_flight_end_time):#GorevDurum.action dosyasında tanımladığımız birim parametresini kullanıcaz,birim bize bu işlemin nerede biteceğini söylüyor
            durum="gecen_sure:"+str(istek.iha_flight_end_time-c)#bu bize işin yüzde kacının yapıldığını söyleyecek
            geri_bildirim.oran=durum#durum değişkeninin(GörevDurum.action dosyasında tanımladığımız) oran parametresini buraya atayarak biz geri bildirim vermiş olduk
            self.a_server.publish_feedback(geri_bildirim)#geri bildirim değerimizi yayınladık bu ifadeyle
            rate.sleep()#ile sn de bir kere geri bildirimi yayınlamış olduk
            c = int(time.strftime('%M'))

        sonuc.sonuc="görev tamamlandı"#burada istemciye gönderilecek cevap içeriği olan görev tamamlandı sonucuna atadık (sonuc(sonuc=GorevDurumResult())un altındaki sonuc parametresi ile serverdan(GorevDurum.action orta satır) istemci(cliente)'ye geri döndürelecek cevapı atamış olduk)
        self.a_server.set_succeeded(sonuc)#serverdan istemciye cevap olarak gönderilecek sonuc parametresini gönderdik
a_s=Actionserver()#A_S ADINDAKİ NESNE TANIMLAMAMIZI YAPTIK
"""
image=cv2.imread("")


