#!/usr/bin/python2
print "content-type:text/html"
print

import commands,cgi,cgitb
cgitb.enable()
data=cgi.FormContent()
nanip=data['name'][0]
jotip=data['job'][0]
nnip='172.17.0.'+nanip
jtip='172.17.0.'+jotip
#print nnip
#print jtip
print '''<body bgcolor="aqua">
<div class="main" border="20px solid">'''
#NAMENODE CREATION-#####################################
def nn_auto(nnip,nnid):
	f=open("/hdfsfiles/hdfs-site.xml","w+")
	k='''<?xml version="1.0"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>
<!--Put site-specific property overiddes in this file. -->

<configuration>
<property>
<name>dfs.name.dir</name>
<value>/namenodocker</value>
</property>
</configuration>'''
	f.write(k)	
	f.close()

	h=open("/hdfsfiles/core-site.xml","w+")
	d='''<?xml version="1.0"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>
<!--Put site-specific property overrides in this file. -->

<configuration>
<property>
<name>fs.default.name</name>
<value>hdfs://'''+nnip+''':9001</value>
</property>
</configuration>'''
	h.write(d)
	h.close()
	commands.getstatusoutput("sudo docker exec {} hadoop namenode -format".format(nnid))
	commands.getstatusoutput("sudo docker exec {} hadoop-daemon.sh start namenode".format(nnid))
	print "<pre>"	
	print "\n\tService Started at IP Address:\t"+nnip 
	print commands.getstatusoutput("sudo docker exec {} /usr/java/jdk1.7.0_51/bin/jps".format(nnid))[1]
	print "</pre>"	
########################################################################################

#Datanode Creation####################################
def dn_auto(j,nnip):
	dirname="datanode_docker"
	dataid=j
	f=open("/hdfsfiles/hdfs-site.xml","w+")
	k='''<?xml version="1.0"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>
<!--Put site-specific property overiddes in this file. -->

<configuration>
<property>
<name>dfs.data.dir</name>
<value>/'''+dirname+'''</value>
</property>
</configuration>'''
	f.write(k)	
	f.close()

	h=open("/hdfsfiles/core-site.xml","w+")
	d='''<?xml version="1.0"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>
<!--Put site-specific property overrides in this file. -->

<configuration>
<property>
<name>fs.default.name</name>
<value>hdfs://'''+nnip+''':9001</value>
</property>
</configuration>'''
	h.write(d)
	h.close()
	commands.getstatusoutput("sudo docker exec {} hadoop-daemon.sh start datanode".format(dataid))
	#commands.getstatusoutput("docker exec {} /usr/java/jdk1.7.0_51/bin/jps".format(dataid))
	#print commands.getstatusoutput("sshpass -predhat ssh root@{0}  /usr/java/jdk1.7.0_51/bin/jps".format(dnip))[1]
####################################################################################################

#TASKTRACKER CREATE
def tt_auto(j,jtip):
	dataid=j
	f=open("/hdfsfiles/mapred-site.xml","w+")
	k='''<?xml version="1.0"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>
<!--Put site-specific property overiddes in this file. -->

<configuration>
<property>
<name>mapred.job.tracker</name>
<value>'''+jtip+''':9002</value>
</property>
</configuration>'''
	f.write(k)	
	f.close()

	#commands.getstatusoutput("sshpass -p root scp /hdfsfiles/mapred-site.xml root@{}:/etc/hadoop".format(ttip))
	#commands.getstatusoutput("sshpass -p root ssh -l root {} hadoop-daemon.sh start tasktracker".format(ttip))
	commands.getstatusoutput("sudo docker exec {} hadoop-daemon.sh start tasktracker".format(dataid))
	print "<pre>"	
	print "Service Started at Container ID:\t"+dataid+"\n"
	print commands.getstatusoutput("sudo docker exec {} /usr/java/jdk1.7.0_51/bin/jps".format(dataid))[1]
	print "</pre>"
	
	#print commands.getstatusoutput("sshpass -p root ssh -l root {} /usr/java/jdk1.7.0_51/bin/jps".format(ttip))[1]
	#print commands.getstatusoutput("docker exec {} /usr/java/jdk1.7.0_51/bin/jps".format(dataid))

