from rest_framework import serializers

from fakeapi.models import Comment, Post


class CommentSerializer(serializers.ModelSerializer):
    postId = serializers.IntegerField(write_only=True, source="post")

    id = serializers.IntegerField(required=True, source="server_id")
    name = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    body = serializers.CharField(required=True)

    def create(self, validated_data):
        comment = Comment.objects.create(
            email=validated_data.pop("email"),
            name=validated_data.pop("name"),
            server_id=validated_data.pop("server_id"),
            body=validated_data.pop("body"),
            post=Post.objects.get(server_id=validated_data.pop("post")),
        )

        return comment

    class Meta:
        model = Comment
        fields = ["id", "postId", "name", "email", "body"]
