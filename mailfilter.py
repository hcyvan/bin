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

# move message from *src_maildir* to *dest_maildir* if the *condition_func*
# return True. *condition_func* is a function with a email.message.Message
# argument. If the function return True, the message will be removed.
def moveMessage(src_maildir, dest_maildir, condition_func):
       move=0
       leave=0
       for key in src_maildir.iterkeys():
              try:
                     message = src_maildir[key]
              except email.errors.MessageParseError:
                     continue
              if condition_func(message):
                     dest_maildir.add(src_maildir.pop(key))
                     move = move+1
              else:
                     leave =leave+1

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

       os.system('getmail -n')
       
       boxlist=['help_gnu_emacs_inbox','kernelnewbies_inbox','inbox','outbox']
       maildir=['/home/navy/mail/'+box for box in boxlist]
       b0 = mailbox.Maildir(maildir[0])
       b1 = mailbox.Maildir(maildir[1])
       b2 = mailbox.Maildir(maildir[2])
       # b3 = mailbox.Maildir(maildir[3])
       moveMessage(b2, b0, help_gnu_emacs)
       moveMessage(b2, b1, kernelnewbies)

       print("... mailfilter ... OK!")
