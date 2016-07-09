#!/usr/bin/python2
print "content-type:text/html"
print

import commands,cgi
data=cgi.FormContent()
nodes=data['node'][0]

def dn_auto(i,nnip):
	dirname="datahad1"+i
	dataid=i
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
########################################################################################
def tt_auto(i,jtip):
	dataid=i
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
	#print "<pre>"	
	print "Service Started at Container ID:\t"+dataid+"\n"
	print commands.getstatusoutput("sudo docker exec {} /usr/java/jdk1.7.0_51/bin/jps".format(dataid))[1]
	#print "</pre>"
	
	#print commands.getstatusoutput("sshpass -p root ssh -l root {} /usr/java/jdk1.7.0_51/bin/jps".format(ttip))[1]
	#print commands.getstatusoutput("docker exec {} /usr/java/jdk1.7.0_51/bin/jps".format(dataid))

###################################################################################################
def status(nnid):
	print "\t\tHDFS STATUS\n"
	print commands.getstatusoutput("sudo docker exec {} hadoop dfsadmin -report".format(nnid))[1]
	commands.getstatusoutput("sudo docker exec {} hadoop dfsadmin -safemode leave".format(nnid))
	print "\nMAP REDUCE REPORT\n"
	print commands.getstatusoutput("sudo docker exec {} hadoop job -list-active-trackers".format(jtid))[1]	
#######################################################################################################
#print '''<body bgcolor="aqua">''''
print "\n\t\t#--Welcome To Hadoop Automation using Dockers--#\n\n"
#nodes=raw_input("Enter Number of Nodes To Be configured:\t")
nnip='172.17.0.2'
baseip='172.17.0.1'
jtip='172.17.0.3'

#IP FIXING

nnid='fda35acf1362'
jtid='ad435fe0988f'
#Namenode Start
commands.getstatusoutput("sudo docker start fda35acf1362 ")
commands.getstatusoutput("sudo docker exec fda35acf1362  service sshd start")
commands.getstatusoutput("sudo docker exec fda35acf1362  service sshd start")
commands.getstatusoutput("sudo docker exec fda35acf1362  hadoop-daemon.sh start namenode")
#print "<pre>"
print "\nService Started at IP Address:\t"+nnip+"\n"
print commands.getstatusoutput("sudo docker exec fda35acf1362  /usr/java/jdk1.7.0_51/bin/jps")[1]
#print "</pre>"
#Jobtracker Start
commands.getstatusoutput("sudo docker start ad435fe0988f")
commands.getstatusoutput("sudo docker exec ad435fe0988f service sshd start")
commands.getstatusoutput("sudo docker exec ad435fe0988f service sshd start")
commands.getstatusoutput("sudo docker exec ad435fe0988f hadoop-daemon.sh start jobtracker")
#print "<pre>"
print "\nService Started at IP Address:\t"+jtip+"\n"
print commands.getstatusoutput("sudo docker exec ad435fe0988f /usr/java/jdk1.7.0_51/bin/jps".format(jtip))[1]
#print "</pre>"
#
#Starting containers
for i in range(int(nodes)):
	j=i+90
	commands.getstatusoutput("sudo docker run -itd -v /hdfsfiles:/etc/hadoop --privileged --name dn"+str(j) + " scpenablessh")[1]
dataid=commands.getstatusoutput("sudo docker ps -a |grep scpenablessh |awk '{print $1}'")[1]
	#iplist=commands.getstatusoutput("nmap -n -sP -T5 172.17.0.0-254 |grep -i report |grep -i 172.17.0|awk '{print $5}'")[1]




#---------------------------------------------------------------#
f=open("dataid.txt","w")
f.write(dataid)
f.close()
l=[]
f=open("dataid.txt","r")
for line in f:
	l.append(line.strip())
#print l
#----------------------------------------------------------------#
for i in  l:
	dn_auto(i,nnip)
	tt_auto(i,jtip)
#status(nnid)

