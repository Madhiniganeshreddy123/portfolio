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
Profile = apps.get_model("core", "Profile")
SkillCategory = apps.get_model("core", "SkillCategory")
Skill = apps.get_model("core", "Skill")
Experience = apps.get_model("core", "Experience")
Education = apps.get_model("core", "Education")


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


# Skills Dashboard
@login_required
def skills_dashboard(request):
    categories = (
        SkillCategory.objects.prefetch_related("skills").all().order_by("order")
    )
    total_skills = Skill.objects.count()

    context = {
        "categories": categories,
        "total_skills": total_skills,
    }
    return render(request, "accounts/skills_dashboard.html", context)


@login_required
def add_skill_category(request):
    if request.method == "POST":
        name = request.POST.get("name")
        order = request.POST.get("order", 0)
        SkillCategory.objects.create(name=name, order=order)
        messages.success(request, "Category created successfully!")
    return redirect("skills_dashboard")


@login_required
def add_skill(request):
    if request.method == "POST":
        name = request.POST.get("name")
        category_id = request.POST.get("category")
        proficiency = request.POST.get("proficiency", 50)
        icon = request.POST.get("icon", "")
        order = request.POST.get("order", 0)

        category = get_object_or_404(SkillCategory, id=category_id)
        Skill.objects.create(
            name=name,
            category=category,
            proficiency=proficiency,
            icon=icon,
            order=order,
        )
        messages.success(request, "Skill created successfully!")
    return redirect("skills_dashboard")


@login_required
def delete_skill(request, skill_id):
    skill = get_object_or_404(Skill, id=skill_id)
    skill.delete()
    messages.success(request, "Skill deleted successfully!")
    return redirect("skills_dashboard")


@login_required
def delete_skill_category(request, category_id):
    category = get_object_or_404(SkillCategory, id=category_id)
    category.delete()
    messages.success(request, "Category deleted successfully!")
    return redirect("skills_dashboard")


# Profile Dashboard
@login_required
def profile_dashboard(request):
    profile = Profile.objects.first()

    if request.method == "POST":
        if profile:
            profile.name = request.POST.get("name", "")
            profile.title = request.POST.get("title", "")
            profile.tagline = request.POST.get("tagline", "")
            profile.about = request.POST.get("about", "")
            profile.profile_image = request.POST.get("profile_image", "")
            profile.email = request.POST.get("email", "")
            profile.linkedin = request.POST.get("linkedin", "")
            profile.github = request.POST.get("github", "")
            profile.save()
        else:
            Profile.objects.create(
                name=request.POST.get("name", ""),
                title=request.POST.get("title", ""),
                tagline=request.POST.get("tagline", ""),
                about=request.POST.get("about", ""),
                profile_image=request.POST.get("profile_image", ""),
                email=request.POST.get("email", ""),
                linkedin=request.POST.get("linkedin", ""),
                github=request.POST.get("github", ""),
            )
        messages.success(request, "Profile updated successfully!")
        return redirect("profile_dashboard")

    context = {"profile": profile}
    return render(request, "accounts/profile_dashboard.html", context)


# Messages Dashboard
@login_required
def messages_dashboard(request):
    all_messages = ContactMessage.objects.all().order_by("-created_at")
    unread_count = ContactMessage.objects.filter(is_read=False).count()

    context = {
        "messages": all_messages,
        "unread_count": unread_count,
    }
    return render(request, "accounts/messages_dashboard.html", context)


@login_required
def toggle_message_read(request, message_id):
    message = get_object_or_404(ContactMessage, id=message_id)
    message.is_read = not message.is_read
    message.save()
    return redirect("messages_dashboard")


@login_required
def delete_message(request, message_id):
    message = get_object_or_404(ContactMessage, id=message_id)
    message.delete()
    messages.success(request, "Message deleted successfully!")
    return redirect("messages_dashboard")


# Experience Dashboard
@login_required
def experience_dashboard(request):
    experiences = Experience.objects.all().order_by("-start_date")

    context = {
        "experiences": experiences,
    }
    return render(request, "accounts/experience_dashboard.html", context)


@login_required
def add_experience(request):
    if request.method == "POST":
        Experience.objects.create(
            title=request.POST.get("title"),
            company=request.POST.get("company"),
            location=request.POST.get("location", ""),
            start_date=request.POST.get("start_date"),
            end_date=request.POST.get("end_date") or None,
            is_current=request.POST.get("is_current") == "on",
            description=request.POST.get("description", ""),
            order=request.POST.get("order", 0),
        )
        messages.success(request, "Experience added successfully!")
    return redirect("experience_dashboard")


@login_required
def delete_experience(request, experience_id):
    experience = get_object_or_404(Experience, id=experience_id)
    experience.delete()
    messages.success(request, "Experience deleted successfully!")
    return redirect("experience_dashboard")


# Education Dashboard
@login_required
def education_dashboard(request):
    educations = Education.objects.all().order_by("-start_year")

    context = {
        "educations": educations,
    }
    return render(request, "accounts/education_dashboard.html", context)


@login_required
def add_education(request):
    if request.method == "POST":
        Education.objects.create(
            degree=request.POST.get("degree"),
            institution=request.POST.get("institution"),
            location=request.POST.get("location", ""),
            start_year=request.POST.get("start_year"),
            end_year=request.POST.get("end_year") or None,
            description=request.POST.get("description", ""),
            order=request.POST.get("order", 0),
        )
        messages.success(request, "Education added successfully!")
    return redirect("education_dashboard")


@login_required
def delete_education(request, education_id):
    education = get_object_or_404(Education, id=education_id)
    education.delete()
    messages.success(request, "Education deleted successfully!")
    return redirect("education_dashboard")
