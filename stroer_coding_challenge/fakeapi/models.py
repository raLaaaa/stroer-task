from django.db import models


class Post(models.Model):
    user_id = models.BigIntegerField(default=99999942)
    server_id = models.BigIntegerField(default=0, unique=True)
    title = models.CharField(max_length=255)
    body = models.TextField(blank=True)

    def __str__(self):
        return f"<Post:{self.pk} {self.title}. "


class Comment(models.Model):
    email = models.EmailField(max_length=254)
    server_id = models.BigIntegerField(default=0, unique=True)
    name = models.CharField(max_length=255)
    body = models.TextField(blank=True)

    post = models.ForeignKey(
        "Post",
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        related_name="comments",
    )

    def __str__(self):
        return f"<Comment:{self.pk} {self.email} with {self.name}. "
