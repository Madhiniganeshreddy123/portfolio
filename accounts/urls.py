from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("register/", views.register_view, name="register"),
    path(
        "message/<int:message_id>/read/",
        views.mark_message_read,
        name="mark_message_read",
    ),
    # Projects
    path("projects/", views.projects_dashboard, name="projects_dashboard"),
    path("projects/edit/<int:project_id>/", views.edit_project, name="edit_project"),
    path(
        "projects/delete/<int:project_id>/", views.delete_project, name="delete_project"
    ),
    # Skills
    path("skills/", views.skills_dashboard, name="skills_dashboard"),
    path("skills/add-category/", views.add_skill_category, name="add_skill_category"),
    path("skills/add/", views.add_skill, name="add_skill"),
    path("skills/delete/<int:skill_id>/", views.delete_skill, name="delete_skill"),
    path(
        "skills/category/delete/<int:category_id>/",
        views.delete_skill_category,
        name="delete_skill_category",
    ),
    # Profile
    path("profile/", views.profile_dashboard, name="profile_dashboard"),
    # Messages
    path("messages/", views.messages_dashboard, name="messages_dashboard"),
    path(
        "messages/toggle/<int:message_id>/",
        views.toggle_message_read,
        name="toggle_message_read",
    ),
    path(
        "messages/delete/<int:message_id>/", views.delete_message, name="delete_message"
    ),
    # Experience
    path("experience/", views.experience_dashboard, name="experience_dashboard"),
    path("experience/add/", views.add_experience, name="add_experience"),
    path(
        "experience/delete/<int:experience_id>/",
        views.delete_experience,
        name="delete_experience",
    ),
    # Education
    path("education/", views.education_dashboard, name="education_dashboard"),
    path("education/add/", views.add_education, name="add_education"),
    path(
        "education/delete/<int:education_id>/",
        views.delete_education,
        name="delete_education",
    ),
]
