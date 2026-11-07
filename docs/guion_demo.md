# Guion de demostración — 10 minutos

## Minuto 0–1: Contexto
- Quiénes somos, qué problema resolvemos: automatizar el triage de devoluciones de TechStore.
- Mostrar Streamlit en pantalla: "Este es nuestro agente de devoluciones".

## Minuto 1–4: Caso estándar (IE1, IE2, IE3)
- Input: pedido **PED-001**.
- Mostrar el "trace" paso a paso en el expander de la UI:
  1. Consulta el pedido (`consultar_pedido`)
  2. Valida política (`validar_politica`)
  3. Calcula reembolso, genera etiqueta
  4. Actualiza CRM y notifica al cliente
- **Punto clave:** 7 pasos sin intervención humana, con traza completa visible.

## Minuto 4–6: Memoria de largo plazo (IE3, IE4)
- Vuelve a procesar **PED-001**: ahora el cliente tiene historial guardado (memoria de largo plazo en SQLite).
- El agente reconoce al cliente recurrente → aplica **aprobar_preferente** en vez de `aprobar_estandar`.
- **Punto clave:** la decisión cambió sin tocar el código — la memoria lo hizo posible.

## Minuto 6–8: Plot twist — replanificación (IE5, IE7)
- Input: **PED-022** (Tablet, $250.000 — alto valor).
- El agente detecta monto > $100.000.
- **Replanifica**: no aprueba automáticamente, pide aprobación de supervisor.
- **Punto clave:** ajustó su comportamiento ante condiciones distintas (regla de prioridad 2 antes que la 6).

## Minuto 8–9: Escalamiento (IE5, IE7)
- Input: **PED-015** (45 días desde la compra).
- El agente detecta "fuera de plazo (45 días, máximo 30)" con `validar_politica`.
- Escala con justificación clara y trazable.

## Minuto 9–10: Cierre (IE8, IE9, IE10)
- Mostrar el diagrama de orquestación (`docs/diagrama_orquestacion.md`).
- Mencionar: "README en GitHub, reproducible desde cero".
- Justificar brevemente: *flujo híbrido* (tools+planner determinístico para las 6 reglas + AgentExecutor con Gemini para razonamiento abierto), y *RAG con Chroma* para citar política/casos en vez de que el LLM "alucine".
- Cierre: "Resuelve automáticamente los casos estándar y preferentes, y escala con justificación el resto — sin perder trazabilidad."

## Preguntas (hasta 10 min)
Preparar respuesta para:
- ¿Por qué el flujo principal no depende del LLM? → Auditabilidad y continuidad ante fallas de cuota/Internet (plan B).
- ¿Qué pasa si cambia la política? → Se reindexa `politicas.md` en Chroma (`scripts/index_politicas.py`); los umbrales de negocio están centralizados en `config/settings.py`.
- ¿Cómo se prueba que el agente decide bien? → `pytest tests/` con 17 tests (tools, planner, end-to-end), ver `evidence/pytest_output.txt`.
- ¿Qué NO hace el agente? → Ver `docs/alcance.md` (no pagos reales, no courier real, no reclamos legales).

## Plan B (si falla Internet o la cuota de Gemini)
- El flujo principal (`procesar_solicitud`) **no usa el LLM**, solo tools + planner: la demo en Streamlit sigue funcionando.
- Tener un video de respaldo grabado en `evidence/videos/` (subir a Drive si pesa mucho y enlazar en el README).
- Tener `data/chroma_db/` ya generado antes de la exposición (no reindexar en vivo).

## Roles sugeridos (equipo de 2)
- **Expositor 1 (0–4 min):** contexto + caso estándar + memoria.
- **Expositor 2 (4–8 min):** plot twist (alto valor) + escalamiento + cierre técnico.
- **Ambos (8–10 min):** preguntas.
