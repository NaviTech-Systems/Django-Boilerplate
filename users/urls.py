from django.conf.urls import url
from django.urls import include, path
from .views import UpdateAvatarView, UserListView, UserView

urlpatterns = [
    path(
        "<slug:username>",
        UserView.as_view(),
        name="profile",
    ),
    url(
        r"^(?P<user_id>\d+)/avatar",
        UpdateAvatarView.as_view(),
        name="profile",
    ),
    url(
        r"^$",
        UserListView.as_view(),
        name="list",
    ),
]
