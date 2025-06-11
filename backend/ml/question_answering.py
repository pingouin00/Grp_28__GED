from transformers.pipelines import pipeline  # ✅ import correct avec transformers >= 4.52

# Chargement du pipeline question-answering
qa_pipeline = pipeline("question-answering", model="deepset/roberta-base-squad2")

def answer_question(question: str, context: str) -> str:
    result = qa_pipeline(question=question, context=context)
    return result["answer"] 
