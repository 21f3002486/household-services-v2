import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

SMTP_SERVER = 'localhost'
SMTP_PORT = 1025
SENDER_EMAIL = 'admin@gmail.com'
SENDER_PASSWORD = ''


def sendmail(to, subject, content):
    msg = MIMEMultipart()

    msg["To"] = to
    msg["Subject"] = subject
    msg["From"] = SENDER_EMAIL

    msg.attach(MIMEText(content, 'text'))

    client = smtplib.SMTP(host=SMTP_SERVER, port=SMTP_PORT)

    client.send_message(msg=msg)

    client.quit()