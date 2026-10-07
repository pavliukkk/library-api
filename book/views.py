from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser

from book.models import Book, Author
from book.permissions import IsAdminOrReadOnly
from book.serializers import (
    BookSerializer,
    AuthorSerializer,
    BookListSerializer,
)


@extend_schema_view(
    list=extend_schema(
        summary="List books",
        description="Returns a list of all books.",
        responses=BookListSerializer(many=True),
    ),
    retrieve=extend_schema(
        summary="Retrieve a book",
        description="Returns detailed information about a book.",
        responses=BookSerializer,
    ),
    create=extend_schema(
        summary="Create a book",
        description="Creates a new book. Available only to administrators.",
        request=BookSerializer,
        responses=BookSerializer,
    ),
    update=extend_schema(
        summary="Update a book",
        description="Updates an existing book. Available only to administrators.",
        request=BookSerializer,
        responses=BookSerializer,
    ),
    partial_update=extend_schema(
        summary="Partially update a book",
        description="Partially updates an existing book. Available only to administrators.",
        request=BookSerializer,
        responses=BookSerializer,
    ),
    destroy=extend_schema(
        summary="Delete a book",
        description="Deletes an existing book. Available only to administrators.",
    ),
)
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.select_related()
    serializer_class = BookSerializer
    permission_classes = [
        IsAdminOrReadOnly,
    ]

    def get_serializer_class(self):
        if self.action == "list":
            return BookListSerializer
        return BookSerializer


@extend_schema_view(
    list=extend_schema(
        summary="List authors",
        description="Returns a list of all authors. Available only to administrators.",
        responses=AuthorSerializer(many=True),
    ),
    retrieve=extend_schema(
        summary="Retrieve an author",
        description="Returns detailed information about an author.",
        responses=AuthorSerializer,
    ),
    create=extend_schema(
        summary="Create an author",
        description="Creates a new author. Available only to administrators.",
        request=AuthorSerializer,
        responses=AuthorSerializer,
    ),
    update=extend_schema(
        summary="Update an author",
        description="Updates an existing author. Available only to administrators.",
        request=AuthorSerializer,
        responses=AuthorSerializer,
    ),
    partial_update=extend_schema(
        summary="Partially update an author",
        description="Partially updates an existing author. Available only to administrators.",
        request=AuthorSerializer,
        responses=AuthorSerializer,
    ),
    destroy=extend_schema(
        summary="Delete an author",
        description="Deletes an existing author. Available only to administrators.",
    ),
)
class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAdminUser]
