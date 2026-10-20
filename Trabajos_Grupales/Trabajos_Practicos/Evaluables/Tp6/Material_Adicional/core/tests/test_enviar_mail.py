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


def cuerpo_del_correo_enviado(resumen: str) -> str:
    """Envía el correo a un servidor simulado y devuelve su cuerpo HTML."""
    with patch("core.email.smtplib.SMTP") as mock_smtp:
        mock_server = MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_server
        enviar_mail_confirmacion_registro_a_actividad(
            "test@example.com", b"qr_falso", resumen=resumen
        )
    mensaje_enviado = mock_server.send_message.call_args[0][0]
    return str(mensaje_enviado.get_body(preferencelist=("html",)).get_content())


def test_enviar_mail_incluye_el_resumen_de_la_inscripcion() -> None:
    """Agrega al cuerpo del correo el resumen recibido."""
    cuerpo = cuerpo_del_correo_enviado("Tirolesa · 20/10/2026 · 10:00")

    assert "Tirolesa · 20/10/2026 · 10:00" in cuerpo


def test_enviar_mail_escapa_el_html_del_resumen() -> None:
    """Muestra como texto los caracteres especiales del resumen."""
    cuerpo = cuerpo_del_correo_enviado("Ana <b>Pérez</b>")

    assert "Ana &lt;b&gt;Pérez&lt;/b&gt;" in cuerpo


def test_enviar_mail_conserva_los_saltos_de_linea_del_resumen() -> None:
    """Muestra cada línea del resumen en un renglón propio."""
    cuerpo = cuerpo_del_correo_enviado("Ana Pérez\nJuan Pérez")

    assert "Ana Pérez<br>Juan Pérez" in cuerpo
