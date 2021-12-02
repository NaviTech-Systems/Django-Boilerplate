from rest_framework import serializers
from .models import User, Profile
from projects.serializers import IssueMinSerializer, ProjectSerializer
from drf_writable_nested.serializers import WritableNestedModelSerializer
from dry_rest_permissions.generics import DRYPermissionsField
from projects.models import Project, Issue
from django.db.models import Q
from django.db.models import Sum


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["avatar", "company", "department", "job"]
        lookup_field = "user_id"


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(many=False)

    class Meta:
        model = User
        ref_name = "User"
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "profile",
            "id",
        ]
        lookup_field = "username"
        extra_kwargs = {"url": {"lookup_field": "username"}}


class ActivitySerializer(serializers.ModelSerializer):
    value = serializers.SerializerMethodField()
    date = serializers.SerializerMethodField()

    class Meta:
        model = Issue
        fields = ["value", "date"]

    def get_value(self, obj):
        return obj["value"]

    def get_date(self, obj):
        return obj["date"].strftime("%m-%d-%Y")


class ProjectsDataSerializer(serializers.Serializer):
    projects_count = serializers.SerializerMethodField()
    active_issues = serializers.SerializerMethodField()
    asigned_issues = ActivitySerializer(
        source="get_asigned_issues_chart", many=True
    )
    reported_issues = ActivitySerializer(
        source="get_reported_issues_chart", many=True
    )
    part_projects = ProjectSerializer(many=True, read_only=True)
    last_issues = IssueMinSerializer(
        source="get_last_issues", many=True, read_only=True
    )

    class Meta:
        fields = [
            "projects_count",
            "asigned_issues",
            "activity",
            "reported_issues",
            "part_projects",
            "last_issues",
        ]
        ref_name = "User Data"

    def get_projects_count(self, obj):
        user = self.context["request"].user
        return Project.objects.filter(members=user).count()

    def get_active_issues(self, obj):
        user = self.context["request"].user
        return Issue.objects.filter(Q(reporter=user, asignee=user)).count()


class UserDetailedSerializer(
    WritableNestedModelSerializer, serializers.ModelSerializer
):
    profile = ProfileSerializer(many=False)
    data = ProjectsDataSerializer(source="*", read_only=True, required=False)
    permissions = DRYPermissionsField()

    class Meta:
        model = User
        ref_name = "User Detailed"
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "profile",
            "id",
            "data",
            "permissions",
        ]
        read_only_fields = ["id", "data"]
        lookup_field = "username"
        extra_kwargs = {"url": {"lookup_field": "username"}}