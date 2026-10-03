from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser

from book.models import Book, Author
from book.serializers import BookSerializer, AuthorSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = []


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAdminUser]
