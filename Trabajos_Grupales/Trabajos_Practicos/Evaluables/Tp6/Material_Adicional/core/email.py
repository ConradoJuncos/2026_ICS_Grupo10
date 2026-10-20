import smtplib
from email.message import EmailMessage
from html import escape


def enviar_mail_confirmacion_registro_a_actividad(
    destinatario: str, qr: bytes, resumen: str = ""
):
    msg = EmailMessage()
    msg["Subject"] = "Confirmación de Registro"
    msg["From"] = "noreply@example.com"
    msg["To"] = destinatario

    msg.set_content(
        f"""\
    <html>
        <body>
            <p>{escape(resumen)}</p>
            <p>Test qr codigo:</p>
            <img src="cid:qr_code" alt="Código QR">
        </body>
    </html>
    """,
        subtype="html",
    )

    # El cid permite que el HTML muestre el QR inline en lugar de adjunto.
    msg.add_related(qr, maintype="image", subtype="png", cid="qr_code")

    with smtplib.SMTP("localhost", 1025) as server:
        server.send_message(msg)
