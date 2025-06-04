from django.urls import path
from ocr.views import ocr_extract

urlpatterns = [
    path('extract/', ocr_extract, name='ocr_extract'),
]
