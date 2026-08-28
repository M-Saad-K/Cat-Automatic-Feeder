import cv2
from picamera2.encoders import H264Encoder
from picamera2 import Picamera2
import time
import os

picam2 = Picamera2()
video_config = picam2.create_video_configuration()
picam2.configure(video_config)
encoder = H264Encoder(bitrate=10000000)

# Ntfy_Server Info
NTFY_SERVER = "https://ntfy.sh"
NTFY_TOPIC_NAME = "Unique Topic Name Goes Here" # Put your topic there TODO: Remeber to add and remove this before git commits

# Save directory
save_directory = "image-save-folder"#
os.makedirs(save_directory, exist_ok = True)

thres = 0.50 # Threshold to detect object

classNames = []
classFile = "detection-model-library/coco.names"
with open(classFile,"rt") as f:
    classNames = f.read().rstrip("\n").split("\n")

configPath = "detection-model-library/ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt"
weightsPath = "detection-model-library/frozen_inference_graph.pb"

net = cv2.dnn_DetectionModel(weightsPath,configPath)
net.setInputSize(320,320)
net.setInputScale(1.0/ 127.5)
net.setInputMean((127.5, 127.5, 127.5))
net.setInputSwapRB(True)

def getObjects(img, thres, nms, draw=True, objects=[]):
    classIds, confs, bbox = net.detect(img,confThreshold=thres,nmsThreshold=nms)
    #print(classIds,bbox)
    if len(objects) == 0: objects = classNames
    objectInfo =[]
    if len(classIds) != 0:
        for classId, confidence,box in zip(classIds.flatten(),confs.flatten(),bbox):
            className = classNames[classId - 1]
            if className in objects:
                objectInfo.append([box,className])
                if (draw):
                    cv2.rectangle(img,box,color=(0,255,0),thickness=2)
                    cv2.putText(img,classNames[classId-1].upper(),(box[0]+10,box[1]+30),
                    cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
                    cv2.putText(img,str(round(confidence*100,2)),(box[0]+200,box[1]+30),
                    cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)

                    # Implement a timer
                    length = 0
                    start = time.time()

                    if className == "cat":

                        send_ntfy_notification(cat, )

                        # Notification is sent, told that it will wait for period for another notification
                        while length != 60:
                            end = time.time()   
                            length = end - start

                    if className == "bird":
                        print("Bird Detected")
                        # Notification is sent, told that will wiat for period for another notification
                        while length != 60:
                            end = time.time()   
                            length = end - start

    return img,objectInfo


if __name__ == "__main__":

    picam2.start()

    while True:
        img = picam2.capture_array()
        img = cv2.cvtColor(img, cv2.COLOR_RGBA2BGR)
        result, objectInfo = getObjects(img,0.45,0.2, objects=['cat', 'bird'])
        #print(objectInfo)
        cv2.imshow("Output",img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    picam2.stop()
    cv2.destroyAllWindows()