from rest_framework.generics import (
    ListAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from .serializers import (
    UserSerializer,
    UserDetailedSerializer,
)
from dry_rest_permissions.generics import DRYPermissions
from .models import User


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 1000


class UserListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    pagination_class = StandardResultsSetPagination
    queryset = User.objects.all()


class UserView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, DRYPermissions]
    serializer_class = UserDetailedSerializer
    queryset = User.objects.all()
    lookup_field = "username"
    lookup_url_kwarg = "username"
