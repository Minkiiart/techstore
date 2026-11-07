"""Planner: decide la acción del agente según el estado."""
from dataclasses import dataclass
from config.settings import (
    UMBRAL_APROBACION, UMBRAL_PREFERENTE, UMBRAL_FRAUDE,
)


@dataclass
class Accion:
    tipo: str
    razon: str


def decidir_accion(estado: dict) -> Accion:
    """Aplica las 6 reglas en orden de prioridad.

    estado esperado:
      - elegible: bool
      - monto: float
      - devoluciones_previas: int
      - cliente_recurrente: bool
      - falta_info: bool
    """
    # Regla 1: no elegible
    if not estado.get("elegible", True):
        return Accion("escalar", estado.get("razon", "No elegible"))

    # Regla 2: monto alto
    if estado.get("monto", 0) > UMBRAL_APROBACION:
        return Accion("solicitar_aprobacion",
                       f"Monto ${estado['monto']:,} > ${UMBRAL_APROBACION:,}")

    # Regla 3: fraude
    if estado.get("devoluciones_previas", 0) >= UMBRAL_FRAUDE:
        return Accion("escalar_fraude",
                       f"{estado['devoluciones_previas']} devoluciones en 90 días")

    # Regla 4: cliente recurrente
    if (estado.get("cliente_recurrente")
            and estado.get("monto", 0) < UMBRAL_PREFERENTE):
        return Accion("aprobar_preferente",
                       "Cliente recurrente, monto bajo")

    # Regla 5: falta info
    if estado.get("falta_info"):
        return Accion("solicitar_info", "Falta comprobante o descripción")

    # Regla 6: default
    return Accion("aprobar_estandar", "Caso estándar dentro de política")


def construir_estado(pedido: dict, validacion: dict) -> dict:
    """Arma el estado que consume decidir_accion."""
    return {
        "elegible": validacion.get("elegible", False),
        "razon": validacion.get("razon", ""),
        "monto": pedido.get("monto", 0),
        "devoluciones_previas": pedido.get("devoluciones_previas_90d", 0),
        "cliente_recurrente": len(pedido.get("historial_cliente", [])) > 0,
        "falta_info": not pedido.get("motivo_devolucion"),
    }
