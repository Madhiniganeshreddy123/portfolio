from django.core.management.base import BaseCommand
from core.models import Project, Profile


class Command(BaseCommand):
    help = "Load or update project and profile data"

    def handle(self, *args, **kwargs):
        Project.objects.filter(title="Customer Behaviour Analysis").update(
            image="images/dashboard.png"
        )
        Project.objects.filter(title="Multimodal Sentiment Analysis").update(
            image="images/sentiment-analysis.jpeg"
        )
        Project.objects.filter(title="Real-Time QR Code System").update(
            image="images/qr-code.jpeg"
        )

        Profile.objects.update_or_create(
            id=1, defaults={"profile_image": "images/profile-image.jpg"}
        )

        self.stdout.write(self.style.SUCCESS("Data updated successfully!"))
