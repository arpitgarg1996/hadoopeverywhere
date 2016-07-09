#!/usr/bin/python2
import commands,cgi

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
	print "\n\tService Started at IP Address:\t"+nnip 
	print commands.getstatusoutput("docker exec {} /usr/java/jdk1.7.0_51/bin/jps".format(nnid))[1]
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
	#print "<pre>"	
	print "Service Started at Container ID:\t"+dataid+"\n"
	print commands.getstatusoutput("sudo docker exec {} /usr/java/jdk1.7.0_51/bin/jps".format(dataid))[1]
	#print "</pre>"
	
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
	#commands.getstatusoutput("docker exec {} /usr/java/jdk1.7.0_51/bin/jps".format(dataid))
	#print commands.getstatusoutput("sshpass -predhat ssh root@{0}  /usr/java/jdk1.7.0_51/bin/jps".format(dnip))[1]

	#commands.getstatusoutput("sshpass -p root scp /hdfsfiles/mapred-site.xml root@{}:/etc/hadoop".format(ttip))
	#commands.getstatusoutput("sshpass -p root ssh -l root {} hadoop-daemon.sh start tasktracker".format(ttip))
	#commands.getstatusoutput("sudo docker exec {} hadoop-daemon.sh start tasktracker".format(dataid))
	#print "<pre>"	
	print "Service Started at Container ID:\t"+jtip+"\n"
	print commands.getstatusoutput("sudo docker exec {} /usr/java/jdk1.7.0_51/bin/jps".format(jtid))[1]
	#print "</pre>"
	
	#print commands.getstatusoutput("sshpass -p root ssh -l root {} /usr/java/jdk1.7.0_51/bin/jps".format(ttip))[1]
	#print commands.getstatusoutput("docker exec {} /usr/java/jdk1.7.0_51/bin/jps".format(dataid))
#####################################################################################################
def status(nnid,jtid):
	print "\t\tHDFS STATUS\n"
	print commands.getstatusoutput("sudo docker exec {} hadoop dfsadmin -report".format(nnid))[1]
	commands.getstatusoutput("sudo docker exec {} hadoop dfsadmin -safemode leave".format(nnid))
	print "\nMAP REDUCE REPORT\n"
	print commands.getstatusoutput("sudo docker exec {} hadoop job -list-active-trackers".format(jtid))[1]	
#######################################################################################################


k="\n\t\t#--Welcome To Manual Hadoop Automation using Dockers--#\n\n"
print k
baseip='172.17.0.1'
node=raw_input("Please Enter the Number of Nodes In the Cluster:\t\t")


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
	ipnode=commands.getstatusoutput("docker exec {0} hostname -i".format(nodeid))[1]
	main[ipnode]=nodeid
#print main


##################################################################################################

#########################################################################################

'''s=open("ipdata.txt","w+")
s.write(iplist)
s.close()
m=[]
t=open("ipdata.txt","r")
for line in t:
	m.append(line.strip())
mm=[]
for i in m:
	if i=='172.17.0.1':
		pass
	else:
		mm.append(i)
#print mm'''



'''main={}
j=0
for i in mm:
	main[i]=l[j]
	j=j+1
print main'''

print "\n\t\tCluster Information\n"
print "IP Address\tFree Ram Size\t\tCPU Configuration\n"
for i,j in  main.items():
	if i=="172.17.0.1":
		pass
	else:
		cpu=commands.getstatusoutput("docker exec {} lscpu|grep 'Model name'".format(j))[1]
		k=commands.getstatusoutput("docker exec {} cat /proc/meminfo|grep MemFree".format(j))[1]
		print i+"\t"+ k[16:]+"\t "+cpu[21:]

x=raw_input("Please Enter Namenode IP:\t\t")
y=raw_input("Please Enter Jobtracker IP IP:\t\t")
nnip='172.17.0.'+x
jtip='172.17.0.'+y
nnid=main[nnip]
jtid=main[jtip]
print nnid
print jtid
nn_auto(nnip,nnid)
jt_auto(nnip,jtip,jtid)
for i,j in main.items():
	if i==nnip or i==jtip or i==baseip:
		pass
	else:
		dn_auto(j,nnip)
		tt_auto(j,jtip)
#status(nnid,jtid)
