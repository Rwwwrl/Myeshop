from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Author


class AllAuthorsApiView(APIView):
    def get(self, request):
        author_names = list(Author.objects.values_list('name', flat=True).all())
        return Response({'author_names': author_names}, status=status.HTTP_200_OK)
