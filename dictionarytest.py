#!/usr/bin/python2

import commands

main={}
q=open("newdictfile.txt","r")
for line in q:
	newline=line.strip()
	ll=newline.split("\t")
	main[ll[0]]=ll[1]
print main
nnip='172.17.0.2'
print "\n\n"
print main[nnip]
