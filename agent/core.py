"""Orquestador del agente TechStore Returns."""
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate

from config.settings import GOOGLE_API_KEY, LLM_MODEL
from agent.tools.consultar_pedido import consultar_pedido
from agent.tools.validar_politica import validar_politica
from agent.tools.calcular_reembolso import calcular_reembolso
from agent.tools.generar_etiqueta import generar_etiqueta
from agent.tools.actualizar_crm import actualizar_crm
from agent.tools.notificar_cliente import notificar_cliente
from agent.tools.buscar_casos import buscar_casos_similares
from agent.planner import decidir_accion, construir_estado
from agent.memory.long_term import guardar_decision

TOOLS = [
    consultar_pedido, validar_politica, calcular_reembolso,
    generar_etiqueta, actualizar_crm, notificar_cliente,
    buscar_casos_similares,
]

PROMPT = ChatPromptTemplate.from_messages([
    ("system",
     "Eres un agente de devoluciones de TechStore. Sigue este proceso:\n"
     "1. Consulta el pedido con consultar_pedido.\n"
     "2. Valida la política con validar_politica.\n"
     "3. Busca casos similares con buscar_casos_similares.\n"
     "4. Ejecuta las acciones que correspondan (reembolso, etiqueta, CRM, notificación).\n"
     "Sé claro, breve y justifica cada decisión con la política o caso citado."),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}"),
])


def crear_agente():
    """Crea el AgentExecutor con todas las tools (razonamiento libre vía LLM)."""
    llm = ChatGoogleGenerativeAI(
        model=LLM_MODEL,
        google_api_key=GOOGLE_API_KEY,
        temperature=0.2,
    )
    agent = create_tool_calling_agent(llm, TOOLS, PROMPT)
    return AgentExecutor(agent=agent, tools=TOOLS, verbose=True, max_iterations=8)


def procesar_solicitud(pedido_id: str, motivo: str = "") -> dict:
    """Flujo determinístico (tools + planner) que resuelve una solicitud de devolución.

    Este es el punto de entrada que usa Streamlit. Es trazable y no depende
    de Internet/LLM, por lo que funciona como plan B durante la demo.
    """
    # 1. Triage determinístico (usa las tools como funciones, sin LLM)
    pedido = consultar_pedido.invoke({"pedido_id": pedido_id})
    if "error" in pedido:
        return {"ok": False, "error": pedido["error"]}

    validacion = validar_politica.invoke({"pedido_id": pedido_id})
    estado = construir_estado(pedido, validacion)
    accion = decidir_accion(estado)

    # 2. Ejecutar acciones según la decisión
    resultado = {"pedido_id": pedido_id, "accion": accion.tipo,
                 "razon": accion.razon, "pedido": pedido, "validacion": validacion}

    if accion.tipo in ("aprobar_estandar", "aprobar_preferente"):
        reembolso = calcular_reembolso.invoke({"pedido_id": pedido_id})
        etiqueta = generar_etiqueta.invoke({"pedido_id": pedido_id})
        actualizar_crm.invoke({"pedido_id": pedido_id, "estado": "aprobado",
                                "nota": accion.razon})
        notificar_cliente.invoke({"cliente_id": pedido["cliente_id"],
                                   "mensaje": f"Tu devolución fue aprobada. Etiqueta: {etiqueta['codigo']}"})
        guardar_decision(pedido["cliente_id"], pedido_id, "aprobado",
                          reembolso["monto"], accion.razon)
        resultado.update({"reembolso": reembolso, "etiqueta": etiqueta})

    elif accion.tipo in ("escalar", "escalar_fraude", "solicitar_aprobacion"):
        actualizar_crm.invoke({"pedido_id": pedido_id, "estado": accion.tipo,
                                "nota": accion.razon})
        notificar_cliente.invoke({"cliente_id": pedido["cliente_id"],
                                   "mensaje": f"Tu caso requiere revisión: {accion.razon}"})
        guardar_decision(pedido["cliente_id"], pedido_id, accion.tipo, 0, accion.razon)

    elif accion.tipo == "solicitar_info":
        notificar_cliente.invoke({"cliente_id": pedido["cliente_id"],
                                   "mensaje": "Necesitamos más información para procesar tu devolución."})

    return {"ok": True, **resultado}
