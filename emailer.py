#!/usr/bin/env python

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import config

def sendMail(subject, content):

    me = config.email['email_from']
    you = config.email['email_to']
    
    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = me
    msg['To'] = you
    
    html = """\
    <html>
      <head></head>
      <body>
        {0}
      </body>
    </html>
    """.format(content)
    
    content = MIMEText(html, 'html')
    
    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    msg.attach(content)
    
    username = config.email['username']
    password = config.email['password']
    # Send the message via local SMTP server.
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo()
    server.starttls()
    server.login(username,password)
    # sendmail function takes 3 arguments: sender's address, recipient's address
    # and message to send - here it is sent as one string.
    server.sendmail(me, you, msg.as_string())
    server.quit()

if __name__ == '__main__':
    sendMail(
        subject = "test email from emailer.py", 
        content = 'Here is some html email content with a <a href="http://google.com">link to Google</a>.')