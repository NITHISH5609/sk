import numpy as np # mathematical operations
import imutils # resize the image
import cv2 #image accqracy
import time # delay 

prototxt = "MobileNetSSD_deploy.prototxt.txt" #load the model
model = "MobileNetSSD_deploy.caffemodel" #load the model
confThresh = 0.2 # to chech the object present or not

CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
	"bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
	"dog", "horse", "motorbike", "person", "pottedplant", "sheep",
	"sofa", "train", "tvmonitor","key"] # this object only identify
COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3)) # to assign color

print("Loading model...") #load the model files
net = cv2.dnn.readNetFromCaffe(prototxt, model)
print("Model Loaded")
print("Starting Camera Feed...")
vs = cv2.VideoCapture(0) #camera inilization
time.sleep(2.0)

while True:
	_, frame = vs.read()
	frame = imutils.resize(frame, width=500)

	(h, w) = frame.shape[:2]
	imResizeBlob = cv2.resize(frame, (300, 300))
	blob = cv2.dnn.blobFromImage(imResizeBlob,
		0.007843, (300, 300), 127.5)

	net.setInput(blob)
	detections = net.forward()
	detShape = detections.shape[2]
	for i in np.arange(0, detShape):
		confidence = detections[0, 0, i, 2]
		if confidence > confThresh:
			idx = int(detections[0, 0, i, 1])
			print("ClassID:", detections[0, 0, i, 1])
			box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
			(startX, startY, endX, endY) = box.astype("int")

			label = "{}: {:.2f}%".format(CLASSES[idx],
				confidence * 100)
			cv2.rectangle(frame, (startX, startY), (endX, endY),
				COLORS[idx], 2)
			y = startY - 15 if startY - 15 > 15 else startY + 15
			cv2.putText(frame, label, (startX, y),
				cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)

	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1)
	if key == 27:
		break
vs.release()
cv2.destroyAllWindows()
