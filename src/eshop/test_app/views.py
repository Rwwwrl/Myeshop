from typing import List

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Author


class AllAuthorsApiView(APIView):
    def get(self, request):
        authors = Author.objects.only('id', 'name').all()

        serialized_authors: List[dict] = []
        for author in authors:
            serialized_authors.append({
                'id': author.id,
                'name': author.name,
            })

        return Response({'authors': serialized_authors}, status=status.HTTP_200_OK)
