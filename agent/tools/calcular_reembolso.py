"""Tool: calcula el reembolso."""
import sqlite3
from langchain_core.tools import tool
from config.settings import DB_PATH


@tool
def calcular_reembolso(pedido_id: str, tipo: str = "total") -> dict:
    """Calcula el monto de reembolso. tipo: 'total' o 'parcial'.
    Devuelve {'monto': float, 'moneda': 'CLP'}.
    """
    conn = sqlite3.connect(DB_PATH)
    row = conn.execute(
        "SELECT monto FROM pedidos WHERE pedido_id = ?", (pedido_id,)
    ).fetchone()
    conn.close()
    if not row:
        return {"error": "Pedido no encontrado"}
    monto = float(row[0])
    if tipo == "parcial":
        monto *= 0.5
    return {"monto": round(monto, 2), "moneda": "CLP"}
