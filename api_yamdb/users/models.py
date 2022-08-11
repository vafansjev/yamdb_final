from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLES = [
        ("user", "user"),
        ("moderator", "moderator"),
        ("admin", "admin"),
    ]
    first_name = models.CharField(
        "first name",
        max_length=150,
        blank=True
    )
    email = models.EmailField(
        "email address",
        unique=True
    )
    role = models.CharField(
        "role",
        max_length=20,
        choices=ROLES,
        default='user',
    )
    bio = models.TextField(
        "bio",
        max_length=250,
        blank=True,
    )
    confirmation_code = models.CharField(
        "confirmation_code",
        max_length=150,
        null=True,
        blank=True,
        unique=True
    )

    @property
    def is_user(self):
        return self.role == 'user'

    @property
    def is_admin(self):
        return self.role == 'admin'

    @property
    def is_moderator(self):
        return self.role == 'moderator'

    def __str__(self):
        return self.username
