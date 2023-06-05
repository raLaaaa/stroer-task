import logging
import json
import requests

from django.core.management import BaseCommand
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class Command(BaseCommand):
    def handle(self, *args, **options):
        User.objects.all().delete()
        user = User.objects.create(username="user")
        user.set_password("1234")
        user.save()
        token = Token.objects.create(user=user)
        self.stdout.write(f"--------------------")
        self.stdout.write(f"Created default user with credentials: user / 1234")
        self.stdout.write(f"Token for API is - Authorization: Bearer {token.key}")
        self.stdout.write(f"You can also obtain this token by posting to /auth/")
        self.stdout.write(f"--------------------")
