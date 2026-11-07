"""Memoria de largo plazo: persistencia en SQLite."""
import sqlite3
from datetime import datetime
from config.settings import DB_PATH


def guardar_decision(cliente_id: str, pedido_id: str, decision: str,
                      monto: float, motivo: str) -> dict:
    """Guarda una decisión en el historial del cliente."""
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "INSERT INTO historial_cliente (cliente_id, pedido_id, fecha, decision, monto, motivo) "
        "VALUES (?, ?, ?, ?, ?, ?)",
        (cliente_id, pedido_id, datetime.now().isoformat(), decision, monto, motivo),
    )
    conn.commit()
    conn.close()
    return {"ok": True}


def obtener_historial(cliente_id: str, limite: int = 5) -> list[dict]:
    """Devuelve las últimas N decisiones del cliente."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    rows = conn.execute(
        "SELECT * FROM historial_cliente WHERE cliente_id = ? "
        "ORDER BY fecha DESC LIMIT ?",
        (cliente_id, limite),
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def contar_devoluciones_recientes(cliente_id: str) -> int:
    """Cuenta devoluciones del cliente (equivale al campo en clientes.csv)."""
    conn = sqlite3.connect(DB_PATH)
    row = conn.execute(
        "SELECT devoluciones_previas_90d FROM clientes WHERE cliente_id = ?",
        (cliente_id,),
    ).fetchone()
    conn.close()
    return row[0] if row else 0
