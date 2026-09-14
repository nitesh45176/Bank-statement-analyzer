from langchain_community.vectorstores import FAISS
import urllib.request
import os

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434")

_embeddings = None
_vector_stores = {}


def _get_embeddings():
    global _embeddings
    if _embeddings is None:
        try:
            from langchain_ollama import OllamaEmbeddings
            _embeddings = OllamaEmbeddings(
                model="nomic-embed-text",
                base_url=OLLAMA_BASE_URL,
            )
        except Exception as e:
            print(f"[vector_store] Could not initialize OllamaEmbeddings: {e}")
            _embeddings = None
    return _embeddings


def _is_ollama_reachable():
    try:
        req = urllib.request.Request(
            f"{OLLAMA_BASE_URL}/api/tags",
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req, timeout=1.5) as resp:
            return resp.status == 200
    except Exception:
        return False


def create_statement_index(
    statement_id: str,
    documents: list[str],
):
    if not documents:
        return

    if not _is_ollama_reachable():
        print(f"[vector_store] Ollama not reachable at {OLLAMA_BASE_URL}. Skipping embedding creation (fallback search will be used).")
        return

    embedder = _get_embeddings()
    if embedder is None:
        return

    try:
        batch_size = 20
        vector_store = None
        total = len(documents)

        for i in range(0, total, batch_size):
            batch = documents[i:i + batch_size]
            print(
                f"[vector_store] Embedding transactions "
                f"{i + 1}-{min(i + batch_size, total)} / {total}"
            )

            batch_store = FAISS.from_texts(
                batch,
                embedder,
            )

            if vector_store is None:
                vector_store = batch_store
            else:
                vector_store.merge_from(batch_store)

        _vector_stores[statement_id] = vector_store
        print(f"[vector_store] RAG index created for {statement_id} with {total} documents.")
    except Exception as e:
        print(f"[vector_store] Warning: Error indexing statement {statement_id}: {e}")


def search_statement(
    statement_id: str,
    query: str,
    k: int = 5,
) -> list[str]:
    vector_store = _vector_stores.get(statement_id)

    if not vector_store:
        return []

    try:
        documents = vector_store.similarity_search(
            query,
            k=k,
        )

        return [
            document.page_content
            for document in documents
        ]
    except Exception as e:
        print(f"[vector_store] Warning: similarity search failed: {e}")
        return []