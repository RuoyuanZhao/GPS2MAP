from selenium import webdriver
import xml.dom.minidom
import matplotlib
import time
import sys
import cv2

size = int(sys.argv[1])
browser = webdriver.Firefox()
def capture(url, save_fn="capture.png"):
	browser.set_window_size(1200, 900)
	browser.get(url)
	time.sleep(1)
	browser.save_screenshot(save_fn)

dom = xml.dom.minidom.parse('output.gps')
root = dom.documentElement
itemlist = root.getElementsByTagName("trkpt")
itemlist2 = root.getElementsByTagName("time")
number = len(itemlist)
cv2.namedWindow("pic")
for i in range(0, number):
	item = itemlist[i]
	item2 = itemlist2[i]
	lat = float(item.getAttribute("lat"))
	lon = float(item.getAttribute("lon"))
	times = item2.firstChild.data
	url = "http://www.openstreetmap.org/#map=%d/%f/%f" % (size, lat, lon)
	savepath = "%s.png" % (times)
	print url
	print savepath
	capture(url, savepath)
	image = cv2.imread(savepath)
	image = image[55:image.shape[0], 0:image.shape[1]]
	mid_height = int(image.shape[0] / 2)
	mid_width = int(image.shape[1] / 2)
	cv2.circle(image, (mid_width, mid_height), 3, (255, 0, 0))
	cv2.imshow("pic", image)
	cv2.imwrite(savepath, image)
browser.close()
