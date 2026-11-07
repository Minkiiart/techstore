"""Indexa políticas y casos históricos en Chroma."""
from langchain_chroma import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document
from config.settings import DATA_DIR, CHROMA_DIR

# Modelo de embeddings gratuito y local
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# 1. Indexar políticas (chunk por sección markdown)
politicas_texto = (DATA_DIR / "politicas.md").read_text(encoding="utf-8")
secciones = [s.strip() for s in politicas_texto.split("\n## ") if s.strip()]
docs_politicas = [
    Document(page_content=s, metadata={"fuente": "politicas.md", "seccion": f"S{i}"})
    for i, s in enumerate(secciones)
]

# 2. Indexar casos previos (ejemplos ficticios)
casos = [
    "Caso: cliente devolvió audífonos por defecto, dentro de plazo, se aprobó reembolso total.",
    "Caso: cliente intentó devolver tablet de $250.000 fuera de plazo, se escaló a supervisor.",
    "Caso: cliente recurrente con 5 devoluciones en 90 días, se marcó para revisión antifraude.",
    "Caso: cliente con historial limpio pidió devolución de $30.000, se aprobó de inmediato.",
]
docs_casos = [
    Document(page_content=c, metadata={"fuente": "caso_previo", "id": f"C{i}"})
    for i, c in enumerate(casos)
]

# 3. Crear/actualizar Chroma
if CHROMA_DIR.exists():
    import shutil
    shutil.rmtree(CHROMA_DIR)

db_politicas = Chroma.from_documents(
    docs_politicas, embeddings,
    collection_name="politicas",
    persist_directory=str(CHROMA_DIR),
)
db_casos = Chroma.from_documents(
    docs_casos, embeddings,
    collection_name="casos_previos",
    persist_directory=str(CHROMA_DIR),
)
print(f"Indexados {len(docs_politicas)} fragmentos de políticas y {len(docs_casos)} casos previos.")
