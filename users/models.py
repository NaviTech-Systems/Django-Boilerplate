from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    UserManager,
)
from django.db.models.functions import TruncDay
from django.db.models.aggregates import Count
from django_prometheus.models import ExportModelOperationsMixin


class User(ExportModelOperationsMixin("user"), AbstractBaseUser):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(
        max_length=255, unique=True, blank=False, null=False
    )
    username = models.CharField(
        max_length=255, unique=True, blank=False, null=False
    )
    first_name = models.CharField(max_length=255, unique=False)
    last_name = models.CharField(max_length=255, unique=False)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "username"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["email"]
    objects = UserManager()

    def __str__(self):
        return self.username

    def current_user(self):
        return {
            "username": self.username,
            "email": self.email,
            "id": self.id,
        }

    @property
    def staff(self):
        return self.is_staff

    @property
    def superuser(self):
        return self.is_superuser

    @property
    def active(self):
        return self.is_active

    @property
    def full_name(self):
        return self.first_name + " " + self.last_name

    @property
    def get_email(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def get_full_name(self):
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        return self.first_name


    def has_object_read_permission(self, request):
        return True

    def has_object_write_permission(self, request):
        return request.user.id == self.id

    @staticmethod
    def has_read_permission(request):
        return True

    @staticmethod
    def has_write_permission(request):
        return True

    @staticmethod
    def has_create_permission(request):
        return True

    class Meta:
        indexes = [
            models.Index(fields=["username"]),
            models.Index(fields=["id"]),
        ]

