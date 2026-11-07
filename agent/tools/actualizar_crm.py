"""Tool: actualiza el estado del ticket en el CRM (mock = SQLite)."""
import sqlite3
from datetime import datetime
from langchain_core.tools import tool
from config.settings import DB_PATH


@tool
def actualizar_crm(pedido_id: str, estado: str, nota: str = "") -> dict:
    """Actualiza el estado del ticket en el CRM.
    estado: 'aprobado', 'escalado', 'pendiente_aprobacion', 'rechazado'.
    Devuelve {'ok': bool}.
    """
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "INSERT INTO historial_cliente (cliente_id, pedido_id, fecha, decision, monto, motivo) "
        "SELECT cliente_id, pedido_id, ?, ?, monto, ? FROM pedidos WHERE pedido_id = ?",
        (datetime.now().isoformat(), estado, nota, pedido_id),
    )
    conn.commit()
    conn.close()
    return {"ok": True, "estado": estado}
