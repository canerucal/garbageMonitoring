import RPi.GPIO as GPIO
import time
from PyQt5 import QtWidgets,uic, QtGui
from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
from PyQt5.QtCore import *
from PyQt5.QtGui import QPixmap
import sys
import cv2 as cv
import MySQLdb
import time
from datetime import timedelta, datetime

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

TRIG = 23
ECHO = 24

print ("HC-SR04 mesafe sensoru")

GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)

db = MySQLdb.connect("localhost","root","123456","Garbage")
insertrec = db.cursor()
sqlquery = "update Garbage set FinishTime = %s where StartTime = %s"
sqlquery1 = "insert into Garbage(StartTime) values(%s)"
class Ui(QtWidgets.QMainWindow):
    # self ile ilgili sınıfa ait metodları ya da parametreleri kullanacağımızı işaret ederiz
    def __init__(self):
        # bir nesne çağırdığınızda otomatik olarak çalışacak ve
        # sadece nesneyi ilk oluşturduğunuzda çalışacak olan bir fonksiyon __init__()
        super(Ui, self).__init__()
        
        uic.loadUi('MainWindow.ui', self)  # Sayfamızı yüklüyoruz.
        self.setImage('/home/tunahan/Desktop/Ödev/0.jpeg')
        
        self.label.setText("Garbage is free")
        self.timer = QTimer()
        # set timer timeout callback function
        self.timer.timeout.connect(self.function)
        self.controlTimer()
    def controlTimer(self):
        # if timer is stopped
        if not self.timer.isActive():
            
            # start timer
            self.timer.start(20)
            


        # if timer is started
        else:
            # stop timer
            self.timer.stop()
            

    def setImage(self, path):

        self.Image.setPixmap(QPixmap(path).scaled(150,200))
        
    def function(self):
        binCapacity = "Empty"
        #while True:
        global val1
        GPIO.output(TRIG, False)
        #print ("Olculuyor...")
        time.sleep(2)

        GPIO.output(TRIG, True)
        time.sleep(0.00001)
        GPIO.output(TRIG, False)
        while GPIO.input(ECHO)==0:
            pulse_start = time.time()

        while GPIO.input(ECHO)==1:
             pulse_end = time.time()

        pulse_duration = pulse_end - pulse_start

        distance = pulse_duration * 17150
        distance = round(distance, 2)

        if distance > 2 and distance < 400:
             
            if distance <= 20 and distance > 0:
                   if binCapacity == "Empty":
                       binCapacity = "Full"
                       print("Time to take out the garbage!")
                       self.setImage('4.jpeg')
                       val = datetime.now()
                       formatted_date = val.strftime('%Y-%m-%d %H:%M:%S')
                       insertrec.execute(sqlquery, (formatted_date,val1.strftime('%Y-%m-%d %H:%M:%S')))
                       db.commit()
                       self.label.setText("Garbage is full")
                   else:
                       self.setImage('4.jpeg')
                        
            elif distance > 20:
                   if (binCapacity == "Full") & (distance > 120):
                       binCapacity = "Empty"
                       self.setImage('0.jpeg')
                       print("Thanks for emptying the garbage!")
                       self.label.setText("Garbage is empty")
                       
                       val1 = datetime.now()
                       formatted_date = val1.strftime('%Y-%m-%d %H:%M:%S')
                       insertrec.execute(sqlquery1, (formatted_date,))
                       db.commit()
                   elif distance < 50:
                       self.setImage('3.jpeg')
                       self.label.setText("%75 is full")
                   elif distance < 80:
                       self.setImage('2.jpeg')
                   elif distance < 120:
                       self.setImage('1.jpeg')
                   else:
                       self.setImage('0.jpeg')
                       self.label.setText("Garbage is empty")
                       val1 = datetime.now()
                       formatted_date = val1.strftime('%Y-%m-%d %H:%M:%S')
                       insertrec.execute(sqlquery1, (formatted_date,))
                       db.commit()
            else:
               self.setImage('0.jpeg')
               val1 = datetime.now()
               formatted_date = val1.strftime('%Y-%m-%d %H:%M:%S')
               insertrec.execute(sqlquery1, (formatted_date,))
               db.commit()
        else:
           print( "Menzil asildi")
        
app = QtWidgets.QApplication(sys.argv)
window = Ui()
window.show()
app.exec()
