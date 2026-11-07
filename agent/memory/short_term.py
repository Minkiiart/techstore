"""Memoria de corto plazo: buffer de conversación."""
from langchain.memory import ConversationBufferMemory


def crear_memoria_corto_plazo() -> ConversationBufferMemory:
    """Crea una memoria de conversación en RAM.
    Se guarda en st.session_state para persistir durante la sesión.
    """
    return ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True,
        output_key="output",
    )
