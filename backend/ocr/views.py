from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework import status
import os

from ocr.ocr_service import extract_text_from_image, extract_text_from_pdf
from ocr.utils import clean_ocr_text, extract_metadata, guess_document_type

UPLOAD_DIR = "uploads"

@api_view(['POST'])
@parser_classes([MultiPartParser])
def ocr_extract(request):
    if 'file' not in request.FILES:
        return Response({'error': 'Fichier requis.'}, status=status.HTTP_400_BAD_REQUEST)

    file = request.FILES['file']
    file_type = file.content_type

    os.makedirs(UPLOAD_DIR, exist_ok=True)
    file_path = os.path.join(UPLOAD_DIR, file.name)
    with open(file_path, 'wb+') as f:
        for chunk in file.chunks():
            f.write(chunk)

    try:
        if file_type in ['image/jpeg', 'image/png']:
            text = extract_text_from_image(file_path)
        elif file_type == 'application/pdf':
            text = extract_text_from_pdf(file_path)
        else:
            return Response({'error': 'Type non supporté.'}, status=415)

        cleaned = clean_ocr_text(text)
        metadata = extract_metadata(cleaned)
        doc_type = guess_document_type(cleaned)

        return Response({
            "text": cleaned,
            "metadata": metadata,
            "type": doc_type
        }, status=200)

    except Exception as e:
        return Response({'error': str(e)}, status=500)

    finally:
        if os.path.exists(file_path):
            os.remove(file_path)
