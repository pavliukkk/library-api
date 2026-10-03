from rest_framework import serializers

from book.models import Book, Author


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ["first_name", "last_name"]


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ["id", "title", "author", "cover", "inventory", "daily_fee"]


class BookListSerializer(BookSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field="full_name",
    )

    class Meta:
        model = Book
        fields = ["id", "title", "author", "cover", "inventory", "daily_fee"]
