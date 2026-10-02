from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from book.models import Author, Book

User = get_user_model()

AUTHOR_URL = "/api/library/authors/"
BOOK_URL = "/api/library/books/"


def detail_url(url, obj_id):
    return f"{url}{obj_id}/"


class BaseViewSetTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="user@test.com",
            password="testpass123",
        )

        self.admin = User.objects.create_superuser(
            email="admin@test.com",
            password="testpass123",
        )

        self.author = Author.objects.create(
            first_name="test_first_name",
            last_name="test_last_name",
        )

    def authenticate_user(self):
        self.client.force_authenticate(user=self.user)

    def authenticate_admin(self):
        self.client.force_authenticate(user=self.admin)


class AuthorViewSetTests(BaseViewSetTest):
    def test_anonymous_user_cannot_list_authors(self):
        response = self.client.get(AUTHOR_URL)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_anonymous_user_cannot_create_author(self):
        response = self.client.post(
            AUTHOR_URL,
            {
                "first_name": "test_first_name",
                "last_name": "test_last_name",
            },
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_anonymous_user_cannot_update_author(self):
        response = self.client.put(
            detail_url(AUTHOR_URL, self.author.id),
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_anonymous_user_cannot_delete_author(self):
        response = self.client.delete(
            detail_url(AUTHOR_URL, self.author.id),
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authenticated_user_cannot_list_authors(self):
        self.authenticate_user()

        response = self.client.get(AUTHOR_URL)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authenticated_user_cannot_create_author(self):
        self.authenticate_user()

        response = self.client.post(
            AUTHOR_URL,
            {
                "first_name": "test_first_name",
                "last_name": "test_last_name",
            },
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authenticated_user_cannot_update_author(self):
        self.authenticate_user()

        response = self.client.put(
            detail_url(AUTHOR_URL, self.author.id),
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authenticated_user_cannot_delete_author(self):
        self.authenticate_user()

        response = self.client.delete(
            detail_url(AUTHOR_URL, self.author.id),
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_list_authors(self):
        self.authenticate_admin()

        response = self.client.get(AUTHOR_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_can_create_author(self):
        self.authenticate_admin()

        response = self.client.post(
            AUTHOR_URL,
            {
                "first_name": "test_first_name",
                "last_name": "test_last_name",
            },
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_admin_can_update_author(self):
        self.authenticate_admin()

        response = self.client.put(
            detail_url(AUTHOR_URL, self.author.id),
            {
                "first_name": "test_first_name_2",
                "last_name": "test_last_name_2",
            },
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_can_delete_author(self):
        self.authenticate_admin()

        response = self.client.delete(
            detail_url(AUTHOR_URL, self.author.id),
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class BookViewSetTests(BaseViewSetTest):
    def setUp(self):
        super().setUp()

        self.book = Book.objects.create(
            title="test_title",
            author=self.author,
            cover="HARD",
            inventory=5,
            daily_fee=2.00,
        )

    def test_anonymous_user_can_list_books(self):
        response = self.client.get(BOOK_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_anonymous_user_can_retrieve_book(self):
        response = self.client.get(
            detail_url(BOOK_URL, self.book.id)
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_authenticated_user_can_list_books(self):
        self.authenticate_user()

        response = self.client.get(BOOK_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_authenticated_user_can_retrieve_book(self):
        self.authenticate_user()

        response = self.client.get(
            detail_url(BOOK_URL, self.book.id)
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)