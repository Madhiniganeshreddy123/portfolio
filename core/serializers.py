from rest_framework import serializers
from .models import Project


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = [
            "id",
            "title",
            "slug",
            "category",
            "description",
            "detailed_description",
            "tech_stack",
            "github_link",
            "demo_link",
            "image",
            "is_featured",
            "order",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "slug", "created_at", "updated_at"]


class ProjectListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = [
            "id",
            "title",
            "slug",
            "category",
            "description",
            "tech_stack",
            "image",
            "is_featured",
            "order",
        ]
