import datetime
from datetime import timezone

from django.db import transaction
from django.shortcuts import redirect
from rest_framework import viewsets, mixins, serializers, status, renderers
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from borrowing.models import Borrowing
from borrowing.serializers import (
    BorrowingSerializer,
    BorrowingListSerializer,
    BorrowingDetailSerializer,
    BorrowingCreateSerializer,
    EmptySerializer,
)

class BorrowingViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
):
    queryset = Borrowing.objects.select_related()
    serializer_class = BorrowingSerializer
    permission_classes = [IsAuthenticated]

    @action(
        detail=True,
        methods=["post"],
        url_path="return",
    )
    def return_borrowing(self, request, pk=None):
        borrowing = self.get_object()


        if borrowing.actual_return_date is not None:
            raise serializers.ValidationError(
                {"actual_return_date": "Borrowing is already returned."}
            )

        with transaction.atomic():
            borrowing.actual_return_date = datetime.date.today()
            borrowing.save(update_fields=["actual_return_date"])

            borrowing.book.inventory += 1
            borrowing.book.save(update_fields=["inventory"])

        return redirect("borrowing:borrowing-list")

    def get_serializer_class(self):
        if self.action == "list":
            return BorrowingListSerializer
        elif self.action == "retrieve":
            return BorrowingDetailSerializer
        elif self.action == "create":
            return BorrowingCreateSerializer
        elif self.action == "return_borrowing":
            return EmptySerializer
        return BorrowingSerializer
