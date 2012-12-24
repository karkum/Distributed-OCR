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
	<body style="background:#CFECEC">
		<center style="font-size:50">OCR Extraordinaire</center><br /><br />
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
		print "<center style=\"font-size:70\">&#x2639</center><center style=\"font-size:30\"><br />Looks like the image is not a PNG image<br />Please upload a PNG image file</center></body></html>"
		sys.exit(1)	
else: 
	print "<center style=\"font-size:70\">&#x2639</center><center style=\"font-size:30\"><br />Looks like you forgot to upload an image file<br />Please go back and upload an image</center></body></html>"
	sys.exit(1)

#check to see if we are doing this in parallel or serial
dist_roption = form.getvalue('dist')
if dist_roption == "parallel":
	
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
	totaltime = computationend - computationstart
	###############################################################

else:
	###############################################################
	computationstart = int(time.time())
	oldname = '/var/www/uploads/' + str(start) + filedata.filename
	os.system('mv ' + oldname + ' ' + oldname + '_1_1_1_1_.png') 
	args = ['java', '-jar', 'SendOne.jar', oldname + '_1_1_1_1_.png']
	proc = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	message = str(proc.communicate())
	computationend = int(time.time())
	totaltime = computationend - computationstart
	###############################################################	
print """
<center style="font-size:30">It took %d seconds to fulfill this request</center><br /><br />
""" %totaltime

#replace the \n in the recieved message with line breaks, to show in the html page
message = message.replace("\\n", "<br />")
#html code to show image that was uploaded and the result of the computation
image = "ha"
if dist_roption == "parallel":
	image = '/uploads/'+str(start)+filedata.filename+"\""
else:
	image = '/uploads/'+str(start)+filedata.filename+'_1_1_1_1_.png'+"\""  
print """
<table>
<tr>
<td><div style="float:left;width:50%%"><img style="padding:2px;border:2px solid #021A40;background:#FFFFFF;width:100%%" src="%s /></div>
""" %image
print """
<div style="float:right;width:45%%;font-size:20"> %s</div></td>
</tr>
""" %message[2:-6]
#print """
#</body>
#</html>
#"""
#delete all the images, excpet the originial (need to display)
if dist_roption == "parallel":
	folder = '/var/www/uploads/images_to_send/' + str(start)+'/'
	try:
		for file in os.listdir(folder):
			#file_path = os.path.join(folder, file)
			#if os.path.isfile(file_path):
			#	os.unlink(file_path)
			#else:
			#	shutil.rmtree(file_path)
			file_path = '/uploads/images_to_send/' + str(start) + '/' + file
			if not(file_path.endswith('.txt')):
				print """
				<tr><td><img style="padding:2px;border:2px solid #021A40;background:#FFFFFF;" src="%s" /></td>
				""" %file_path
				text_file_path = '/var/www' + file_path[:-3] + "txt"
				f = open(text_file_path, 'r')
				text = f.read()
				print """
				<td><div style="font-size:20"> %s</div></td></tr>
				""" %text
		#os.removedirs(folder)
		#os.remove('/var/www/uploads/'+str(start)+filedata.filename)
		textfile = string.replace(str(start)+filedata.filename, ".png", "_output.txt")
		os.remove('/var/www/uploads/'+textfile)
	except:
		print "Unexpected Error when deleting"
print """
</table>
</body>
</html>
"""