###################################################################################################
#Jobtracker CREATE
def jt_auto(nnip,jtip,jtid):
	f=open("/hdfsfiles/mapred-site.xml","w+")
	k='''<?xml version="1.0"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>
<!--Put site-specific property overiddes in this file. -->

<configuration>
<property>
<name>mapred.job.tracker</name>
<value>'''+jtip+''':9002</value>
</property>
</configuration>'''
	f.write(k)	
	f.close()
	h=open("/hdfsfiles/core-site.xml","w+")
	d='''<?xml version="1.0"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>
<!--Put site-specific property overrides in this file. -->

<configuration>
<property>
<name>fs.default.name</name>
<value>hdfs://'''+nnip+''':9001</value>
</property>
</configuration>'''
	h.write(d)
	h.close()
	commands.getstatusoutput("sudo docker exec {} hadoop-daemon.sh start jobtracker".format(jtid))
	#commands.getstatusoutput("sudo docker exec {} hadoop-daemon.sh start tasktracker".format(dataid))
	print "<pre>"	
	print "Service Started at Container ID:\t"+jtip+"\n"
	print commands.getstatusoutput("sudo docker exec {} /usr/java/jdk1.7.0_51/bin/jps".format(jtid))[1]
	print "</pre>"
	
	#print commands.getstatusoutput("sshpass -p root ssh -l root {} /usr/java/jdk1.7.0_51/bin/jps".format(ttip))[1]
	#print commands.getstatusoutput("docker exec {} /usr/java/jdk1.7.0_51/bin/jps".format(dataid))
#####################################################################################################
def status(nnid,jtid):
	print "<hr><pre>"
	k="HDFS STATUS\n"
	print '''<h2 align="center" style="color:navy;font-size:1.6em;">%s</h2>'''%(k)
	print "<hr>"
	print commands.getstatusoutput("sudo docker exec {} hadoop dfsadmin -report".format(nnid))[1]
	print '''</pre>'''	
	commands.getstatusoutput("sudo docker exec {} hadoop dfsadmin -safemode leave".format(nnid))
	#print "<pre>"
	#print "\nMAP REDUCE REPORT\n"
	#print commands.getstatusoutput("sudo docker exec {} hadoop job -list-active-trackers".format(jtid))[1]
	#print "</pre>"
#######################################################################################################


k="\n\t\tHADOOP EVERYWHERE\n"
lll="\n\n#--Welcome To Manual Hadoop Automation using Dockers--#\n"
print '''<h1 align="center" style="color:navy;">%s</h1>'''%(k)
print '''<h3 align="center" style="color:maroon;">%s</h3>'''%(lll)
baseip='172.17.0.1'
#node=raw_input("Please Enter the Number of Nodes In the Cluster:\t\t")
main={}
q=open("newdictfile.txt","r")
for line in q:
	newline=line.strip()
	ll=newline.split("\t")
	main[ll[0]]=ll[1]
#print main
print "\n\n"
#print main[nnip]
nnid=main[nnip]
jtid=main[jtip]
ff=open("nnidjtid.txt","w+")
ff.write(nnid+"\t"+jtid+"\t"+nnip)
ff.close
#print nnid
#print jtid
nn_auto(nnip,nnid)
jt_auto(nnip,jtip,jtid)
for i,j in main.items():
	if i==nnip or i==jtip or i==baseip:
		pass
	else:
		dn_auto(j,nnip)
		tt_auto(j,jtip)
status(nnid,jtid)
print'''<html>
<hr><hr>
<div style="background-color:#000080;border:20px;">
<br>
<form enctype="multipart/form-data" action="../cgi-bin/fupmanual.cgi" method="post">
<br>
<p style="color:yellow; font-size:1.5em;">Choose File To Be Uploaded into HDFS:<br> <input type="file" name="file"></p><br>
<p><input type="submit" value="Upload"></p>
<br>
<br>
</form>
</body>
</html>'''

