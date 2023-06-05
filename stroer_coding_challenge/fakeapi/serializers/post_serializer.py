from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from fakeapi.models import Post
from fakeapi.serializers.comment_serializer import CommentSerializer


class PostSerializer(serializers.ModelSerializer):
    userId = serializers.IntegerField(write_only=True, source="user_id")
    id = serializers.IntegerField(
        required=True,
        source="server_id",
        validators=[UniqueValidator(queryset=Post.objects.all())],
    )
    title = serializers.CharField(required=True)
    body = serializers.CharField(required=True)

    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = "__all__"
