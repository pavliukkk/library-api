import datetime

from django.db import transaction
from django.shortcuts import redirect
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets, mixins, serializers
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from borrowing.models import Borrowing
from borrowing.serializers import (
    BorrowingSerializer,
    BorrowingListSerializer,
    BorrowingDetailSerializer,
    BorrowingCreateSerializer,
    EmptySerializer,
)


@extend_schema_view(
    list=extend_schema(
        summary="List borrowings",
        description="Returns a list of borrowings belonging to the authenticated user.",
        responses=BorrowingListSerializer(many=True),
    ),
    retrieve=extend_schema(
        summary="Retrieve a borrowing",
        description="Returns detailed information about a borrowing.",
        responses=BorrowingDetailSerializer,
    ),
    create=extend_schema(
        summary="Create a borrowing",
        description=(
            "Creates a new borrowing for the authenticated user. "
            "The book inventory is decreased by one."
        ),
        request=BorrowingCreateSerializer,
        responses=BorrowingCreateSerializer,
    ),
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

    @extend_schema(
        summary="Return a borrowing",
        description=(
            "Returns a borrowed book. "
            "The book inventory is increased by one. "
            "A borrowing cannot be returned more than once."
        ),
        request=EmptySerializer,
        responses=BorrowingDetailSerializer,
    )
    @action(
        detail=True,
        methods=["post"],
        url_path="return",
    )
    def return_borrowing(self, request, pk=None):
        borrowing = self.get_object()

        if borrowing.actual_return_date is not None:
            raise serializers.ValidationError(
                {
                    "actual_return_date": (
                        "Borrowing is already returned."
                    )
                }
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
