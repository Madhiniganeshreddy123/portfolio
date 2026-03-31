from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.apps import apps
from django.conf import settings
from django.contrib.auth import get_user_model

from .models import CustomUser

Message = apps.get_model("core", "Message")
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
        "total_messages": Message.objects.count(),
        "unread_messages": Message.objects.filter(is_read=False).count(),
        "total_skills": apps.get_model("core", "Skill").objects.count(),
        "recent_messages": Message.objects.order_by("-created_at")[:5],
    }
    return render(request, "accounts/dashboard.html", context)
