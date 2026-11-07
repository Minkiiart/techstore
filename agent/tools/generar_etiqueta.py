"""Tool: genera etiqueta mock de devolución."""
import uuid
from langchain_core.tools import tool


@tool
def generar_etiqueta(pedido_id: str) -> dict:
    """Genera una etiqueta de envío mock para devolución.
    Devuelve {'codigo': str, 'url': str}.
    """
    codigo = f"RET-{pedido_id}-{uuid.uuid4().hex[:6].upper()}"
    return {"codigo": codigo,
            "url": f"https://techstore-fake.local/etiquetas/{codigo}.pdf"}
