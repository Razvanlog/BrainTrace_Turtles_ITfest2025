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
ok=1
if ok==1:
    conn=sqlite3.connect(db_filename)
    cursor=conn.cursor()
    cursor.execute('SELECT  FROM myapp_patientdata')
    conn.commit()
    rows=cursor.fetchall()
    
    
    #WORKS
    model=tf.keras.models.load_model('brain_tumor_version2.keras')
    photo_location='archive/Testing/notumor/Te-no_0010.jpg'
    image_string=tf.io.read_file('/home/razvan/repos/itfest2025_AImodeltraining/'+photo_location)
    image=tf.image.decode_image(image_string,channels=3)
    target_size=(128,128)
    image=tf.image.resize(image,target_size)
        # image=tf.image.convert_image_dtype(image,tf.float32)
        # image=(image-127.5)/127.5
        # result=model.predict(image)
        # print(image.shape)
    result=-1
    if image.shape==(128,128,3):
        image=tf.expand_dims(image,axis=0)
            # dataset=tf.data.Dataset.from_tensor_slices(image)
            # dataset=dataset.batch(1)
            # print(dataset)
        result=model(image)
        print(np.argmax(result,axis=1))
    print(result,'succes')
    arr=['Glioma','Meningioma','No tumor','Pituitary']
    pos=0
    strResult=arr[np.argmax(result,axis=1)[0]]



    # print(strResult)
    # for i in list(result):
    #     if i==True:
    #         strResult=arr[pos]
    #     pos+=1
    # strResult=arr[tf.where(tf.equal(result,1))]

    # print('succes')
    for i in rows:
        (number,photo_location,f_name,l_name,receiver_email,age)=i
        ok=0
        im=Image.open('/home/razvan/repos/isic_2024/web_site/isic/media'+photo_location)
        width,height=im.size
        fwidth,fheight=(128,128)
        left=width//2-fwidth//2
        right=width//2+fwidth//2
        top=height//2-fheight//2
        bottom=height//2+fheight//2
        im=im.crop((left,top,right,bottom))
        im.save('/home/razvan/repos/isic_2024/web_site/isic/media'+photo_location)
        photo_location='archive/Testing/notumor/Te-no_0010.jpg'
        # image_string=tf.io.read_file('/home/razvan/repos/itfest2025_AImodeltraining/'+photo_location)
        # image=tf.image.decode_image(image_string,channels=3)
        # target_size=(128,128)
    #     image=tf.image.resize(image,target_size)
    #     # image=tf.image.convert_image_dtype(image,tf.float32)
    #     # image=(image-127.5)/127.5
    #     # result=model.predict(image)
    #     # print(image.shape)
    #     result=-1
    #     if image.shape==(128,128,3):
    #         image=tf.expand_dims(image,axis=0)
    #         # dataset=tf.data.Dataset.from_tensor_slices(image)
    #         # dataset=dataset.batch(1)
    #         # print(dataset)
    #         result=model(image)
    #         print(np.argmax(result,axis=1))
    #     print(result,'succes')
    #     # if ok==1:
    #     #     smtp_server='smtp.gmail.com'
    #     #     port=587
        #     sender_email='webemailt@gmail.com'
        #     message=MIMEText('Hello World!')
        #     context=ssl.create_default_context()
        #     print('ok')
        #     with smtplib.SMTP(smtp_server,port) as server:
        #         print('ok')
        #         server.ehlo()
        #         print('ok')
        #         server.starttls(context=context)
        #         server.ehlo()
        #         print('ok')
        #         server.login(sender_email,password)
        #         server.sendmail(sender_email,receiver_email,message.as_string())
        #         print("succes")
# # 'csim18782@gmail.com'

        # print(type(i))
# except:
#     print('cannot connect to database')

# print(rows)


    smtp_server='smtp.gmail.com'
    port=587
    sender_email='braintrace.turtles@gmail.com'
    # 'csim18782@gmail.com'
    receiver_email='razvan.diaconescu04@e-uvt.ro'
    msg=MIMEMultipart()
    from email.header import Header
    msg['subject']=Header('Your result to the MRI analysis')
    msg['From']=sender_email
    msg['To']=receiver_email
    message=MIMEText('Hello User!\n The result of the analysis of the MRI scan is '+strResult+'.')
    msg.attach(message)
   
    context=ssl.create_default_context()
    print('ok')
    with smtplib.SMTP(smtp_server,port) as server:
        print('ok')
        server.ehlo()
        print('ok')
        server.starttls(context=context)
        server.ehlo()
        # print('ok')
        server.login(sender_email,password)
        # server.sendmail(sender_email,receiver_email,msg)
        server.send_message(msg)
        print("succes")