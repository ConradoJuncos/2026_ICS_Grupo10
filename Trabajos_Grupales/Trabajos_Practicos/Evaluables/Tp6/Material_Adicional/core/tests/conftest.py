"""Configuración compartida por las pruebas de la aplicación."""

from collections.abc import Iterator
from unittest.mock import MagicMock, patch

import pytest


@pytest.fixture(autouse=True)
def servidor_smtp() -> Iterator[MagicMock]:
    """Reemplaza el servidor de correo para que ninguna prueba envíe mails reales."""
    with patch("core.email.smtplib.SMTP") as mock_smtp:
        mock_server = MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_server
        yield mock_server
