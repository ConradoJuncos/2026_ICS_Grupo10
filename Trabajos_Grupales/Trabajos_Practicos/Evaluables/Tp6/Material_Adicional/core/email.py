import smtplib
from email.message import EmailMessage

def enviar_mail_confirmacion_registro_a_actividad(destinatario: str, qr: bytes):
    # Construir el contenidod el mail
    msg = EmailMessage()
    msg['Subject'] = "Confirmación de registro a actividad"
    msg['From'] = "noreply@example.com"
    msg['To'] = destinatario
    msg.set_content("test.")
    
    # Añadir el QR como archivo adjunto
    msg.add_attachment(
        qr,
        maintype='image',
        subtype='png',
        filename='qr.png'
    )

    # Conectar al servidor SMTP y enviar el mail
    with smtplib.SMTP('localhost', 1025) as server:
        server.send_message(msg)