import os
from email.message import EmailMessage
import ssl
import smtplib


class MailSender:

    def email_alert(self, subject_in, body_in, to_in):
        msg_sender = "instantpay529@gmail.com"
        msg_password = 'dlzetlrbctmnbqlk'
        msg_receiver2 = to_in

        subject = subject_in
        body = body_in

        em = EmailMessage()
        em['From'] = msg_sender
        em['To'] = msg_receiver2
        em['Subject'] = subject
        em.set_content(body)

        content = ssl.create_default_context()

        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=content) as smtp:
            smtp.login(msg_sender, msg_password)
            smtp.sendmail(msg_sender, msg_receiver2, em.as_string())


if __name__ == '__main__':
    my_object = MailSender()
    my_object.email_alert("Account Registration", """
Congratulations! 
You have successfully created
an account with instant pay e_wallet
""", "olaitanblessinge@gmail.com")

    # Zainab Alayande
    # sunepao9152 @ gmail.com