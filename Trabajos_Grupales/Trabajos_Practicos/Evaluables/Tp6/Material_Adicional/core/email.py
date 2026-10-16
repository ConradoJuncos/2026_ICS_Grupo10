import smtplib
from email.message import EmailMessage

def enviar_mail_confirmacion_registro_a_actividad(destinatario: str, qr: bytes):
    msg = EmailMessage()
    # Informacion del mail, asunto, de quien, para quien
    msg['Subject'] = "Confirmación de Registro"
    msg['From'] = "noreply@example.com"
    msg['To'] = destinatario
    
    # Cuerpo del mensaje, con html
    msg.set_content("""\
    <html>
        <body>
            <p>Test qr codigo:</p>
            <img src="cid:qr_code" alt="Código QR">
        </body>
    </html>
    """, subtype='html')
    
    # Añade la imagen del qr, usando magia que no comprendo
    msg.add_related(
        qr,
        maintype='image',
        subtype='png',
        cid='qr_code'
    )
    
    # Envio del mail efectivamente
    with smtplib.SMTP('localhost', 1025) as server:
        server.send_message(msg)