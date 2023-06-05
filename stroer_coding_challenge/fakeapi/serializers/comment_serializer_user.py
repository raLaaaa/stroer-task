from rest_framework import serializers

from fakeapi.models import Comment, Post


class CommentSerializerUser(serializers.ModelSerializer):
    server_id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    body = serializers.CharField(required=True)

    def create(self, validated_data):
        id_from_url = self.context.get("post_id_from_url")

        comment = Comment.objects.create(
            email=validated_data.pop("email"),
            name=validated_data.pop("name"),
            server_id=-1,
            body=validated_data.pop("body"),
            post=Post.objects.get(server_id=id_from_url),
        )

        comment.server_id = comment.id
        comment.save()

        return comment

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.email = validated_data.get("email", instance.email)
        instance.body = validated_data.get("body", instance.body)
        # We do not want to move posts directly
        # instance.post = Post.objects.get(server_id=validated_data.get('postId', instance.server_id))
        instance.save()
        return instance

    class Meta:
        model = Comment
        fields = ["id", "server_id", "name", "email", "body"]
