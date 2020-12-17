#!/usr/bin/env python3



import RPi.GPIO as GPIO
import time
import smtplib
import picamera
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.multipart import MIMEBase
from email import encoders
import os

#setup GPIO pin
pirPin = 17


def setup():

	GPIO.setmode(GPIO.BCM)		# Set the GPIO modes to BCM Numbering
	GPIO.setup(pirPin, GPIO.IN)    # Set pirPin to input
	
def user_email():
    add = input()
    return add

def email_sender():
    #This is  a path that pictures were capture there.
    #we need that path to find and email pictures
    files = os.listdir("/home/pi/Desktop")

    extension = "jpg"
    for file in files:
        if extension in file: #code just find the file with .jpg extention in the path we have
            user ="alexmorti6060@gmail.com" #sending gmail
            recv ="arefshiran1616@gmail.com" #receiving gmail
            subject = "Someone enter to Your room" #subject of email message
            message = MIMEMultipart()
            message["From"] = user
            message["To"] = recv
            message["Subject"]= subject
            #titel of email set here.
            body = "This person enter your room!!"
            message.attach(MIMEText(body,"plain"))
            attachment = open(file,"rb")
            part = MIMEBase("application","octet-stream")
            part.set_payload((attachment).read())
            encoders.encode_base64(part)
            part.add_header("Content-Disposition","attachment;filename= " + file)
            #Attach the massge now.
            message.attach(part)
            text = message.as_string()
            #587 SMTP port is for emails
            server = smtplib.SMTP("smtp.gmail.com",587)
            server.starttls()
            server.login(user,"********")
            server.sendmail(user,recv,text)
            server.quit()
        else:
            pass


#This function is for camera that take 6 pictures
def camera_take():
    with picamera.PiCamera() as camera:
        camera.capture('roomperson1.jpg')
        camera.capture('roomperson2.jpg')
        camera.capture('roomperson3.jpg')
        camera.capture('roomperson4.jpg')
        camera.capture('roomperson5.jpg')
        camera.capture('roomperson6.jpg')



#program start here and functions called
def starter():
    while True:

        pir_val = GPIO.input(pirPin)
        #tester = False

        if pir_val==GPIO.HIGH:
            tester = True
            print("Someone Here!!")
            camera_take()
            email_sender()
            continue


#This function finish the program and will reset GPIO sensor
def destroy():
	GPIO.cleanup()







if __name__ == '__main__':     # Program start from here

    print("Hi welcome to my program this program will take pictures if who ever enter too your room")

	setup()
	try:
		starter()
	except KeyboardInterrupt:
		destroy()
