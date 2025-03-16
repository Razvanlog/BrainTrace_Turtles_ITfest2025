import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import tensorflow as tf
import keras
import socket
import sqlite3
import time
import shutil
import numpy as np
from PIL import Image
db_filename='/home/razvan/repos/itfest2025_AImodeltraining/BrainTrace_Turtles_ITfest2025_site/demo/db.sqlite3'
photo_storage='/home/razvan/repos/itfest2025_AImodeltraining/BrainTrace_Turtles_ITfest2025_site/demo/media/'
# '/tumor_images/'
ok=1
if ok==1:
    conn=sqlite3.connect(db_filename)
    cursor=conn.cursor()
    cursor.execute('SELECT first_name,last_name,email,tumor_image FROM myapp_patientdata')
    conn.commit()
    rows=cursor.fetchall()
    #WORKS
    model=tf.keras.models.load_model('brain_tumor_version2.keras')
    smtp_server='smtp.gmail.com'
    port=587
    sender_email='braintrace.turtles@gmail.com'
    for i in rows:
        (fname,lname,email,photo_location)=i
        ok=0
        if photo_location!="" or photo_location!=None:
            # print(photo_storage+" "+photo_location)
            try:
                im=Image.open(photo_storage+photo_location)
                width,height=im.size
                fwidth,fheight=(128,128)
                left=width//2-fwidth//2
                right=width//2+fwidth//2
                top=height//2-fheight//2
                bottom=height//2+fheight//2
                im=im.crop((left,top,right,bottom))
                im.save(photo_storage+photo_location)
                im_string=tf.io.read_file(photo_storage+photo_location)
                img=tf.image.decode_image(im_string,channels=3)
                target_size=(128,128)
                img=tf.image.resize(img,target_size)
                result=-1
                if img.shape==(128,128,3):
                    img=tf.expand_dims(img,axis=0)
                    result=model(img)
                print('succes')
                arr=['Glioma','Meningioma','No tumor','Pituitary']
                strResult=arr[np.argmax(result,axis=1)[0]]
                print(strResult)
                receiver_email=email
                msg=MIMEMultipart()
                from email.header import Header
                msg['subject']=Header('Your result to the MRI analysis')
                msg['From']=sender_email
                msg['To']=receiver_email
                message=MIMEText('Hey '+fname+' '+lname+',\n The result of the analysis of the MRI scan is '+strResult+'.')
                msg.attach(message)
                password='asxyyoywyunwpedh'
                context=ssl.create_default_context()
                print('ok')
                with smtplib.SMTP(smtp_server,port) as server:
                    print('ok')
                    server.ehlo()
                    print('ok')
                    server.starttls(context=context)
                    server.ehlo()
                    server.login(sender_email,password)
                    server.send_message(msg)
                    print("succes"+" "+receiver_email)
            except:
                a=0