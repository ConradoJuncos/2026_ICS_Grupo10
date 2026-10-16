import io
import segno

class GenerarQr:
    def generate(self, data: str) -> bytes:
        buffer = io.BytesIO()
        segno.make(data).save(buffer, kind="png")
        buffer.seek(0)
        return buffer.getvalue()