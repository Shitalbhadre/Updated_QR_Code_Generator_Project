import qrcode
import os
from modules.utils import add_qrcode

def generate_qr(user_id, content, qr_type="Text", color="#000000", bgcolor="#FFFFFF", logo_path=None):
    # Create QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(content)
    qr.make(fit=True)
    img = qr.make_image(fill_color=color, back_color=bgcolor).convert("RGB")

    # Add logo if provided
    if logo_path and os.path.exists(logo_path):
        from PIL import Image
        logo = Image.open(logo_path)
        box_size = img.size[0] // 4
        logo = logo.resize((box_size, box_size))
        pos = ((img.size[0]-box_size)//2, (img.size[1]-box_size)//2)
        img.paste(logo, pos)

    # Save QR image
    if not os.path.exists("assets/qrcodes"):
        os.makedirs("assets/qrcodes")
    file_path = os.path.join("assets/qrcodes", f"{user_id}_{int(os.times()[4])}.png")
    img.save(file_path)

    # Save to MongoDB
    add_qrcode(user_id=user_id, qr_type=qr_type, content=content, file_path=file_path)

    return file_path
