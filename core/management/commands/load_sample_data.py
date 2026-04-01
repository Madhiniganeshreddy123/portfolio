from django.core.management.base import BaseCommand
from core.models import Project, Profile


class Command(BaseCommand):
    help = "Load or update project and profile data"

    def handle(self, *args, **kwargs):
        Project.objects.filter(title="Customer Behaviour Analysis").update(image="")
        Project.objects.filter(title="Multimodal Sentiment Analysis").update(image="")
        Project.objects.filter(title="Real-Time QR Code System").update(image="")

        Profile.objects.update_or_create(id=1, defaults={"profile_image": ""})

        self.stdout.write(self.style.SUCCESS("Data updated successfully!"))
