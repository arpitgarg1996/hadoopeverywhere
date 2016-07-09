#!/usr/bin/python2
print "content-type:text/html"
print

import commands,cgi,cgitb
cgitb.enable()
data=cgi.FormContent()
node=data['nodes'][0]

print '''<body bgcolor="aqua">'''

pr="\tHADOOP EVERYWHERE\n"
k="\n#--Welcome To Manual Hadoop Automation using Dockers--#\n\n"
print '''<h1 align="center" style="color:maroon;">%s</h1>'''%(pr)
print '''<hr>'''
print '''<h2 align="center" style="color:navy;">%s</h2>'''%(k)

baseip='172.17.0.1'
q=open("newdictfile.txt","w+")
#node=raw_input("Please Enter the Number of Nodes In the Cluster:\t\t")


#Starting containers
for i in range(int(node)):
	j=i+10
	commands.getstatusoutput("sudo docker run -itd -v /hdfsfiles:/etc/hadoop --privileged --name dn"+str(j) + " scpenablessh")[1]
dataid=commands.getstatusoutput("sudo docker ps -a |grep scpenablessh |awk '{print $1}'")[1]

#iplist=commands.getstatusoutput("nmap -n -sP -T5 172.17.0.0-254 |grep -i report |grep -i 172.17.0|awk '{print $5}'")[1]

main={}
f=open("dataidmanual.txt","w+")
f.write(dataid)
f.close()
l=[]
f=open("dataidmanual.txt","r")
for line in f:
	l.append(line.strip())
#print l

for i in l:
	nodeid=i
	ipnode=commands.getstatusoutput("sudo docker exec {0} hostname -i".format(nodeid))[1]
	main[ipnode]=nodeid
#print main
for i,j in main.items():
	q.write(i+"\t"+j+"\n")
q.close()


##################################################################################################

#########################################################################################

print "<pre>"
print "\n\t\tCluster Information\n"
print "IP Address\tFree Ram Size\t\tCPU Configuration\n"
print "</pre>"
#q=open("newdictfile.txt","w+")
for i,j in  main.items():
	if i=="172.17.0.1":
		pass
	else:
		cpu=commands.getstatusoutput("sudo docker exec {} lscpu|grep 'Model name'".format(j))[1]
		k=commands.getstatusoutput("sudo docker exec {} cat /proc/meminfo|grep MemFree".format(j))[1]
		print '''<pre>'''		
		print i+"\t"+ k[16:]+"\t "+cpu[21:]
		print '''</pre>'''
		#q.write(i+"\t"+j+"\n")
#q.close()

print '''<hr><hr>
<form action="http://192.168.56.108/cgi-bin/dockermanualpage2.py" method="POST">
Namenode IP<input type="text" name="name" />Jobtracker IP<input type="text" name="job" /><br>
<input type="submit" value="Configure Cluster" />'''


