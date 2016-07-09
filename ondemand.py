#!/usr/bin/python2
import commands

def dn_auto(i,nnip):
	dirname="datahd1"+i.split(".")[3]
	dnip=i
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
	commands.getstatusoutput("sshpass -p root scp /hdfsfiles/hdfs-site.xml root@{}:/etc/hadoop".format(dnip))
	commands.getstatusoutput("sshpass -p root scp /hdfsfiles/core-site.xml root@{}:/etc/hadoop".format(dnip))
	commands.getstatusoutput("sshpass -p root ssh -l root {} hadoop-daemon.sh start datanode".format(dnip))
	commands.getstatusoutput("sshpass -p root ssh -l root {} /usr/java/jdk1.7.0_51/bin/jps".format(dnip))[1]
#--------------------------------------------------#
def status(nnip):
	print commands.getstatusoutput("sshpass -p root ssh -l root {} hadoop dfsadmin -report".format(nnip))[1]
	commands.getstatusoutput("sshpass -p root ssh -l root {} hadoop dfsadmin -safemode leave".format(nnip))[1]
	print commands.getstatusoutput("sshpass -p root ssh -l root {} hadoop job -list-active-trackers".format(nnip))[1]	

#--------------------------------------------------------------------------------#
def tt_auto(i,jtip):
	ttip=i
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

	commands.getstatusoutput("sshpass -p root scp /hdfsfiles/mapred-site.xml root@{}:/etc/hadoop".format(ttip))
	commands.getstatusoutput("sshpass -p root ssh -l root {} hadoop-daemon.sh start tasktracker".format(ttip))
	print "Service Started at IP Address:\t"+ttip+"\n"
	print commands.getstatusoutput("sshpass -p root ssh -l root {} /usr/java/jdk1.7.0_51/bin/jps".format(ttip))[1]
#---------------------------------------------------#

#MAIN PROGRAM STARTS HERE

print "\n\t\tWelcome To Hadoop Automation using Dockers\n\n"
nodes=raw_input("Enter Number of Datanodes To Be configured:\t")
nnip='172.17.0.2'
baseip='172.17.0.1'
jtip='172.17.0.3'

#IP FIXING
a=commands.getstatusoutput("docker start fda35acf1362")
commands.getstatusoutput("docker exec fda35acf1362 service sshd start")
commands.getstatusoutput("docker exec fda35acf1362 service sshd start")
commands.getstatusoutput("docker exec fda35acf1362 hadoop-daemon.sh start namenode")
print "\nService Started at IP Address:\t"+nnip+"\n"
print commands.getstatusoutput("sshpass -p root ssh -l root {} /usr/java/jdk1.7.0_51/bin/jps".format(nnip))[1]

commands.getstatusoutput("docker start ad435fe0988f")
commands.getstatusoutput("docker exec ad435fe0988f service sshd start")
commands.getstatusoutput("docker exec ad435fe0988f service sshd start")
commands.getstatusoutput("docker exec ad435fe0988f hadoop-daemon.sh start jobtracker")
print "\nService Started at IP Address:\t"+jtip+"\n"
print commands.getstatusoutput("docker exec ad435fe0988f /usr/java/jdk1.7.0_51/bin/jps".format(jtip))[1]

#Starting containers
for i in range(int(nodes)):
	j=i+20
	#print commands.getstatusoutput("docker run -itd -v /hdfsfiles:/etc/hadoop --privileged --name dn"+str(j) + " scpenablessh")
	commands.getstatusoutput("docker run -itd  --privileged --name dn"+str(j) + " scpenablessh")

iplist=commands.getstatusoutput("nmap -n -sP -T5 172.17.0.0-254 |grep -i report |grep -i 172.17.0|awk '{print $5}'")[1]




#---------------------------------------------------------------#
f=open("nmaplist.txt","w+")
f.write(iplist)
f.close()
l=[]
f=open("nmaplist.txt","r")
for line in f:
	l.append(line.strip())
#print l
#----------------------------------------------------------------#
for i in  l:
	if i=="172.17.0.1" or i==nnip or i==jtip:
		pass
	else:
		dn_auto(i,nnip)
		tt_auto(i,jtip)
status(nnip)
#----------------------------------------------------------------------------#

