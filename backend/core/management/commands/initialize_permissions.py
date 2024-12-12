# core/management/commands/initialize_permissions.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group


class Command(BaseCommand):
    help = 'Initialize groups for the application'

    def handle(self, *args, **kwargs):
        # Создание групп
        self.create_groups()

        self.stdout.write(self.style.SUCCESS('Groups initialized successfully.'))

    def create_groups(self):
        """
        Create groups for access management
        """
        group_names = [
            "FundAdmin",
            "FundManager",
        ]

        for group_name in group_names:
            group, created = Group.objects.get_or_create(name=group_name)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Group "{group_name}" created successfully.'))
            else:
                self.stdout.write(self.style.WARNING(f'Group "{group_name}" already exists.'))
