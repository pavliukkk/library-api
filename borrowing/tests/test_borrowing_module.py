import datetime

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from book.models import Author, Book
from borrowing.models import Borrowing

User = get_user_model()

BORROWING_URL = "/api/borrowings/borrowings/"


def detail_url(url, obj_id):
    return f"{url}{obj_id}/"


class BaseViewSetTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="user@test.com",
            password="testpass123",
            first_name="test_first_name",
            last_name="test_last_name",
        )

        self.admin = User.objects.create_superuser(
            email="admin@test.com",
            password="testpass123",
            first_name="admin_first_name",
            last_name="admin_last_name",
        )

        self.author = Author.objects.create(
            first_name="test_first_name",
            last_name="test_last_name",
        )

        self.book = Book.objects.create(
            title="test_title",
            author=self.author,
            cover="HARD",
            inventory=5,
            daily_fee=2.00,
        )

        self.borrowing = Borrowing.objects.create(
            borrow_date=datetime.date.today(),
            expected_return_date=datetime.date.today() + datetime.timedelta(days=1),
            actual_return_date=None,
            user=self.user,
            book=self.book,
        )

    def authenticate_user(self):
        refresh = RefreshToken.for_user(self.user)

        self.client.credentials(HTTP_AUTHORIZE=f"Bearer {refresh.access_token}")

    def authenticate_admin(self):
        refresh = RefreshToken.for_user(self.admin)

        self.client.credentials(HTTP_AUTHORIZE=f"Bearer {refresh.access_token}")


class BorrowingViewSetTests(BaseViewSetTest):
    def test_anonymous_user_can_list_borrowings(self):
        response = self.client.get(BORROWING_URL)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_anonymous_user_can_retrieve_borrowings(self):
        response = self.client.get(detail_url(BORROWING_URL, self.borrowing.id))

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_anonymous_user_cannot_create_borrowings(self):
        response = self.client.post(
            BORROWING_URL,
            {
                "borrow_date": datetime.date.today(),
                "expected_return_date": datetime.date.today()
                + datetime.timedelta(days=1),
                "book": self.book,
            },
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated_user_can_list_borrowings(self):
        self.authenticate_user()

        response = self.client.get(BORROWING_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_authenticated_user_can_retrieve_borrowings(self):
        self.authenticate_user()

        response = self.client.get(detail_url(BORROWING_URL, self.borrowing.id))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_authenticated_user_can_create_borrowings(self):
        self.authenticate_user()

        response = self.client.post(
            BORROWING_URL,
            {
                "borrow_date": datetime.date.today(),
                "expected_return_date": datetime.date.today()
                + datetime.timedelta(days=1),
                "book": self.book.id,
            },
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_admin_can_list_borrowings(self):
        self.authenticate_admin()

        response = self.client.get(BORROWING_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_user_can_retrieve_borrowings(self):
        self.authenticate_admin()

        response = self.client.get(detail_url(BORROWING_URL, self.borrowing.id))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_user_can_create_borrowings(self):
        self.authenticate_admin()

        response = self.client.post(
            BORROWING_URL,
            {
                "borrow_date": datetime.date.today(),
                "expected_return_date": datetime.date.today()
                + datetime.timedelta(days=1),
                "book": self.book.id,
            },
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
