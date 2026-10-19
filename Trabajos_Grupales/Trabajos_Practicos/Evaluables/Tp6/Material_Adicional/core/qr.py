import io
import segno  # libreria utilizada para generar qrs


class GenerarQr:
    # Añadidos parametros basicos en caso de no ser pasados
    def __init__(self, scale: int = 10, error: str = "m"):
        self.scale = scale
        self.error = error

    def generate(self, data: str) -> bytes:
        qr = segno.make(data, error=self.error)
        buffer = io.BytesIO()
        qr.save(buffer, kind="png", scale=self.scale)
        buffer.seek(0)
        return buffer.getvalue()
