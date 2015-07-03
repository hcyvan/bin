#! /usr/bin/python
import os
import sys
fileList=os.listdir(os.getcwd())
# change the scripts to excutable state, and create to soft link to them
if (len(sys.argv)==1):
	for file in fileList:
		if((file[-3:]==".py"or file[-3:]==".sh") and file!="configure.py"):
			print file
			os.system("chmod 755 "+file)
			os.system("ln -s "+file+" "+file[:-3])

# re move the soft link to the scripts
if (len(sys.argv)==2 and sys.argv[1]=="-d"):
	for file in fileList:
		if(file[-3:]==".py" and file!="configure.py"):
				os.system("rm "+file[:-3])

