# core/model.py
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = (
        ('fund_admin', 'Fund Administrator'),
        ('fund_manager', 'Fund Manager'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    email = models.EmailField(unique=True)  # Email as unique field

    USERNAME_FIELD = 'email'  # Use email as the unique identifier
    REQUIRED_FIELDS = ['username']  # Keep username for compatibility

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='core_users_groups',
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='core_users_permissions',
        blank=True
    )

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
