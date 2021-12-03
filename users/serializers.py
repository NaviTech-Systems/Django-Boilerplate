from rest_framework import serializers
from .models import User, Profile
from projects.serializers import IssueMinSerializer, ProjectSerializer
from drf_writable_nested.serializers import WritableNestedModelSerializer
from dry_rest_permissions.generics import DRYPermissionsField
from projects.models import Project, Issue
from django.db.models import Q
from django.db.models import Sum





class UserSerializer(serializers.ModelSerializer):


    class Meta:
        model = User
        ref_name = "User"
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "id",
        ]
        lookup_field = "username"
        extra_kwargs = {"url": {"lookup_field": "username"}}



class UserDetailedSerializer(
    WritableNestedModelSerializer, serializers.ModelSerializer
):

    permissions = DRYPermissionsField()

    class Meta:
        model = User
        ref_name = "User Detailed"
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",

            "id",

            "permissions",
        ]
        read_only_fields = ["id"]
        lookup_field = "username"
        extra_kwargs = {"url": {"lookup_field": "username"}}