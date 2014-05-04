FaceDetect
--------------------------------------------------------------------
This is a very simple set of unfinished python scripts. Based on the example provided at
http://fideloper.com/facial-detection
Created late on a Satuday night to get something done, and is not meant for you to use in a production environment as is.
Nothing is verified etc. 
Python is not my primary pleasure, so feel free to improve.
--------------------------------------------------------------------

sudo apt-get update
sudo apt-get install -y vim build-essential python-software-properties    # The Basics
sudo apt-get install -y python-opencv python-numpy python-scipy        # OpenCV items
sudo apt-get install -y ffmpeg       # ffmpeg, (might need more here?, I build from git)

wget http://eclecti.cc/files/2008/03/haarcascade_frontalface_alt.xml

--------------------------------------------------------------------

detect.py filename
	Detect calls ffmpeg to get the framerate of the video, then uses ffmpeg again to extract the keyframes from the file.
	The images are save to (basename)/clean/ as jpg files
	The opencv routine is run over the images, if at least one face is detected, than the image is saved with a rectangle drawn in (basename)/detected/ 
	When the loop is complete a csv file is written to (basename)/(basename).csv with the filenames and face locations for each image
	csv: filename, x1, y1, x2, y2
	
	
loop.py filename column#
	Loop over the csv file
	wget the http location in column number supplied
	run detect.py on it.
	