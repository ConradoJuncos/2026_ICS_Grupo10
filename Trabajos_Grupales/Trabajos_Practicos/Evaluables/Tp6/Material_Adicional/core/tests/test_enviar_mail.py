"""Comprueba el envío del correo de confirmación."""

from unittest.mock import MagicMock, patch

from core.email import enviar_mail_confirmacion_registro_a_actividad


@patch("core.email.smtplib.SMTP")
def test_enviar_mail_registro_actividad(mock_smtp: MagicMock) -> None:
    """Entrega el correo al servidor SMTP sin usar un servidor real."""
    mock_server = MagicMock()
    mock_smtp.return_value.__enter__.return_value = mock_server

    enviar_mail_confirmacion_registro_a_actividad("test@example.com", b"qr_falso")

    mock_server.send_message.assert_called_once()
