from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.apps import apps
from django.conf import settings
from django.contrib.auth import get_user_model
from django.http import JsonResponse

from .models import CustomUser

ContactMessage = apps.get_model("core", "Message")
Project = apps.get_model("core", "Project")


def register_view(request):
    if settings.DEBUG:
        if request.method == "POST":
            username = request.POST.get("username")
            email = request.POST.get("email")
            password = request.POST.get("password")
            confirm_password = request.POST.get("confirm_password")

            if password != confirm_password:
                messages.error(request, "Passwords do not match")
                return render(request, "accounts/register.html")

            if CustomUser.objects.filter(username=username).exists():
                messages.error(request, "Username already exists")
                return render(request, "accounts/register.html")

            user = CustomUser.objects.create_user(
                username=username,
                email=email,
                password=password,
                is_staff=True,
                is_superuser=True,
            )
            messages.success(request, "Superuser created successfully! Please login.")
            return redirect("login")
        return render(request, "accounts/register.html")
    else:
        messages.error(request, "Registration is disabled in production")
        return redirect("login")


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("dashboard")
        else:
            messages.error(request, "Invalid credentials")
    return render(request, "accounts/login.html", {"debug": settings.DEBUG})


def logout_view(request):
    logout(request)
    return redirect("login")


@login_required
def dashboard(request):
    context = {
        "total_projects": Project.objects.count(),
        "total_messages": ContactMessage.objects.count(),
        "unread_messages": ContactMessage.objects.filter(is_read=False).count(),
        "total_skills": apps.get_model("core", "Skill").objects.count(),
        "recent_messages": ContactMessage.objects.order_by("-created_at")[:5],
    }
    return render(request, "accounts/dashboard.html", context)


@login_required
def mark_message_read(request, message_id):
    message = get_object_or_404(ContactMessage, id=message_id)
    message.is_read = True
    message.save()
    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return JsonResponse({"status": "success"})
    return redirect("dashboard")


@login_required
def projects_dashboard(request):
    if request.method == "POST":
        Project.objects.create(
            title=request.POST.get("title"),
            category=request.POST.get("category"),
            description=request.POST.get("description"),
            detailed_description=request.POST.get("detailed_description", ""),
            tech_stack=request.POST.get("tech_stack", ""),
            github_link=request.POST.get("github_link", ""),
            demo_link=request.POST.get("demo_link", ""),
            order=request.POST.get("order", 0),
        )
        messages.success(request, "Project created successfully!")
        return redirect("projects_dashboard")

    projects = Project.objects.all().order_by("order")
    for project in projects:
        project.tech_stack_list = [
            t.strip() for t in project.tech_stack.split(",") if t.strip()
        ]
    total_analysis = Project.objects.filter(category="analysis").count()
    total_development = Project.objects.filter(category="development").count()

    context = {
        "projects": projects,
        "total_analysis": total_analysis,
        "total_development": total_development,
    }
    return render(request, "accounts/projects_dashboard.html", context)


@login_required
def edit_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    if request.method == "POST":
        project.title = request.POST.get("title")
        project.category = request.POST.get("category")
        project.description = request.POST.get("description")
        project.detailed_description = request.POST.get("detailed_description", "")
        project.tech_stack = request.POST.get("tech_stack", "")
        project.github_link = request.POST.get("github_link", "")
        project.demo_link = request.POST.get("demo_link", "")
        project.order = request.POST.get("order", 0)
        project.is_featured = request.POST.get("is_featured") == "on"
        project.save()
        messages.success(request, "Project updated successfully!")
        return redirect("projects_dashboard")

    return render(request, "accounts/edit_project.html", {"project": project})


@login_required
def delete_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    project.delete()
    messages.success(request, "Project deleted successfully!")
    return redirect("projects_dashboard")
