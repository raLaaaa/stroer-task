import logging
import json
import requests

from django.core.management import BaseCommand
from django.db import transaction

from fakeapi.serializers.post_serializer import PostSerializer
from fakeapi.serializers.comment_serializer import CommentSerializer
from fakeapi.models import Post, Comment


class Command(BaseCommand):
    help = "Syncs our db with fake api."

    def sync(self):
        self.stdout.write("Sending posts and comments...")

        posts = Post.objects.all()
        serializer = PostSerializer(data=posts, many=True)
        serializer.is_valid()
        data = serializer.data

        headers = {"Content-type": "application/json; charset=UTF-8"}

        r = requests.post(
            "https://jsonplaceholder.typicode.com/posts", json=data, headers=headers
        )
        self.stdout.write(str(r.text))
        self.stdout.write(str(r.status_code))
        self.stdout.write("Synced posts.")

    def handle(self, *args, **options):
        self.sync()
        self.stdout.write("Done.")
