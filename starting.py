import serial
import urllib.request as ur
import cv2
import numpy as np
from time import sleep
from datetime import datetime
import pytz
import smtplib
import imghdr
from email.message import EmailMessage

Sender_Email = "viktoria4566r@gmail.com"
Reciever_Email = "alexmailpro@yandex.ru"
Password = "Qwerty23R"

url='http://192.168.31.55:8080/shot.jpg'
serial = serial.Serial("/dev/ttyS0", timeout=None, baudrate=9600)
serial.flushInput()                  

while 1:
    if serial.inWaiting():
        print("ALERT")
        serial.flushInput()
 
        imgResp = ur.urlopen(url)
        imgNp = np.array(bytearray(imgResp.read()),dtype=np.uint8)
        img = cv2.imdecode(imgNp,-1)
        current_time = datetime.now().astimezone(pytz.timezone("Europe/Moscow")).strftime("%H:%M:%S")
        image_name = f'alert {current_time}.jpg'
        cv2.imwrite(image_name, img)
        
        newMessage = EmailMessage()                         
        newMessage['Subject'] = "Someone has entered your home!!!!" 
        newMessage['From'] = Sender_Email                   
        newMessage['To'] = Reciever_Email 
        newMessage.set_content(f'Save your home {current_time}')
        
        with open(image_name, 'rb') as f:
            image_data = f.read()
            image_type = imghdr.what(f.name)
            pic_name = f.name
            
        newMessage.add_attachment(image_data, maintype='image', subtype=image_type, filename=pic_name)
        
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(Sender_Email, Password)              
            smtp.send_message(newMessage)
        
    sleep(1)
