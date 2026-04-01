from django.core.management.base import BaseCommand
from core.models import Project, Profile


class Command(BaseCommand):
    help = "Load or update project and profile data"

    def handle(self, *args, **kwargs):
        # Clear all images first
        Project.objects.all().update(image="")
        Profile.objects.all().update(profile_image="")

        self.stdout.write(self.style.SUCCESS("Data updated successfully!"))
