#_*_coding:utf-8_*_
#!usr/bin/python3
# import the necessary packages
#命令行参数解析包
import numpy as np
import argparse
import cv2
# 3.定义各种颜色的阈值
#设置黄色的阙值
yellow_lower = np.array([156, 43, 46])
yellow_upper = np.array([180, 255, 255])
yellow_min = np.array([15, 128, 46])
yellow_max = np.array([34, 255, 255])
#设置红色的阙值
red_lower = np.array([156, 128, 46])
red_upper = np.array([180, 255, 255])
red_min = np.array([0, 128, 46])
red_max = np.array([5, 255,255])
#设置绿色的阙值
green_min = np.array([35, 128, 46])
green_max = np.array([77, 255, 255])
#设置蓝色的阙值
blue_min = np.array([100, 128, 46])
blue_max = np.array([124, 255, 255])
#设置黑色的阙值
black_min = np.array([0, 0, 0])
black_max = np.array([180, 255, 10])
#设置白色的阙值
white_min = np.array([0, 0, 70])
white_max = np.array([180, 30, 255])

cap = cv2.VideoCapture(0)
while True:
	ok, frame = cap.read()  # 读取每一帧图片
	# 图形基本转换
	frame = cv2.GaussianBlur(frame, (5, 5), 0)  # 高斯模糊
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)  # 转换 hsv
	mask = cv2.inRange(hsv, red_min, red_max)  # 生成掩膜
	# 形态学操作
	mask = cv2.erode(mask, None, iterations=2)
	mask = cv2.dilate(mask, None, iterations=2)
	mask = cv2.GaussianBlur(mask, (3, 3), 0)
	res = cv2.bitwise_and(frame, frame, mask=mask)  # 与运算
	cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
							cv2.CHAIN_APPROX_SIMPLE)[-2]  # 检测颜色的轮廓
	if not ok:
		break

	# 侦测到目标颜色
	if len(cnts) > 0:
		cnt = max(cnts, key=cv2.contourArea)
		(x, y), radius = cv2.minEnclosingCircle(cnt)
		cv2.circle(frame, (int(x), int(y)), int(radius) * 2,
				   (255, 255, 0), 2)  # 在目标轮廓上画圈
		print('x:', x, 'y:', y)
	print("test!")
	cv2.imshow("Output", frame)
	if cv2.waitKey(1)& 0xFF == ord('q'):
		break
	if cv2.getWindowProperty("Output",1)<0 :
		break
cap.release()
cv2.destroyAllWindows()