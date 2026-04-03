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
]
