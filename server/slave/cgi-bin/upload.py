#!/usr/bin/env python
import os
import subprocess
import cgi
import cgitb; cgitb.enable()  # for troubleshooting

print "Content-type: text/plain"
print

#print """
#<html>
#
#<head><title>Sample CGI Script</title></head>
#
#<body>
#
#  <h3> Sample CGI Script </h3>
#"""

form = cgi.FieldStorage()
filedata = form['datafile']
message="sd"
if filedata.filename:
	fn = os.path.basename(filedata.filename)
	open('../uploads/' + fn, 'wb').write(filedata.file.read())


#print """
#
#  <p>Previous message: %s</p>
#
#  <p>form
#
#  <form method="post" action="index.cgi">
#    <p>message: <input type="text" name="message"/></p>
#  </form>
#
#</body>
#
#</html>
#""" % cgi.escape(message)
filePath = '../uploads/' + fn
outputFilePath = filePath + 'Output'
readFilePath = outputFilePath + '.txt'
nums = fn.split('_')
print nums[1] + ' ' + nums[2] + ' ' + nums[3] + ' ' + nums[4]
output = subprocess.call(['/usr/local/bin/tesseract', filePath, outputFilePath])
f = open(readFilePath, 'r')
print f.read()
os.remove(filePath)
os.remove(readFilePath)

