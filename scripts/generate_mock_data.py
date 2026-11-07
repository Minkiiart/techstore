"""Genera datos ficticios para TechStore."""
import csv
import random
from datetime import datetime, timedelta

random.seed(42)

PRODUCTOS = [
    ("Audífonos Bluetooth", "audio", 45000),
    ("Mouse inalámbrico", "accesorios", 25000),
    ("Teclado mecánico", "accesorios", 85000),
    ("Monitor 24\"", "pantalla", 180000),
    ("Cargador USB-C", "accesorios", 15000),
    ("Parlante portátil", "audio", 65000),
    ("Webcam HD", "accesorios", 40000),
    ("Tablet 10\"", "tablet", 250000),
    ("Smartwatch", "wearable", 120000),
    ("Cable HDMI", "accesorios", 12000),
]
MOTIVOS = ["producto defectuoso", "no era lo que esperaba", "llegó dañado",
           "talla equivocada", "cambio de opinión", "producto incompleto"]
ESTADOS = ["entregado", "entregado", "entregado", "en_transito"]

hoy = datetime(2025, 10, 15)

with open("data/pedidos.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["pedido_id", "cliente_id", "producto", "categoria",
                "monto", "fecha_compra", "estado", "motivo_devolucion"])
    for i in range(1, 41):
        prod, cat, precio = random.choice(PRODUCTOS)
        # Forzar escenarios específicos
        if i == 15:  # Fuera de plazo
            dias_atras = 45
        elif i == 22:  # Alto valor
            prod, cat, precio = "Tablet 10\"", "tablet", 250000
            dias_atras = 10
        else:
            dias_atras = random.randint(1, 28)
        fecha = (hoy - timedelta(days=dias_atras)).strftime("%Y-%m-%d")
        cliente = f"C-{random.randint(1,15):03d}"
        w.writerow([f"PED-{i:03d}", cliente, prod, cat, precio,
                    fecha, random.choice(ESTADOS), random.choice(MOTIVOS)])

with open("data/clientes.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["cliente_id", "nombre", "email", "devoluciones_previas_90d"])
    for i in range(1, 16):
        w.writerow([f"C-{i:03d}", f"Cliente {i}",
                    f"cliente{i}@example.com", random.randint(0, 5)])

print("Datos generados en data/")
