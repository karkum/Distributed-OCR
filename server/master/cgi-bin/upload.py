#!/usr/bin/env python
import os
import time
import cgi
import cgitb; cgitb.enable()  # for troubleshooting
import subprocess;
print "Content-type: text/html"
print

print """
<html>

<head><title>Sample CGI Script</title></head>

<body>

  <h3> Sample CGI Script </h3>
"""

form = cgi.FieldStorage()
filedata = form['datafile']
message="sd"
if filedata.filename:
	fn = os.path.basename(filedata.filename)
	open('../uploads/' + fn, 'wb').write(filedata.file.read())


print """

  <p>Previous message: %s</p>

  <p>form

  <form method="post" action="index.cgi">
    <p>message: <input type="text" name="message"/></p>
  </form>

</body>

</html>
""" % cgi.escape(message)

#args = ['java', '-jar', 'Split.jar', '/var/www/uploads/' + filedata.filename, '/home/ec2-user/images_to_send/']
timestamp = int(time.time())
os.makedirs('/var/www/uploads/images_to_send/'+str(timestamp)+'/')
args = ['java', '-jar', 'Split.jar', '/var/www/uploads/' + filedata.filename, '/var/www/uploads/images_to_send/'+str(timestamp)+'/']
print args
proc = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
print proc.communicate()

args = ['java', '-jar', 'SendCombine.jar', '/var/www/uploads/images_to_send/' + str(timestamp)+'/']
print args
proc = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
print proc.communicate()
