from django.conf.urls import url
from django.urls import include, path
from .views import UserListView, UserView

urlpatterns = [
    path(
        "<slug:username>",
        UserView.as_view(),
        name="profile",
    ),
    url(
        r"^$",
        UserListView.as_view(),
        name="list",
    ),
]
