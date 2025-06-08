from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from ml.db_loader import load_documents_from_db

# Charger le modèle léger d'embedding
model = SentenceTransformer("all-MiniLM-L6-v2")

# Charger les documents depuis MongoDB
documents = load_documents_from_db()

if not documents:
    raise ValueError("Aucun document trouvé dans la base de données MongoDB.")

# Encoder les documents en vecteurs
doc_embeddings = np.array(model.encode(documents))

# Construire l'index FAISS
index = faiss.IndexFlatL2(doc_embeddings.shape[1])
index.add(doc_embeddings)

def find_relevant_context(question: str, top_k=1):
    """
    Retourne les documents les plus similaires à la question.
    """
    question_vec = np.array(model.encode([question]))
    D, I = index.search(question_vec, top_k)
    return [documents[i] for i in I[0]]
