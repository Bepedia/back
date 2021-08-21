from dotenv import load_dotenv

load_dotenv()

MAIL_MESSAGE = """
<html>
<body>
    Contenu: <br /> <br />
    {content}
    <br />
    <br />
    QR Code: <br /> <br />
    <img src="cid:image1" />
</body>
</html>
"""
