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


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ["title", "is_featured", "order", "created_at"]
    list_editable = ["is_featured", "order"]
    list_filter = ["is_featured"]
    search_fields = ["title", "tech_stack"]


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ["title", "company", "start_date", "is_current", "order"]
    list_editable = ["is_current", "order"]
    list_filter = ["is_current"]


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ["degree", "institution", "start_year", "end_year", "order"]
    list_editable = ["order"]


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ["name", "subject", "email", "is_read", "created_at"]
    list_editable = ["is_read"]
    list_filter = ["is_read"]
    search_fields = ["name", "email", "subject", "message"]
    readonly_fields = ["created_at"]
