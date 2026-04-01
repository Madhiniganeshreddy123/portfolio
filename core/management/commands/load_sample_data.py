from django.core.management.base import BaseCommand
from core.models import Project


class Command(BaseCommand):
    help = "Fix project images"

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

        self.stdout.write(self.style.SUCCESS("Images fixed successfully!"))
