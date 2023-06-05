import logging
import json
import requests

from django.core.management import BaseCommand
from django.db import transaction

from fakeapi.serializers.post_serializer import PostSerializer
from fakeapi.serializers.comment_serializer import CommentSerializer
from fakeapi.models import Post, Comment

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Fetches Posts & Comments from the FakeAPI. This will result in a fresh database state. All objects get reimported."

    def requestPosts(self):
        self.stdout.write("Cleaning old posts of database...")
        Post.objects.all().delete()

        self.stdout.write("Fetching posts...")
        r = requests.get("https://jsonplaceholder.typicode.com/posts")
        response = json.loads(r.text)

        post_serializer = PostSerializer(data=response, many=True)
        post_serializer.is_valid(raise_exception=True)
        post_serializer.save()
        self.stdout.write(f"Successfully created {len(post_serializer.data)} posts.")

    def requestComments(self):
        self.stdout.write("Cleaning old comments of database...")
        Comment.objects.all().delete()

        self.stdout.write("Fetching comments...")
        r = requests.get("https://jsonplaceholder.typicode.com/comments")
        response = json.loads(r.text)

        comment_serializer = CommentSerializer(data=response, many=True)
        comment_serializer.is_valid(raise_exception=True)
        comment_serializer.save()
        self.stdout.write(
            f"Successfully created {len(comment_serializer.data)} comments."
        )

    def handle(self, *args, **options):
        self.stdout.write(f"--------------------")
        self.stdout.write(f"Importing data from fake api")
        with transaction.atomic():
            self.requestPosts()
            self.requestComments()
        self.stdout.write(f"--------------------")
