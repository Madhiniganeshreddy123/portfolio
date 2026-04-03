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
