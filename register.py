#! /usr/bin/python3
import os
import sys
import re
import argparse

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

# Add *path* to the PATH
def add_to_PATH(path):
        PATH=set(os.getenv('PATH').split(':'))
        bashrc=os.getenv('HOME')+'.bashrc'
        if path not in PATH:
                commit='\n# Add by %s\n'%os.path.realpath(sys.argv[0])
                shell='export PATH=$PATH:%s\n'%path
                if not grepfl(bashrc, r'%s'%commit.strip()):
                        fd=open(bashrc, 'a+')
                        fd.write(commit+shell)
                        fd.close()
                        print("ADD:\n"+commit+shell+'\nTO '+bashrc)

def install(files):
        for f in files:
                os.system('chmod 755 '+f)
                os.system('ln -s '+f+' '+os.path.splitext(f)[0])
def clean(files):
        for f in files:
                os.system('rm '+os.path.splitext(f)[0])
                os.system('chmod -x '+f)

                        
if __name__ == '__main__':
        describe="\
        This is a python script to regist this directory to PATH, change \
        the other scripts in this directory executable and create soft link \
        without extend name for them. Do not change this script to executable \
        to prevent misuse. -h or --help for usage"

        parser = argparse.ArgumentParser(description=describe)
        group = parser.add_mutually_exclusive_group()
        group.add_argument("-c", "--clean", action="store_true")
        group.add_argument("-i", "--install", action="store_true")
        args = parser.parse_args()

        files=set(os.listdir(os.getcwd()))-set([__file__, 'README.md','.git'])

        if args.clean:
                print('...clean...')
                clean(files)

        else:
                print('...install...')
                add_to_PATH(os.getcwd())
                install(files)

