from agent.planner import decidir_accion


def test_escalar_por_no_elegible():
    a = decidir_accion({"elegible": False})
    assert a.tipo == "escalar"


def test_escalar_por_fuera_de_plazo():
    a = decidir_accion({"elegible": False, "razon": "Fuera de plazo"})
    assert a.tipo == "escalar"
    assert "plazo" in a.razon.lower()


def test_solicitar_aprobacion_por_monto_alto():
    a = decidir_accion({"elegible": True, "monto": 150_000})
    assert a.tipo == "solicitar_aprobacion"


def test_escalar_por_fraude():
    a = decidir_accion({"elegible": True, "monto": 40_000, "devoluciones_previas": 4})
    assert a.tipo == "escalar_fraude"


def test_aprobar_preferente():
    a = decidir_accion({"elegible": True, "monto": 30_000,
                         "cliente_recurrente": True})
    assert a.tipo == "aprobar_preferente"


def test_aprobar_estandar():
    a = decidir_accion({"elegible": True, "monto": 20_000})
    assert a.tipo == "aprobar_estandar"
