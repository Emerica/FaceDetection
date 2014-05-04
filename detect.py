#!/usr/bin/python
import cv2
import sys
import os
import subprocess
import glob

csv = []
#http://fideloper.com/facial-detection
def detect(path):
    img = cv2.imread(path)
    cascade = cv2.CascadeClassifier("./haarcascade_frontalface_alt.xml")
    rects = cascade.detectMultiScale(img, 1.3, 4, cv2.cv.CV_HAAR_SCALE_IMAGE, (20,20))

    if len(rects) == 0:
        return [], img
    rects[:, 2:] += rects[:, :2]
    return rects, img

def box(rects, img, filename, filedetected):
    faces = 0
    cv2.imwrite(filename, img);
    for x1, y1, x2, y2 in rects:
        csv.append(filename + "," + str(x1) + "," + str(y1) + "," + str(x2) + "," + str(y2))
        cv2.rectangle(img, (x1, y1), (x2, y2), (127, 255, 0), 2)
        faces=faces+1
    if faces:
        cv2.imwrite(filedetected, img);
    return faces

print "Making directories"
try:
    os.mkdir(os.path.splitext(sys.argv[1])[0])
    os.mkdir(os.path.splitext(sys.argv[1])[0] + "/clean")
    os.mkdir(os.path.splitext(sys.argv[1])[0] + "/detected")
except:
   print "Directories exist"

print "Detect Fps"
p1 = subprocess.Popen(["ffmpeg","-i", sys.argv[1] ], stderr=subprocess.PIPE)
result =  p1.communicate()
lines = str(result).split("\\n")
for line in lines:
    pos = line.find(" fps")
    if(pos > 0):
        fps = str(line).split(" ")[16]
        break

print "Fps:" + str(fps)

print "Extracting Images"
p = subprocess.Popen(["ffmpeg", "-i" , sys.argv[1], "-vf", "select='eq(pict_type\,I)',setpts='N/("+ fps +"*TB)'",  os.path.splitext(sys.argv[1])[0] + "/clean/%09d.jpg"], stdout=subprocess.PIPE)
result = p.communicate()[0]

print "Runing face detection on images"
csvfile = os.path.splitext(sys.argv[1])[0] + "/" + os.path.splitext(sys.argv[1])[0]  + ".csv"


files = glob.glob(os.path.splitext(sys.argv[1])[0] + '/clean/*.jpg')


for image in files:
    rects, img = detect(image)
    basename = image.split("/")[-1]
    filed = os.path.splitext(sys.argv[1])[0] + "/detected/" + basename;
    faces = box(rects, img, image, filed)
    if faces > 0:
        print "Image " + image
        print str(faces) + " faces found"
    

print "Exporting csv"
output = "\n".join(csv)
target = open(csvfile, 'w')
target.write(output)
target.close()