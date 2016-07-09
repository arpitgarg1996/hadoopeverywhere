#! /usr/bin/python2
print "content-type:text/html" # browser understands HTML only , we need to tell this
print ""	# it indicates the termination of header.


import cgitb # its traceback for displaying the errors on web browser
import cgi
import commands,os
#import mysql.connector as mariadb
cgitb.enable() # enabling  the traceback

form = cgi.FieldStorage()

fileitem = form['file']
if fileitem.filename :

# strip leading path from file name
# to avoid directory traversal attacks
  		fn = os.path.basename(fileitem.filename)
		f=open("filename.txt","w+")
		f.write(fn)
		f.close()
		kk=open("nnidjtid.txt","r+")
		for line in kk:
			ll=line.split("\t")
			#print ll		
		nnid=ll[0]
		jtid=ll[1]
		nnip=ll[2]
		open('../hadoop/' + fn, 'wb').write(fileitem.file.read())
		message = 'The file "' + fn + '" was uploaded successfully'
		#print message
		#print fn
		#print nnip
		commands.getstatusoutput("sudo sshpass -p root scp /var/www/hadoop/"+fn + " root@{}:/".format(nnip))
		commands.getstatusoutput("sudo docker exec {} hadoop fs -mkdir /user/apache".format(nnid))
		commands.getstatusoutput("sudo docker exec {} hadoop fs -chown apache /user/apache".format(nnid))
		commands.getstatusoutput("sudo docker exec {} hadoop fs -chmod 777 /user/apache".format(nnid))
		commands.getstatusoutput("sudo docker exec "+nnid +" hadoop fs -put /"+fn + " /user/apache")
		print """<body style=\"background-color:green;color:yellow;\"><h1>Welcome To Hadoop Everywhere HDFS Filesystem</h1><br><h3>Congratulations : Your File Has Been Successfully Uploaded into HDFS Cluster</h3>
<br>
<h3 style="a:hover{color:yellow;} color:white; font-size:1.6em;"><a style="color:white;"href="maprducemanual.py" target="_blank">Perform Wordcount</a><script>
				function alertMsg(){
					alert('File uploaded Successfully :P ');
				}
				alertMsg();
				</script>
				</body>"""

else:
		print """<body style=\"background-color:red;\"><script>
				function alertMsg(){
					alert('Upload Failed. Please  try again later');
				}
				alertMsg();
				</script>
				</body>"""
