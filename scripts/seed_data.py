"""Carga los CSV en SQLite para consultas rápidas."""
import sqlite3
import pandas as pd
from config.settings import DB_PATH, DATA_DIR

DB_PATH.parent.mkdir(exist_ok=True)
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.executescript("""
DROP TABLE IF EXISTS pedidos;
DROP TABLE IF EXISTS clientes;
DROP TABLE IF EXISTS historial_cliente;

CREATE TABLE pedidos (
    pedido_id TEXT PRIMARY KEY,
    cliente_id TEXT,
    producto TEXT,
    categoria TEXT,
    monto REAL,
    fecha_compra TEXT,
    estado TEXT,
    motivo_devolucion TEXT
);

CREATE TABLE clientes (
    cliente_id TEXT PRIMARY KEY,
    nombre TEXT,
    email TEXT,
    devoluciones_previas_90d INTEGER
);

CREATE TABLE historial_cliente (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cliente_id TEXT,
    pedido_id TEXT,
    fecha TEXT,
    decision TEXT,
    monto REAL,
    motivo TEXT
);
""")

pd.read_csv(DATA_DIR / "pedidos.csv").to_sql("pedidos", conn, if_exists="append", index=False)
pd.read_csv(DATA_DIR / "clientes.csv").to_sql("clientes", conn, if_exists="append", index=False)
conn.commit()
conn.close()
print(f"SQLite listo en {DB_PATH}")
