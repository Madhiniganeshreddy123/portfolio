from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Profile,
    SkillCategory,
    Skill,
    Project,
    Experience,
    Education,
    Message,
)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ["name", "email", "created_at"]
    fields = [
        "name",
        "title",
        "tagline",
        "about",
        "profile_image",
        "resume",
        "email",
        "linkedin",
        "github",
    ]


class SkillInline(admin.TabularInline):
    model = Skill
    extra = 1


@admin.register(SkillCategory)
class SkillCategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "order"]
    list_editable = ["order"]
    inlines = [SkillInline]


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ["name", "category", "proficiency", "order"]
    list_filter = ["category"]
    list_editable = ["proficiency", "order"]
    search_fields = ["name"]


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ["title", "image_thumbnail", "is_featured", "order", "created_at"]
    list_editable = ["is_featured", "order"]
    list_filter = ["is_featured"]
    search_fields = ["title", "tech_stack", "description"]
    readonly_fields = ["created_at", "updated_at", "slug"]
    ordering = ["order", "-created_at"]

    fieldsets = (
        (
            "Basic Information",
            {"fields": ("title", "slug", "description", "tech_stack")},
        ),
        ("Links", {"fields": ("github_link", "demo_link")}),
        ("Media", {"fields": ("image",)}),
        ("Display Options", {"fields": ("is_featured", "order")}),
        (
            "Timestamps",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )

    def image_thumbnail(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 4px;">',
                obj.image.url,
            )
        return format_html(
            '<div style="width: 50px; height: 50px; background: #ddd; border-radius: 4px; display: flex; align-items: center; justify-content: center;"><i class="fas fa-image"></i></div>'
        )

    image_thumbnail.short_description = "Image"


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ["title", "company", "start_date", "is_current", "order"]
    list_editable = ["is_current", "order"]
    list_filter = ["is_current"]
    search_fields = ["title", "company", "description"]


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ["degree", "institution", "start_year", "end_year", "order"]
    list_editable = ["order"]
    search_fields = ["degree", "institution"]


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ["name", "subject", "email", "is_read", "created_at"]
    list_editable = ["is_read"]
    list_filter = ["is_read"]
    search_fields = ["name", "email", "subject", "message"]
    readonly_fields = ["created_at"]
    date_hierarchy = "created_at"
