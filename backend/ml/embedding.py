import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from typing import List

# Initialisation du modèle et de l'index FAISS
model = SentenceTransformer("all-MiniLM-L6-v2")
index = faiss.IndexFlatL2(384)  # 384 est la taille de l'embedding MiniLM

# Données d'exemple
documents: List[str] = [
    "Le projet Diwan permet de classer automatiquement les fichiers.",
    "L’utilisateur peut poser une question et obtenir une réponse par l’IA.",
    "L’application utilise FAISS et SentenceTransformer."
]

# Embedding des documents
doc_embeddings = model.encode(documents)
doc_embeddings = np.array(doc_embeddings).astype("float32")

# Ajout à l'index
index.add(doc_embeddings)

# Fonction pour retrouver les documents similaires
def find_similar_context(question: str, top_k: int = 1) -> List[str]:
    """
    Reçoit une question et retourne les contextes les plus proches.
    """
    question_vec = model.encode([question])
    question_vec = np.array(question_vec).astype("float32")
    distances, indices = index.search(question_vec, top_k)
    return [documents[i] for i in indices[0]]