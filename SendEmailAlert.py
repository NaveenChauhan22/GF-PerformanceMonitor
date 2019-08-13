#Send email using gmail's smtp and QA's test account

import sys
import socket
import smtplib, email
from email import encoders
import os

FIRST_ARG = sys.argv[1]
#SECOND_ARG = sys.argv[2]
#HOST_IP = socket.gethostbyname(socket.gethostname())

HOST_IP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
HOST_IP.connect(("8.8.8.8", 80))
strHOST_IP = HOST_IP.getsockname()[0]
HOST_IP.close()

SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 465
SMTP_USERNAME = 'mobilelabsQA@gmail.com'
SMTP_PASSWORD = 'Basement@D-25'
SMTP_FROM = 'mobilelabsQA@gmail.com'
SMTP_TO = ['naveen.chauhan@mobilelabsinc.com','naveen.chauhan@pyramidconsultinginc.com']
EMAIL_SUBJECT = strHOST_IP + ': GigaFox server performance alert!'

#TEXT_FILENAME = '/Users/administrator/Desktop/Jira/NewFolder/Logs/MobileLabs.DeviceConnect.WatchDog.log'
MESSAGE = 'Alert for Server: ' + strHOST_IP + '\n\nMessage: \n***************************************************************************\
***************************************************************************\n' + str(FIRST_ARG) \
+ '\n*************************************************************************************************************************************\
*****************'

#Construct the message
#msg = email.MIMEMultipart.MIMEMultipart()
#body = email.MIMEText.MIMEText(MESSAGE)
#attachment = email.MIMEBase.MIMEBase('text', 'plain')
#attachment.set_payload(open(TEXT_FILENAME).read())
#attachment.add_header('Content-Disposition', 'attachment', filename=os.path.basename(TEXT_FILENAME))
#encoders.encode_base64(attachment)

#msg.attach(body)
#msg.attach(attachment)
#msg.add_header('From', SMTP_FROM)
#msg.add_header('To', SMTP_TO)

msg = 'Subject: {}\n\n{}'.format(EMAIL_SUBJECT,MESSAGE)

# Now send the message
try:
    mailer = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)
    # EDIT: mailer is already connected
    # mailer.connect()
    mailer.login(SMTP_USERNAME, SMTP_PASSWORD)
    mailer.sendmail(SMTP_FROM, SMTP_TO, msg)
    mailer.close()
except:
    print 'Couldn\'t send email!'
