#! /bin/bash
# Msmtp is dependented
# This script will create an e-mail, which item "To:" is required.
# "Cc:" and "Bcc:" can be add if you want.
# A blank line should be add between the title and content.
# MAIL can be change to a directory where you want to put your e-mail.



MAIL=/home/navy/mail
file=${MAIL}/$(date +%Y%m%d%H%M%S).eml
touch ${file}
echo -e "From: Navy <navych@126.com>\nTo:\nCc:\nBcc:\nSubject:\nReply-To: Navy <navych@126.com>\n" > ${file}
vim ${file}
msmtp -t < ${file}
if [ $? -eq 0 ];then
	mv ${file} ${MAIL}/outbox/
fi

