import mimetypes
import os
import smtplib
from email.message import EmailMessage
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import make_msgid

from config import MAIL_MESSAGE


def send_carton_mail_old(carton, qr_path, to):

    image_cid = make_msgid(domain='xyz.com')

    mail_body = {
        "name": carton.get("name"),
        "nbItems": carton.get("nbItems"),
        "content": "<br />".join([i.get('label') for i in carton.get("items")]),
        "img": image_cid[1:-1]
    }

    server_ssl = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server_ssl.login(
        os.environ.get("GMAIL_LOGIN"),
        os.environ.get("GMAIL_PASSWORD"),
    )

    msg = EmailMessage()
    msg['Subject'] = f"QR Code pour carton {carton.get('name')}"
    msg['From'] = os.environ.get("GMAIL_LOGIN")
    msg['To'] = to
    msg.add_alternative(
        MAIL_MESSAGE.format(**mail_body)
    )

    with open(qr_path, 'rb') as img:
        # know the Content-Type of the image
        maintype, subtype = mimetypes.guess_type(img.name)[0].split('/')

        # attach it
        msg.get_payload()[0].add_related(img.read(),
                                         maintype=maintype,
                                         subtype=subtype,
                                         cid=image_cid)

    # server_ssl.sendmail(
    #     os.environ.get("GMAIL_LOGIN"),
    #     to,
    #     msg.as_string()
    # )
    server_ssl.send_message(msg)
    server_ssl.close()


def send_carton_mail(carton, qr_path, to):

    # Define these once; use them twice!
    strFrom = os.environ.get("GMAIL_LOGIN")
    strTo = to

    # Create the root message and fill in the from, to, and subject headers
    msgRoot = MIMEMultipart('related')
    msgRoot['Subject'] = f"QR Code pour carton {carton.get('name')}"
    msgRoot['From'] = strFrom
    msgRoot['To'] = strTo
    msgRoot.preamble = ''

    mail_body = {
        "name": carton.get("name"),
        "nbItems": carton.get("nbItems"),
        "content": "<br /> - ".join([i.get('label') for i in carton.get("items")]),
        # "img": image_cid[1:-1]
    }

    # Encapsulate the plain and HTML versions of the message body in an
    # 'alternative' part, so message agents can decide which they want to display.
    msgAlternative = MIMEMultipart('alternative')
    msgRoot.attach(msgAlternative)

    # msgText = MIMEText('This is the alternative plain text message.')
    # msgAlternative.attach(msgText)

    # We reference the image in the IMG SRC attribute by the ID we give it below
    msgText = MIMEText(MAIL_MESSAGE.format(**mail_body), 'html')
    msgAlternative.attach(msgText)

    # This example assumes the image is in the current directory
    fp = open(qr_path, 'rb')
    msgImage = MIMEImage(fp.read())
    fp.close()

    # Define the image's ID as referenced above
    msgImage.add_header('Content-ID', '<image1>')
    msgRoot.attach(msgImage)

    # Send the email (this example assumes SMTP authentication is required)
    server_ssl = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server_ssl.login(
        os.environ.get("GMAIL_LOGIN"),
        os.environ.get("GMAIL_PASSWORD"),
    )
    server_ssl.sendmail(strFrom, strTo, msgRoot.as_string())
    server_ssl.quit()
