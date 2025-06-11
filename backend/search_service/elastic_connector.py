from elasticsearch import Elasticsearch
import os

def get_es_client():
    return Elasticsearch([os.getenv("ELASTIC_URL", "http://localhost:9200")])
