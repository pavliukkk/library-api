from drf_spectacular.utils import extend_schema
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from user.serializers import UserSerializer


@extend_schema(
    summary="Register a user",
    description="Creates a new user account.",
    request=UserSerializer,
    responses=UserSerializer,
)
class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = ()


@extend_schema(
    summary="Manage user profile",
    description=(
        "Returns or updates the profile of the currently authenticated user."
    ),
    responses=UserSerializer,
)
class ManageUserView(
    generics.RetrieveUpdateAPIView,
):
    serializer_class = UserSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user