import cv2
import numpy as np
import geopy
from geopy.distance import VincentyDistance

def mouse_select(event, x, y, flags, params):
	if event == cv2.EVENT_LBUTTONDOWN:
		sbox = [x, y]
	elif event == cv2.EVENT_LBUTTONUP:
		ebox = [x, y]

def create_box():
	count = 0
	while(1):
		count+=1
		img = cv2.imread('frame.jpeg',0)
		cv2.namedWindow('real image')
		cv2.setMouseCallback('real image', mouse_select,0)
		cv2.imshow('real image', img)
		if count < 50:
			if(cv2.waitKey(33) == 27):
				cv2.destroyAllWindows()
				break
		elif count >= 50:
			if(cv2.waitKey(0) == 27):
				cv2.destroyAllWindows()
				break
		count = 0	

def get_drone_loc():
	with open('data.txt', 'r') as f:
		data = f.readlines()
	for line in data:
		line_s = line.split()
	lat, lon, alt,  bearing = line_s[4], line_s[3], line_s[6], line_s[5]

hvf=88.3560
vfv=56.8858

def distance():
	h_angle=hvf/2
	width=2*alt*tan(h_angle)
	v_angle=vfv/2
	length=2*alt*tan(v_angle)
	dpp_w=width/1080
	dpp_l=length/720
	#co ordinates of destination point
	x=sbox[0]+ebox[0]
	y=sbox[1]+ebox[1]
	x1=360-x
	y1=540-y
	x_dis=x1*dpp_l
	y_dis=y1*dpp_w
	dis=(x_dis^2 + y_dis^2)^0.5

def new_coordinates(dis):
	start=geopy.Point(lat,lon)
	d=geopy.distance.VincentyDistance(dis)
	print(d.destination(point=start,bearing=bearing))
	

cap = cv2.VideoCapture(0)
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi',fourcc, 20.0, (640,480))
while (cap):
	ret, frame = cap.read()
	cv2.imshow('video recording', frame)

	if cv2.waitKey(1) and 0xFF == ord('q'):#quit
		break
	if cv2.waitKey(1) and 0xFF == ord('p'):#Pause
		isRecording=False
		cv2.imshow("frame.jpeg",frame)
		create_box()
		get_drone_loc()
		distance()
		new_coordinates()
		while(1):
			if cv2.waitKey(1) and 0xFF == ord('c'):#Continue
				isRecording=True
# When everything done, release the capture
cap.release()
out.release()
cv2.destroyAllWindows()