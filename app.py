import cv2
from imutils.io import TempFile
from datetime import datetime
from datetime import date
import imutils
import time
import os, os.path
from azure.storage.blob import ContainerClient
from azure.storage.blob import BlobClient

CONNECT_STR = ""
CONTAINER_NAME = "blobtest"

container_client = ContainerClient.from_connection_string(conn_str=CONNECT_STR, container_name=CONTAINER_NAME)

faceDetect = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
camera = cv2.VideoCapture(0)
trigger = False
notifSent = False
writer = None
iterate = 0
while(True): 
    _,frame = camera.read()
    triggerPrev = trigger
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    faces = faceDetect.detectMultiScale(gray,1.2,5)

    if faces!=():
        trigger = True
    else:
        trigger = False

    if (trigger and not triggerPrev):
        startTime = datetime.now()
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        filename = "video/{}_{}.avi".format(startTime.strftime('%A'),iterate)
        file_blob = "{}_{}.avi".format(startTime.strftime('%A'),iterate)
        writer = cv2.VideoWriter(filename,fourcc,20,(640,480))
    elif triggerPrev:
        timeDiff = (datetime.now() - startTime).seconds
        if trigger and timeDiff > 20:
            if not notifSent:
                # build the message and send a notification
                msg = "Intruder alert"
				# release the video writer pointer and reset the
				# writer object
                writer.release()
                writer = None
				
				# send the message and the video to the owner and
				# set the notification sent flag
				# tn.send(msg, tempVideo)
                notifSent = True
        if not trigger:
            # if a notification has already been sent, then just set 
			# the notifSent to false for the next iteration
            if notifSent:
                notifSent = False
            else:
                # record the end time and calculate the total time in
                # seconds
                endTime = datetime.now()
                totalSeconds = (endTime - startTime).seconds
                dateOpened = date.today().strftime("%A, %B %d %Y")
                # build the message and send a notification
                if totalSeconds>=3:
                    msg = "Someone is looking at your door {} at {} " \
                            "for {} seconds.".format(dateOpened,startTime.strftime("%I:%M%p"), totalSeconds)
                    iterate += 1
                    writer.release()
                    writer = None
                    # tn.send(msg, tempVideo)
                    
                    print(msg)
    if writer is not None:
        writer.write(frame)

    for (x,y,w,h) in faces:
        cv2.rectangle(frame,(x,y), (x+w,y+h),(0,255,0),2)

    cv2.imshow("Face",frame);

    if(cv2.waitKey(1) ==ord('q')):
        break;
# check to see if we need to release the video writer pointer
if writer is not None:
    writer.release()

if iterate!=0:
    file_list = os.listdir('video/')
    for i in range(len(file_list)):
        input_file_path = 'video/{}'.format(file_list[i])
        output_blob_name = file_list[i]
        blob = BlobClient.from_connection_string(conn_str=CONNECT_STR, container_name=CONTAINER_NAME, blob_name=output_blob_name)
        exists = blob.exists()
        if exists:
            print("File already exist!")
        else:
            with open(input_file_path, "rb") as data:
                container_client.upload_blob(name=output_blob_name, data=data)
            print("Upload file",i,",Succsess")


camera.release()
cv2.destroyAllWindows()
