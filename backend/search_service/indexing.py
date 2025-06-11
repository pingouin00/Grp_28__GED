from search_service.elastic_connector import get_es_client

INDEX_NAME = "ged_documents"

def create_index():
    es = get_es_client()
    if not es.indices.exists(index=INDEX_NAME):
        es.indices.create(index=INDEX_NAME)

def index_document(doc_id, content, metadata, doc_type="inconnu"):
    """
    Indexe un document OCR dans Elasticsearch avec métadonnées enrichies.
    """
    es = get_es_client()
    create_index()  # S'assure que l'index existe

    body = {
        "content": content,
        "title": metadata.get("title", ""),
        "author": metadata.get("author", ""),
        "tags": metadata.get("tags", []),
        "upload_date": metadata.get("date", ""),  # "date" ou autre champ selon ton extracteur
        "type": doc_type
    }

    es.index(index=INDEX_NAME, id=doc_id, body=body)
