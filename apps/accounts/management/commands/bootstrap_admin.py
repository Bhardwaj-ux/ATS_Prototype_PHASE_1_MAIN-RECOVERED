import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = "Create or update admin user from environment variables"

    def handle(self, *args, **options):
        User = get_user_model()

        email = os.getenv("ADMIN_EMAIL")
        password = os.getenv("ADMIN_PASSWORD")
        username = os.getenv("ADMIN_USERNAME", "admin")

        if not email or not password:
            self.stdout.write(
                self.style.WARNING("ADMIN_EMAIL or ADMIN_PASSWORD not set. Skipping admin bootstrap.")
            )
            return

        field_names = {f.name for f in User._meta.get_fields()}

        if "email" in field_names:
            lookup = {"email": email}
        else:
            lookup = {User.USERNAME_FIELD: username}

        defaults = {}
        if "email" in field_names:
            defaults["email"] = email
        if "username" in field_names:
            defaults["username"] = username

        user, created = User.objects.get_or_create(**lookup, defaults=defaults)

        if "email" in field_names:
            user.email = email
        if "username" in field_names and not getattr(user, "username", None):
            user.username = username

        user.is_staff = True
        user.is_superuser = True
        if hasattr(user, "is_active"):
            user.is_active = True

        user.set_password(password)
        user.save()

        if created:
            self.stdout.write(self.style.SUCCESS(f"Created admin user: {email}"))
        else:
            self.stdout.write(self.style.SUCCESS(f"Updated admin user: {email}"))