from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from fakeapi.models import Post
from fakeapi.serializers.comment_serializer import CommentSerializer


class PostSerializerUser(serializers.ModelSerializer):
    userId = serializers.IntegerField(read_only=True, source="user_id")
    title = serializers.CharField(required=True)
    body = serializers.CharField(required=True)

    comments = CommentSerializer(many=True, read_only=True)

    def create(self, validated_data):
        post = Post.objects.create(
            title=validated_data.pop("title"),
            body=validated_data.pop("body"),
            server_id=-1,
        )

        post.server_id = post.id
        post.save()

        return post

    class Meta:
        model = Post
        fields = ["id", "userId", "title", "body", "comments"]
