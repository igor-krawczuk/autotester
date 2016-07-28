import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.mime.text import MIMEText

class MailNotificator(object):

    def __init__(self, target_mail, server,port, fromaddr,password):
        self.target = target_mail
        self.port =  port
        self.server_url = server
        self.fromaddr=fromaddr
        self.password = password


    def done(self):
        self.send("The current test run is finished" )

    def send(self, body, subject=None):
        if subject is None:
            if len(body)>=20:
                subject=body[:20]
            else:
                subject=body
        msg = MIMEMultipart()
        msg["From"]=self.fromaddr
        msg["To"]=self.target
        msg["Subject"]=subject
        msg.attach(MIMEText(body,"PLAIN"))

        server = smtplib.SMTP(self.server_url, self.port)
        server.starttls()
        server.login(self.fromaddr,self.password)
        text = msg.as_string()
        server.sendmail(self.fromaddr, self.target, text)
        server.quit()


