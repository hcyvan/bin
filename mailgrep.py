#! /usr/bin/python
'''
This is a script to classify the MailBox-format mails. This script can work
with other program which can product a MailBox-format such as getmail.

A source-box should be specified, which is the source of all mails. Some 
obj-box and reg-exp pairs should also used as the argument of moveBoxMult().
obj-box is the destination of the mails in source-box, which match the 
regular expression reg-exp. All the files in the script should be expressed
as absolute path. Some pretreatment can be done to get the absolute path 
before use the function defined in this script. Moreover, *checkBox()* 
should be used to make sure the mailbox is MailBox-format.
 
The main progress is short and can be modified to suit your requirement. 
'''
import os
import sys
import re
import shutil
import collections
'''
# To judge if a file contain a line match *regep*
def mailGrep(fileName,regep):
    pattern=re.compile(regep)    
    fd=open(fileName,'r')
    lines=fd.readlines()
    for line in lines:
        found=pattern.search(line)
        if found:
            return True
'''
# To judge where to move the mail according to *regep*s
def mailDest(fileName,grepDict):
    fd=open(fileName,'r')
    lines=fd.readlines()
    fd.close()
    for line in lines:
        for pattern in grepDict.keys():
            #print grepDict[pattern]
            #print line
            if pattern.search(line):
                return grepDict[pattern]
    return os.path.dirname(os.path.dirname(fileName))
# Check whether the box has a MailBox format, and repair it if not.  
def checkBox(box):
    if not os.path.isabs(box):
        sys.stderr.write("Please use a absolue path as the mailBox!\n")
        exit()
    if not os.path.isdir(box):
        sys.stderr.write("The mailBox should be a directory!\n")
        exit()
    else:
        cur=os.path.join(box,r'cur')
        new=os.path.join(box,r'new')
        tmp=os.path.join(box,r'tmp')
        if not os.path.exists(cur):
            os.mkdir(cur)
        if not os.path.exists(new):
            os.mkdir(new)
        if not os.path.exists(tmp):
            os.mkdir(tmp)
# Get all of the path of a box whose format is MailBox. If the subdirectory 
# of the box is not intact, complete it. A tuple, (box, cur, new, tmp), is 
# returned by *subDir*. The tuple represent the subdirectories of the box.
def subDir(box):
    checkBox(box)
    cur=os.path.join(box,r'cur')
    new=os.path.join(box,r'new')
    tmp=os.path.join(box,r'tmp')
    return (box,cur,new,tmp)
'''
# Move mails matched *regep* from srcBox to obj Box
def moveBox(srcBox,objBox,regep):
    srcBoxCur=os.path.join(srcBox,r'cur')
    srcBoxNew=os.path.join(srcBox,r'new')
    srcBoxTmp=os.path.join(srcBox,r'cmp')

    objBoxCur=os.path.join(objBox,r'cur')
    objBoxNew=os.path.join(objBox,r'new')
    objBoxTmp=os.path.join(objBox,r'cmp')
    
    for mail in os.listdir(srcBoxCur):
        fileName=os.path.join(srcBoxCur,mail)
        if mailGrep(fileName,regep):
            shutil.move(fileName,os.path.join(objBoxCur,mail))
    for mail in os.listdir(srcBoxNew):
        fileName=os.path.join(srcBoxNew,mail)
        if mailGrep(fileName,regep):
            shutil.move(fileName,os.path.join(objBoxNew,mail))
'''

# Move mails matched *regep* from srcBox to obj Box
# @@moveBox(src,obj1,regep1,obj2,regep2,...)
def moveBoxMult(srcBox,*obj):
    pairNum=len(obj)
    if pairNum%2 == 1:
        sys.stderr.write("One objBox lack a regep in moveBox()\n")
        exit()

    # Global variable. Ordered dict
    grepDict=collections.OrderedDict()
    for i in range(pairNum):
        if i == pairNum-1:
            break
        if i%2 == 1:
            continue
        objBox=obj[i]
        i+=1
        regep=obj[i]
        grepDict[re.compile(regep)]=objBox
    src=subDir(srcBox)
    for i in range(1,len(src)):
        curNewTmp=os.path.basename(src[i])
        for mail in os.listdir(src[i]):
            fileName=os.path.join(src[i],mail)
            dest=mailDest(fileName,grepDict)
            if(dest != src[0]):
                destName=os.path.join(os.path.join(dest,curNewTmp),mail)
                shutil.move(fileName,destName)

# Main prog

# Get absolue-path and MailBox-format box path
MAIL=r'/home/navy/mail/'
SRC=r'inbox'
OBJ1=r'kernelnewbies_inbox'
REGEP1=r'kernelnewbies'
OBJ2=r'help_gnu_emacs_inbox'
REGEP2=r'help-gnu-emacs'

src=os.path.join(MAIL,SRC)
obj1=os.path.join(MAIL,OBJ1)
obj2=os.path.join(MAIL,OBJ2)

checkBox(src)
checkBox(obj1)
checkBox(obj2)

# Call *getmail -n* to get the new mails
os.system('getmail -n')

# Move mails match REGEP1 from src to obj1
# Move mails match REGEP2 from src to obj2
moveBoxMult(src,obj1,REGEP1,obj2,REGEP2)

print "mailgrep OK..."

