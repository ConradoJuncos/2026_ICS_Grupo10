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


@patch("core.email.smtplib.SMTP")
def test_enviar_mail_incluye_el_resumen_de_la_inscripcion(mock_smtp: MagicMock) -> None:
    """Agrega al cuerpo del correo el resumen recibido."""
    mock_server = MagicMock()
    mock_smtp.return_value.__enter__.return_value = mock_server

    enviar_mail_confirmacion_registro_a_actividad(
        "test@example.com", b"qr_falso", resumen="Tirolesa · 20/10/2026 · 10:00"
    )

    mensaje_enviado = mock_server.send_message.call_args[0][0]
    cuerpo = mensaje_enviado.get_body(preferencelist=("html",)).get_content()
    assert "Tirolesa · 20/10/2026 · 10:00" in cuerpo


@patch("core.email.smtplib.SMTP")
def test_enviar_mail_escapa_el_html_del_resumen(mock_smtp: MagicMock) -> None:
    """Muestra como texto los caracteres especiales del resumen."""
    mock_server = MagicMock()
    mock_smtp.return_value.__enter__.return_value = mock_server

    enviar_mail_confirmacion_registro_a_actividad(
        "test@example.com", b"qr_falso", resumen="Ana <b>Pérez</b>"
    )

    mensaje_enviado = mock_server.send_message.call_args[0][0]
    cuerpo = mensaje_enviado.get_body(preferencelist=("html",)).get_content()
    assert "Ana &lt;b&gt;Pérez&lt;/b&gt;" in cuerpo
