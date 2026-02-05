"""Seed database with sample data for development."""

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

User = get_user_model()


class Command(BaseCommand):
    """Seed database with sample users for development."""

    help = "Seed database with sample data for development"

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Clear existing data before seeding",
        )
        parser.add_argument(
            "--users",
            type=int,
            default=5,
            help="Number of regular users to create (default: 5)",
        )

    def handle(self, *args, **options):
        if options["clear"]:
            self.stdout.write("Clearing existing users...")
            User.objects.exclude(is_superuser=True).delete()
            self.stdout.write(self.style.SUCCESS("Cleared existing users"))

        self.create_admin_user()
        self.create_sample_users(options["users"])
        self.stdout.write(self.style.SUCCESS("\nSeeding complete!"))

    def create_admin_user(self):
        """Create an admin user if it doesn't exist."""
        if User.objects.filter(email="admin@example.com").exists():
            self.stdout.write("Admin user already exists")
            return

        User.objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="admin123",
            first_name="Admin",
            last_name="User",
        )
        self.stdout.write(self.style.SUCCESS("Created admin user: admin@example.com / admin123"))

    def create_sample_users(self, count: int):
        """Create sample regular users."""
        created = 0
        for i in range(1, count + 1):
            email = f"user{i}@example.com"
            if User.objects.filter(email=email).exists():
                self.stdout.write(f"User {email} already exists")
                continue

            User.objects.create_user(
                username=f"user{i}",
                email=email,
                password="password123",
                first_name=f"User",
                last_name=f"{i}",
                bio=f"Sample user {i} for development testing.",
            )
            created += 1

        self.stdout.write(self.style.SUCCESS(f"Created {created} sample users"))
        if created > 0:
            self.stdout.write("  Credentials: user1@example.com / password123")
