from rest_framework.decorators import api_view
from rest_framework.response import Response
from search_service.elastic_connector import get_es_client

@api_view(['GET'])
def search_documents(request):
    query = request.GET.get("q", "")
    if not query:
        return Response({"error": "query param 'q' is required"}, status=400)

    es = get_es_client()
    response = es.search(index="documents", query={
        "multi_match": {
            "query": query,
            "fields": ["title", "content", "author", "tags"]
        }
    })

    hits = response["hits"]["hits"]
    results = [{"id": hit["_id"], **hit["_source"]} for hit in hits]
    return Response(results)
