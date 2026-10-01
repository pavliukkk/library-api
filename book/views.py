from rest_framework import viewsets, permissions

from book.models import Book, Author
from book.serializers import BookSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAdminUser]
