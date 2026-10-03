from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

CREATE_USER_URL = "/api/users/"
MANAGE_USER_URL = "/api/users/me/"


class BaseUserApiTest(APITestCase):
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

    def authenticate_user(self):
        refresh = RefreshToken.for_user(self.user)

        self.client.credentials(HTTP_AUTHORIZE=f"Bearer {refresh.access_token}")

    def authenticate_admin(self):
        refresh = RefreshToken.for_user(self.admin)

        self.client.credentials(HTTP_AUTHORIZE=f"Bearer {refresh.access_token}")


class CreateUserViewTests(BaseUserApiTest):
    def test_anonymous_user_can_create_user(self):
        response = self.client.post(
            CREATE_USER_URL,
            {
                "email": "newuser@test.com",
                "password": "testpass123",
                "first_name": "test_first_name",
                "last_name": "test_last_name",
            },
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_authenticated_user_can_create_user(self):
        self.authenticate_user()

        response = self.client.post(
            CREATE_USER_URL,
            {
                "email": "newuser@test.com",
                "password": "testpass123",
                "first_name": "test_first_name",
                "last_name": "test_last_name",
            },
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_admin_can_create_user(self):
        self.authenticate_admin()

        response = self.client.post(
            CREATE_USER_URL,
            {
                "email": "newuser@test.com",
                "password": "testpass123",
                "first_name": "test_first_name",
                "last_name": "test_last_name",
            },
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_cannot_create_user_with_existing_email(self):
        response = self.client.post(
            CREATE_USER_URL,
            {
                "email": self.user.email,
                "password": "testpass123",
                "first_name": "test_first_name",
                "last_name": "test_last_name",
            },
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_cannot_create_user_with_invalid_email(self):
        response = self.client.post(
            CREATE_USER_URL,
            {
                "email": "invalid-email",
                "password": "testpass123",
                "first_name": "test_first_name",
                "last_name": "test_last_name",
            },
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_cannot_create_user_without_password(self):
        response = self.client.post(
            CREATE_USER_URL,
            {
                "email": "newuser@test.com",
                "first_name": "test_first_name",
                "last_name": "test_last_name",
            },
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class ManageUserViewTests(BaseUserApiTest):
    def test_anonymous_user_cannot_retrieve_profile(self):
        response = self.client.get(MANAGE_USER_URL)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated_user_can_retrieve_profile(self):
        self.authenticate_user()

        response = self.client.get(MANAGE_USER_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data["email"], self.user.email)
        self.assertEqual(
            response.data["first_name"],
            self.user.first_name,
        )
        self.assertEqual(
            response.data["last_name"],
            self.user.last_name,
        )

    def test_admin_can_retrieve_profile(self):
        self.authenticate_admin()

        response = self.client.get(MANAGE_USER_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data["email"], self.admin.email)

    def test_authenticated_user_can_update_profile(self):
        self.authenticate_user()

        response = self.client.patch(
            MANAGE_USER_URL,
            {
                "first_name": "updated_first_name",
                "last_name": "updated_last_name",
            },
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.user.refresh_from_db()

        self.assertEqual(
            self.user.first_name,
            "updated_first_name",
        )
        self.assertEqual(
            self.user.last_name,
            "updated_last_name",
        )

    def test_authenticated_user_can_update_email(self):
        self.authenticate_user()

        response = self.client.patch(
            MANAGE_USER_URL,
            {
                "email": "newemail@test.com",
            },
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.user.refresh_from_db()

        self.assertEqual(
            self.user.email,
            "newemail@test.com",
        )

    def test_authenticated_user_can_update_password(self):
        self.authenticate_user()

        response = self.client.patch(
            MANAGE_USER_URL,
            {
                "password": "newpassword123",
            },
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.user.refresh_from_db()

        self.assertTrue(self.user.check_password("newpassword123"))

        self.assertFalse(self.user.check_password("testpass123"))
