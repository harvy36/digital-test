from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from apps.users.models import Member, Loan
from apps.users.serializers import (
    MemberSerializer,
    LoanSerializer,
    LoginSerializer,
    LoanDetailsSerializer,
)
from django.utils import timezone
from django.contrib.auth import get_user_model


User = get_user_model()


def create_password(user):
    password = User.objects.make_random_password()
    print(f"Generated password for user {user.username}: {password}")
    user.set_password(password)
    user.save()
    return password


class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["user__email", "role"]
    pagination_class = PageNumberPagination
    page_size = 10

    def get_permissions(self):
        perms = super().get_permissions()
        if not self.request.user.is_staff:
            self.permission_denied(
                self.request,
                message="Debe ser usuario staff para acceder a este recurso.",
            )
        return perms

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_data = {
            "username": serializer.validated_data["email"],
            "email": serializer.validated_data["email"],
            "first_name": serializer.validated_data["name"],
            "is_staff": serializer.validated_data["role"] == "staff",
        }
        user = User(**user_data)
        password = create_password(user)
        user.set_password(password)
        user.save()
        member = serializer.save(user=user)
        member_serializer = self.get_serializer(member)
        user_data_response = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "is_staff": user.is_staff,
            "password": password,  # Include password in response for testing purposes
        }
        return Response(
            {
                "member": member_serializer.data,
                "user": user_data_response,
            },
            status=status.HTTP_201_CREATED,
        )


class LoanViewSet(viewsets.ModelViewSet):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["book__title", "member_id", "book_id"]
    pagination_class = PageNumberPagination
    page_size = 2

    def get_queryset(self):
        queryset = super().get_queryset()
        active = self.request.query_params.get("active")

        # if usuario login
        if self.request.user.is_authenticated and not self.request.user.is_staff:
            queryset = queryset.filter(member__user=self.request.user)
        if active is not None:
            if active.lower() == "true":
                queryset = queryset.filter(returned_at__isnull=True)
            elif active.lower() == "false":
                queryset = queryset.filter(returned_at__isnull=False)

        return queryset

    def get_serializer_class(self):
        if self.action in ["list", "return_loan"]:
            return LoanDetailsSerializer
        return super().get_serializer_class()

    def list(self, request, *args, **kwargs):
        page_size = (
            self.request.query_params.get("page_size", self.page_size)
            if self.request.user.is_authenticated
            else self.page_size
        )
        try:
            page_size_int = int(page_size)
        except (TypeError, ValueError):
            page_size_int = self.page_size

        self.pagination_class.page_size = page_size_int
        return super().list(request, *args, **kwargs)

    @action(detail=True, methods=["post"], url_path="return")
    def return_loan(self, request, pk=None):
        loan = self.get_object()
        if loan.returned_at is not None:
            return Response(
                {"detail": "El préstamo ya fue devuelto."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        loan.returned_at = timezone.now()
        loan.save()
        serializer = self.get_serializer(loan)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LoginView(APIView):
    def get_serializer(self, *args, **kwargs):
        return LoginSerializer(*args, **kwargs)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, _ = Token.objects.get_or_create(user=user)
        print(f"Usuario autenticado: {user.username}")
        return Response(
            {"detail": "Inicio de sesión exitoso", "token": token.key},
            status=status.HTTP_200_OK,
        )
