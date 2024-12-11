# core/management/commands/initialize_permissions.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Permission, Group
from django.contrib.contenttypes.models import ContentType
from core.models import User


class Command(BaseCommand):
    help = 'Initialize custom permissions and groups'

    def handle(self, *args, **kwargs):
        # Content type for User model
        content_type = ContentType.objects.get_for_model(User)

        # Create permissions
        self.create_permissions(content_type)

        # Create groups
        self.create_groups()

        self.stdout.write(self.style.SUCCESS('Custom permissions and groups initialized.'))

    def create_permissions(self, content_type):
        permissions = [
            {
                "codename": "can_manage_own_assets",
                "name": "Can manage own assets",
            },
            {
                "codename": "can_manage_client_assets",
                "name": "Can manage client assets",
            },
        ]

        for perm in permissions:
            if not Permission.objects.filter(codename=perm["codename"]).exists():
                Permission.objects.create(
                    codename=perm["codename"],
                    name=perm["name"],
                    content_type=content_type,
                )
                self.stdout.write(self.style.SUCCESS(f'Permission "{perm["codename"]}" created successfully.'))

    def create_groups(self):
        # Group definitions with associated permissions
        groups = [
            {
                "name": "Admin",
                "permissions": Permission.objects.all(),
            },
            {
                "name": "FundManager",
                "permissions": Permission.objects.filter(
                    codename__in=["can_manage_client_assets"]
                ),
            },
            {
                "name": "FundAdmin",
                "permissions": Permission.objects.filter(
                    codename__in=["can_manage_own_assets"]
                ),
            },
        ]

        for group_data in groups:
            group, created = Group.objects.get_or_create(name=group_data["name"])
            if created:
                group.permissions.set(group_data["permissions"])
                self.stdout.write(self.style.SUCCESS(f'Group "{group_data["name"]}" created successfully.'))
            else:
                self.stdout.write(self.style.WARNING(f'Group "{group_data["name"]}" already exists.'))

