#! /usr/bin/python2
print "content-type:text/html" # browser understands HTML only , we need to tell this
print ""	# it indicates the termination of header.


import cgitb,cgi,commands
cgitb.enable()
#form = cgi.FieldStorage()
print """<body style=\"background-color:green;color:yellow;\"><h1>Welcome To Hadoop Everywhere Map Reduce Portal</h1><br><h3>Wordcount Result</h3>
<br></body>"""
print "\n"
f=open("filename.txt","r+")
for line in f:
	var=line.strip()
	#print var+"\n\n"
q=open("nnidjtid.txt","r+")
for line in q:
	ll=line.split("\t")
jtid=ll[1]
#print jtid
print '''<pre>'''
print commands.getstatusoutput("sudo docker exec "+jtid + " hadoop jar /usr/share/hadoop/hadoop-examples-1.2.1.jar wordcount /user/apache/" +var+ " /mim32")[1]
print '''</pre>'''



print '''<pre>'''
print commands.getstatusoutput("sudo docker exec "+jtid +" hadoop fs -cat /mim32/part-r-00000")[1]
print '''</pre>'''



