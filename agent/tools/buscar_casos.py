"""Tool: recupera políticas y casos similares (RAG)."""
from functools import lru_cache
from langchain_chroma import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.tools import tool
from config.settings import CHROMA_DIR


@lru_cache(maxsize=2)
def _get_db(coleccion: str):
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    return Chroma(
        collection_name=coleccion,
        embedding_function=embeddings,
        persist_directory=str(CHROMA_DIR),
    )


@tool
def buscar_casos_similares(texto: str) -> list[dict]:
    """Busca políticas y casos previos similares al texto dado.
    Devuelve una lista de fragmentos relevantes con su fuente.
    """
    db = _get_db("casos_previos")
    casos = db.similarity_search(texto, k=2)
    db_pol = _get_db("politicas")
    politicas = db_pol.similarity_search(texto, k=2)

    return [
        {"tipo": "caso", "texto": d.page_content, "meta": d.metadata}
        for d in casos
    ] + [
        {"tipo": "politica", "texto": d.page_content, "meta": d.metadata}
        for d in politicas
    ]
