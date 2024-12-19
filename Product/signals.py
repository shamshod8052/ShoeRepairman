import qrcode
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from django.core.files.base import ContentFile
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import Order


@receiver(post_save, sender=Order)
def generate_qr_code(sender, instance, created, **kwargs):
    if not created:
        return

    order_url = f"{settings.SITE_DOMAIN}/order/{instance.id}/"

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(order_url)
    qr.make(fit=True)

    qr_image = qr.make_image(fill_color="black", back_color="white").convert("RGB")

    qr_width, qr_height = qr_image.size
    new_height = qr_height + 60
    new_image = Image.new("RGB", (qr_width, new_height), "white")

    new_image.paste(qr_image, (0, 0, qr_width, qr_height))

    draw = ImageDraw.Draw(new_image)
    font_size = 40
    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except IOError:
        font = ImageFont.load_default()

    order_id_text = f"ID: {instance.id}"

    bbox = draw.textbbox((0, 0), order_id_text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    text_position = ((qr_width - text_width) // 2, qr_height + 1)
    draw.text(text_position, order_id_text, fill="black", font=font)

    buffer = BytesIO()
    new_image.save(buffer, format="PNG")
    buffer.seek(0)

    filename = f"order_{instance.id}.png"
    instance.qr_code.save(filename, ContentFile(buffer.read()), save=False)
    instance.save()
