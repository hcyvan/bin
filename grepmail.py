#! /usr/bin/python3
import os
import mailbox
import email.message
'''
This script is to replace mailgrep.py. Use the standard lib of python3,
mailbox, to access the messages in the Maildir format mailbox. And, use
the standard lib email.message to handle the message.
The process is esaier and robuster than the code in mailgrep.py. Python
should be more esay.
'''

# move message from *src* to *dest* if the *condition_func* return True.
# *src* and *dest* is two directory; *condition_func* is a function with
# a email.message.Message argument. If the function return True, the
# message will be removed.
def moveMessage(src, dest, condition_func):
       # check the *dest* directory
       dest_sub=os.listdir(dest)
       if not 'new' in dest_sub:
              os.mkdir(os.path.join(dest,'new'))
       if not 'cur' in dest_sub:
              os.mkdir(os.path.join(dest,'cur'))
       if not 'tmp' in dest_sub:
              os.mkdir(os.path.join(dest,'tmp'))
       
       src_maildir=mailbox.Maildir(src)
       dest_maildir=mailbox.Maildir(dest)
       for key in src_maildir.iterkeys():
              try:
                     message = src_maildir[key]
              except email.errors.MessageParseError:
                     continue
              if condition_func(message):
                     dest_maildir.add(src_maildir.pop(key))

if __name__ == '__main__':

       def kernelnewbies(message):
              match='kernelnewbies.kernelnewbies.org'
              try:
                     if match in message['list-id']:
                            return True
              except:
                     return False
              return False

       def help_gnu_emacs(message):
              match='help-gnu-emacs.gnu.org'
              try:
                     if match in message['list-id']:
                            return True
              except:
                     return False
              return False

       def others(message):
              match='customer_service@jd.com'
              try:
                     if match in message['From']:
                            return True
              except:
                     return False
              return False

       os.system('getmail -n')
       
       boxlist=['inbox','help_gnu_emacs_inbox','kernelnewbies_inbox','others_inbox','outbox']
       maildir=['/home/navy/mail/'+box for box in boxlist]
       
       moveMessage(maildir[0], maildir[1], help_gnu_emacs)
       moveMessage(maildir[0], maildir[2], kernelnewbies)
       moveMessage(maildir[0], maildir[3], others)

       print("... mailfilter ... OK!")
