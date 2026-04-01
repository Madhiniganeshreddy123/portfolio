from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = "Fix migrations and update data"

    def handle(self, *args, **kwargs):
        cursor = connection.cursor()

        # Check which migrations are applied
        cursor.execute("SELECT name FROM django_migrations WHERE app = 'core'")
        applied = [row[0] for row in cursor.fetchall()]
        self.stdout.write(f"Applied migrations: {applied}")

        # Fix 0002 migration (slug column already exists)
        if "0002_project_slug" not in applied:
            cursor.execute(
                "DELETE FROM django_migrations WHERE app = 'core' AND name IN ('0002_project_slug', '0003_alter_project_image_alter_project_slug', '0004_alter_profile_profile_image')"
            )
            self.stdout.write(
                self.style.WARNING("Deleted migration records for re-applying")
            )
        else:
            # Mark as fake if already applied
            self.stdout.write(
                self.style.SUCCESS("Migration 0002 already applied, skipping...")
            )

        self.stdout.write(self.style.SUCCESS("Database fix completed!"))
