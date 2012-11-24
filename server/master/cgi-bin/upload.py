#!/usr/bin/env python
import imghdr
import string
import sys
import os
import shutil
import time
import cgi
import cgitb; cgitb.enable()  # for troubleshooting
import subprocess;
#This is the top of the html page
print "Content-type: text/html"
print

print """
<html>

<head><title>Distributed OCR</title></head>

<body>

  <h3> Distributed OCR Results Page </h3>
"""
#The time when the request was received
start = int(time.time())
#used to get the file
form = cgi.FieldStorage()
#look for datafile in the html page
filedata = form['datafile']
#make sure there is a file to upload 
if filedata.filename:
	#create the file using the start
	fn = str(start) + os.path.basename(filedata.filename)
	#write the image in the ../uploads dir.
	open('../uploads/' + fn, 'wb').write(filedata.file.read())
	#make sure the file is a png image
	if imghdr.what('/var/www/uploads/'+fn) is not 'png':
		print "Please go back and upload a png image"
		sys.exit(1)	
else: 
	print "Please go back and upload an image"
	sys.exit(1)

###############################################################
computationstart = int(time.time())
#Create a directory for this image's split sections
os.makedirs('/var/www/uploads/images_to_send/'+str(start)+'/')
#run the split program, which runs the IDT jar and saves each split in the above dir
args = ['java', '-jar', 'Split.jar', '/var/www/uploads/' + str(start) + filedata.filename, '/var/www/uploads/images_to_send/'+str(start)+'/']
subprocess.call(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#proc = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#print proc.communicate()

#next, run the send andcombine jar. it sends the split images and the combines the text we get back
args = ['java', '-jar', 'SendCombine.jar', '/var/www/uploads/images_to_send/' + str(start)+'/']
#print args
proc = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
message = str(proc.communicate())
computationend = int(time.time())
###############################################################

totaltime = computationend - computationstart

#replace the \n in the recieved message with line breaks, to show in the html page
message = message.replace("\\n", "<br />")
#html code to show image that was uploaded and the result of the computation
image = '/uploads/'+str(start)+filedata.filename+"\""
print """
<h5>Input Image:</h5>
<br/>
<img src = "%s>
""" %image
print """
</br>
</br>
</body>
 Image Contents:%s 
""" %message
print """
</br>
 Total time (seconds) required for computation: %d
</html>
""" %totaltime
#delete all the images, excpet the originial (need to display)
folder = '/var/www/uploads/images_to_send/' + str(start)+'/'
try:
	for file in os.listdir(folder):
		file_path = os.path.join(folder, file)
		if os.path.isfile(file_path):
			os.unlink(file_path)
		else:
			shutil.rmtree(file_path)
	os.removedirs(folder)
	#os.remove('/var/www/uploads/'+str(start)+filedata.filename)
	textfile = string.replace(str(start)+filedata.filename, ".png", "_output.txt")
	os.remove('/var/www/uploads/'+textfile)
except:
	print "Unexpected Error"

