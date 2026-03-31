from django.shortcuts import render, redirect
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
from .models import Profile, SkillCategory, Project, Experience, Education, Message


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


class ContactView(CreateView):
    model = Message
    fields = ["name", "email", "subject", "message"]
    template_name = "portfolio/contact.html"
    success_url = "/"

    def form_valid(self, form):
        messages.success(
            self.request, "Thank you for your message! I will get back to you soon."
        )
        return super().form_valid(form)


def project_detail(request, pk):
    project = Project.objects.get(pk=pk)
    return render(request, "portfolio/project_detail.html", {"project": project})
