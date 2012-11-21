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
print "Content-type: text/html"
print

print """
<html>

<head><title>Distributed OCR</title></head>

<body>

  <h3> Distributed OCR Results Page </h3>
"""

timestamp = int(time.time())
form = cgi.FieldStorage()
filedata = form['datafile']
if filedata.filename:
	fn = str(timestamp) + os.path.basename(filedata.filename)
	open('../uploads/' + fn, 'wb').write(filedata.file.read())
	if imghdr.what('/var/www/uploads/'+fn) is not 'png':
		print "Please go back and upload a png image"
		sys.exit(1)	
else: 
	print "Please go back and upload an image"
	sys.exit(1)
#args = ['java', '-jar', 'Split.jar', '/var/www/uploads/' + filedata.filename, '/home/ec2-user/images_to_send/']
os.makedirs('/var/www/uploads/images_to_send/'+str(timestamp)+'/')
args = ['java', '-jar', 'Split.jar', '/var/www/uploads/' + str(timestamp) + filedata.filename, '/var/www/uploads/images_to_send/'+str(timestamp)+'/']
#print args
subprocess.call(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#proc = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#print proc.communicate()

args = ['java', '-jar', 'SendCombine.jar', '/var/www/uploads/images_to_send/' + str(timestamp)+'/']
#print args
proc = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
message = str(proc.communicate())
message = message.replace("\\n", "<br />")
image = '/uploads/'+str(timestamp)+filedata.filename+"\""
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
</html>
""" %message

folder = '/var/www/uploads/images_to_send/' + str(timestamp)+'/'
try:
	for file in os.listdir(folder):
		file_path = os.path.join(folder, file)
		if os.path.isfile(file_path):
			os.unlink(file_path)
		else:
			shutil.rmtree(file_path)
	os.removedirs(folder)
	#os.remove('/var/www/uploads/'+str(timestamp)+filedata.filename)
	textfile = string.replace(str(timestamp)+filedata.filename, ".png", "_output.txt")
	os.remove('/var/www/uploads/'+textfile)
except:
	print "Unexpected Error"

