"""Envía los correos de confirmación de inscripción a los visitantes."""

import smtplib
from email.message import EmailMessage
from html import escape

from django.conf import settings


def enviar_mail_confirmacion_registro_a_actividad(
    destinatario: str, qr: bytes, resumen: str = ""
) -> None:
    """Envía el resumen de la inscripción con su código QR incrustado."""
    resumen_html = escape(resumen).replace("\n", "<br>")
    msg = EmailMessage()
    msg["Subject"] = "Confirmación de Registro"
    msg["From"] = "noreply@example.com"
    msg["To"] = destinatario

    msg.set_content(
        f"""\
    <html>
        <body>
            <p>Tu inscripción a EcoHarmony Park está confirmada.</p>
            <p>{resumen_html}</p>
            <p>Presentá este código QR al llegar a la actividad.</p>
            <img src="cid:qr_code" alt="Código QR">
        </body>
    </html>
    """,
        subtype="html",
    )

    # El cid permite que el HTML muestre el QR inline en lugar de adjunto.
    msg.add_related(qr, maintype="image", subtype="png", cid="qr_code")

    with smtplib.SMTP(settings.CORREO_SMTP_HOST, settings.CORREO_SMTP_PUERTO) as server:
        server.send_message(msg)
