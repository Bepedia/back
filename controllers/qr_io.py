import qrcode
import uuid


def generate_qr(url):
    img = qrcode.make(url)
    img_name = f"/tmp/{str(uuid.uuid4())}.png"
    img.save(img_name)
    return img_name
