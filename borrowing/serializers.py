from django.db import transaction
from rest_framework import serializers

from book.serializers import BookListSerializer
from borrowing.models import Borrowing
from notifications.helper import send_message
from user.serializers import UserSerializer


class EmptySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ()
        model = Borrowing


class BorrowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = [
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book",
            "user",
        ]


class BorrowingListSerializer(BorrowingSerializer):
    book = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()

    class Meta:
        model = Borrowing
        fields = [
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book",
            "user",
        ]

    def get_user(self, obj):
        return obj.user.email

    def get_book(self, obj):
        return {
            "title": obj.book.title,
            "author": obj.book.author.full_name,
            "daily_fee": obj.book.daily_fee,
        }


class BorrowingDetailSerializer(serializers.ModelSerializer):
    book = BookListSerializer()
    user = UserSerializer()

    class Meta:
        model = Borrowing
        fields = [
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book",
            "user",
        ]


class BorrowingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = [
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book",
        ]

    def validate_book(self, book):
        if book.inventory == 0:
            raise serializers.ValidationError("This book is currently unavailable.")

        return book

    @transaction.atomic
    def create(self, validated_data):
        user = self.context["request"].user
        book = validated_data["book"]

        book.inventory -= 1
        book.save(update_fields=("inventory",))

        message = f'Book "{book.title}" has been borrowed by {user.email}'
        send_message(message)

        return Borrowing.objects.create(
            user=user,
            **validated_data,
        )
