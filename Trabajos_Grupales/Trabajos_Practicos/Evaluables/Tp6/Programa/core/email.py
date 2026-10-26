"""Envía los correos de confirmación de inscripción a los visitantes."""

import smtplib
from email.message import EmailMessage
from email.utils import make_msgid

from django.conf import settings
from django.template.loader import render_to_string


def enviar_mail_confirmacion_registro_a_actividad(
    destinatario: str, qr: bytes, resumen: str = ""
) -> None:
    """Envía el resumen de la inscripción con su código QR incrustado."""
    cid_qr = make_msgid(domain="ecoharmony.park")
    msg = EmailMessage()
    msg["Subject"] = "Tu inscripción en EcoHarmony Park está confirmada"
    msg["From"] = "EcoHarmony Park <noreply@example.com>"
    msg["To"] = destinatario
    msg.set_content(
        render_to_string(
            "core/correo_confirmacion.html",
            {"resumen": resumen, "cid_qr": cid_qr[1:-1]},
        ),
        subtype="html",
    )

    # El cid permite que el HTML muestre el QR inline en lugar de adjunto.
    msg.add_related(qr, maintype="image", subtype="png", cid=cid_qr)

    with smtplib.SMTP(settings.CORREO_SMTP_HOST, settings.CORREO_SMTP_PUERTO) as server:
        server.send_message(msg)
