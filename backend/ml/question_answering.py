from rest_framework.decorators import api_view
from rest_framework.response import Response
from transformers.pipelines import pipeline

qa_pipeline = pipeline("question-answering", model="deepset/roberta-base-squad2")

@api_view(["POST"])
def ask_question(request):
    data = request.data
    question = data.get("question", "")
    context = data.get("context", "")

    if not question or not context:
        return Response({"error": "question et contexte requis"}, status=400)

    result = qa_pipeline({"question": question, "context": context})
    return Response({"answer": result["answer"]})