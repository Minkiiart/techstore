"""Tool: consulta un pedido por ID en SQLite, incluyendo historial del cliente."""
import sqlite3
from langchain_core.tools import tool
from config.settings import DB_PATH
from agent.memory.long_term import obtener_historial, contar_devoluciones_recientes


@tool
def consultar_pedido(pedido_id: str) -> dict:
    """Consulta los datos de un pedido por su ID y el historial del cliente.
    Devuelve un dict con producto, monto, fecha_compra, estado, cliente_id,
    historial_cliente (últimas decisiones) y devoluciones_previas_90d.
    Si el pedido no existe, devuelve {'error': '...'}.
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    row = conn.execute(
        "SELECT * FROM pedidos WHERE pedido_id = ?", (pedido_id,)
    ).fetchone()
    conn.close()
    if not row:
        return {"error": f"Pedido {pedido_id} no encontrado"}
    pedido = dict(row)
    pedido["historial_cliente"] = obtener_historial(pedido["cliente_id"], limite=3)
    pedido["devoluciones_previas_90d"] = contar_devoluciones_recientes(pedido["cliente_id"])
    return pedido


if __name__ == "__main__":
    print(consultar_pedido.invoke({"pedido_id": "PED-001"}))
