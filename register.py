'''
This is a python script to regist this directory to PATH, change the other scripts
in this directory executable and create soft link without extend name for 
them. Do not change this script to executable to prevent misuse.

+ *python ./register* : Regist this directory and make other script executable
+ *python ./register -d* : Delete the soft links. 
 
'''
import os
import sys
import re

exts=set([r'.py',r'.sh'])
paths=set(os.getenv('PATH').split(':'))

## Grep a *fileName* line-by-line by *regep*
def grepfl(fileName,regep):
        pattern=re.compile(regep)    
        fd=open(fileName,'r')
        lines=fd.readlines()
        fd.close()
        for line in lines:
                if pattern.search(line):
                        return True
        return False
                
# If os.getcwd() is not in PATH, Add it to .bashrc. The path will not
# be added twice.
if os.getcwd() not in paths:
        # Judge whether does "~/.bashrc" exist
        bashrc=os.path.join(os.getenv('HOME'),'.bashrc')
        if os.path.exists(bashrc):
                commit='\n# Add by %s\n'%os.path.realpath(sys.argv[0])
                shell='export PATH=$PATH:%s\n'%os.getcwd()
                if not grepfl(bashrc, r'%s'%commit.strip()):
                        fd=open(bashrc,'a+')
                        fd.write(commit+shell)
                        fd.close()
                        print("ADD:\n"+commit+shell+'\nTO '+bashrc)

# Chomd 755 and create soft link for scripts 
files=os.listdir(os.getcwd())
for fname in files:
        parts=os.path.splitext(fname)
        if (parts[1] in exts):
                if (len(sys.argv)==1):
                        # Change the scripts to excutable state
                        # and create to soft link to them
                        os.system('chmod 755 '+fname)
                        os.system('ln -s '+fname+' '+parts[0])
                if (len(sys.argv)==2 and sys.argv[1]=='-d'):
                        # Remove the soft link to the scripts
                        os.system('rm '+parts[0])
                        os.system('chmod -x '+fname)

