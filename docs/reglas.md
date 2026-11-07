# Reglas de decisión (orden de prioridad)

| # | Condición | Acción | Razón |
|---|---|---|---|
| 1 | No elegible (fuera de plazo o producto no elegible) | escalar | Política |
| 2 | Monto > $100.000 | solicitar_aprobacion | Riesgo financiero |
| 3 | Cliente con ≥3 devoluciones en 90 días | escalar_fraude | Prevención |
| 4 | Cliente recurrente y monto < $50.000 | aprobar_preferente | Fidelización |
| 5 | Falta comprobante o descripción | solicitar_info | Completitud |
| 6 | Caso estándar | aprobar_estandar | Flujo feliz |

El agente evalúa las reglas de arriba hacia abajo y se detiene en la primera que se cumple.
