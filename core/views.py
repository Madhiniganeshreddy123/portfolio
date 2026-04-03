from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import (
    TemplateView,
    FormView,
    ListView,
    DetailView,
    CreateView,
)
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse
from django.db.models import F
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Profile, SkillCategory, Project, Experience, Education, Message
from .serializers import ProjectSerializer, ProjectListSerializer


class HomeView(TemplateView):
    template_name = "portfolio/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = Profile.objects.first()
        skills = SkillCategory.objects.prefetch_related("skills").all()
        projects = Project.objects.filter(is_featured=True).order_by("order")[:6]
        experiences = Experience.objects.all()
        education = Education.objects.all()

        context.update(
            {
                "profile": profile,
                "skill_categories": skills,
                "projects": projects,
                "experiences": experiences,
                "education": education,
            }
        )
        return context


class ProjectsView(ListView):
    model = Project
    template_name = "portfolio/projects.html"
    context_object_name = "projects"
    paginate_by = 9

    def get_queryset(self):
        return Project.objects.all().order_by("order")


class ProjectDetailView(DetailView):
    model = Project
    template_name = "portfolio/project_detail.html"
    context_object_name = "project"

    def get_object(self):
        return get_object_or_404(Project, slug=self.kwargs["slug"])


class ContactView(TemplateView):
    template_name = "portfolio/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = Profile.objects.first()
        skills = SkillCategory.objects.prefetch_related("skills").all()
        projects = Project.objects.filter(is_featured=True).order_by("order")[:6]
        experiences = Experience.objects.all()
        education = Education.objects.all()

        context.update(
            {
                "profile": profile,
                "skill_categories": skills,
                "projects": projects,
                "experiences": experiences,
                "education": education,
            }
        )
        return context

    def post(self, request, *args, **kwargs):
        name = request.POST.get("name")
        email = request.POST.get("email")
        subject = request.POST.get("subject")
        message_text = request.POST.get("message")

        Message.objects.create(
            name=name, email=email, subject=subject, message=message_text
        )
        messages.success(
            request, "Thank you for your message! I will get back to you soon."
        )
        return redirect("home")


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all().order_by("order")
    serializer_class = ProjectSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return ProjectListSerializer
        return ProjectSerializer

    @action(detail=False, methods=["post"])
    def reorder(self, request):
        order_list = request.data.get("order", [])
        for idx, project_id in enumerate(order_list):
            Project.objects.filter(id=project_id).update(order=idx)
        return Response({"status": "success"})
