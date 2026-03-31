from django.urls import path
from . import views

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("projects/", views.ProjectsView.as_view(), name="projects"),
    path(
        "project/<slug:slug>/", views.ProjectDetailView.as_view(), name="project_detail"
    ),
    path("contact/", views.ContactView.as_view(), name="contact"),
]
