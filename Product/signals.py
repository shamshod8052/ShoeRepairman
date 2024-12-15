import qrcode
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

    img = qr.make_image(fill_color="black", back_color="white")
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)

    filename = f"order_{instance.id}.png"
    instance.qr_code.save(filename, ContentFile(buffer.read()), save=False)
    instance.save()
