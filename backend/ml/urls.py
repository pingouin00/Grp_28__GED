from django.urls import path
from ml.question_answering import ask_question

urlpatterns = [
    path("ask/", ask_question, name="ask-question"),
]