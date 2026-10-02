from django.urls import path, include
from rest_framework import routers

from book.views import BookViewSet, AuthorViewSet

app_name = "book"

router = routers.DefaultRouter()
router.register("books", BookViewSet)
router.register("authors", AuthorViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
