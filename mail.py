import smtplib
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

def send_mail_packet(b64_image_str, text_message):
    sender = "mailagent4chang@gmail.com"
    password = 'ylck gbnn pznz qutu'
    receiver = "chandraprakash.changu@gmail.com"

    msg = MIMEMultipart()
    msg["From"] = sender
    msg["To"] = receiver
    msg["Subject"] = "Packet"

    if not b64_image_str:
        msg.attach(MIMEText("no image\n\n" + text_message, "plain"))
    else:
        msg.attach(MIMEText(text_message, "plain"))
        raw = base64.b64decode(b64_image_str)
        part = MIMEBase("application", "octet-stream")
        part.set_payload(raw)
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", "attachment; filename=capture.jpg")
        msg.attach(part)

    s = smtplib.SMTP("smtp.gmail.com", 587)
    s.starttls()
    s.login(sender, password)
    s.sendmail(sender, receiver, msg.as_string())
    print('sent mail ...')
    s.quit()
