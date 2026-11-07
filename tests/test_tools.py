"""Tests de las tools."""
from agent.tools.consultar_pedido import consultar_pedido
from agent.tools.validar_politica import validar_politica
from agent.tools.calcular_reembolso import calcular_reembolso
from agent.tools.generar_etiqueta import generar_etiqueta
from agent.memory.long_term import guardar_decision, obtener_historial


def test_consultar_pedido_existente():
    r = consultar_pedido.invoke({"pedido_id": "PED-001"})
    assert "error" not in r
    assert r["pedido_id"] == "PED-001"
    assert r["monto"] > 0


def test_consultar_pedido_inexistente():
    r = consultar_pedido.invoke({"pedido_id": "PED-999"})
    assert "error" in r


def test_validar_politica_dentro_de_plazo():
    r = validar_politica.invoke({"pedido_id": "PED-001"})
    assert "elegible" in r


def test_validar_politica_fuera_de_plazo():
    r = validar_politica.invoke({"pedido_id": "PED-015"})
    assert r["elegible"] is False


def test_calcular_reembolso():
    r = calcular_reembolso.invoke({"pedido_id": "PED-001", "tipo": "total"})
    assert r["monto"] > 0
    assert r["moneda"] == "CLP"


def test_generar_etiqueta():
    r = generar_etiqueta.invoke({"pedido_id": "PED-001"})
    assert r["codigo"].startswith("RET-PED-001")


def test_guardar_y_recuperar_historial():
    guardar_decision("C-001", "PED-001", "aprobado", 45000, "test")
    historial = obtener_historial("C-001", limite=1)
    assert len(historial) == 1
    assert historial[0]["decision"] == "aprobado"
