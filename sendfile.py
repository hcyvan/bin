#! /usr/bin/python3
import os
import sys
import smtplib
import argparse
#from email.mime.text import MIMEText
import email.parser
import mailbox

USERNAME='navych@126.com'
PASSWORD=''
FROM='navych@126.com'
MAILDIR='/home/navy/mail/test_box'

if __name__ == '__main__':
        describe=" %(prog)s is a python script to send a file by smtplib";
        parser = argparse.ArgumentParser(prog=__file__, description=describe)
        parser.add_argument('-p', '--password',
                            #required=True,
                            help='the password for authentication')
        parser.add_argument('-u', '--username',
                            default=USERNAME,
                            help='the username for authentication')
        parser.add_argument('-f', '--from_addr', metavar='FROM',
                            default=FROM,
                            help='set the "From:" filed, default: %s'%FROM)
        parser.add_argument('-t', '--to_addr', metavar='To',
                            nargs='*',
                            help='set the "To:" filed')
        parser.add_argument('-s', '--subject',
                            nargs='?', const='',
                            help='set the "Subject:" filed')
        parser.add_argument('mail',
                            help='the file you want to send')
        args = parser.parse_args()

        
        parser=email.parser.Parser()
        fd=open(args.mail)
        msg=parser.parse(fd)
        #msg=MIMEText(fd.read())
        fd.close()

        if args.subject=='':
            del msg['Subject']
            msg.__setitem__('Subject', input('Subject: '))
        elif args.subject != None:
            msg.__setitem__('Subject', args.subject)
        msg.__setitem__('From', args.from_addr)
        if args.to_addr != None:
            msg.__setitem__('To', ','.join(args.to_addr))
        if msg['to']==None or msg['to']=='':
            sys.stderr.write('You need to specify the "TO:" field\n')
            exit()

        box=mailbox.Maildir(MAILDIR)
        box.add(msg)
        server=smtplib.SMTP('smtp.126.com',25)
        # server.set_debuglevel(1)
        if args.password != None:
            PASSWORD=args.password
        else:
            PASSWORD=input('password: ')
        server.login(USERNAME, PASSWORD)
        server.send_message(msg)
        server.quit()
