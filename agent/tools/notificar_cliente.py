"""Tool: envía notificación simulada al cliente."""
from langchain_core.tools import tool


@tool
def notificar_cliente(cliente_id: str, mensaje: str) -> dict:
    """Registra una notificación simulada para el cliente.
    Devuelve {'ok': bool, 'canal': str}.
    """
    # En un caso real, aquí se conectaría un email/SMS.
    print(f"[NOTIF] -> {cliente_id}: {mensaje}")
    return {"ok": True, "canal": "mock", "cliente_id": cliente_id}
