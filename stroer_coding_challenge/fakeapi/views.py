from django.shortcuts import render
from rest_framework.generics import ListAPIView
from rest_framework.generics import CreateAPIView
from rest_framework.generics import DestroyAPIView
from rest_framework.generics import UpdateAPIView
from fakeapi.models import Comment, Post
from fakeapi.serializers.post_serializer_user import PostSerializerUser
from fakeapi.serializers.comment_serializer import CommentSerializer
from fakeapi.serializers.comment_serializer_user import CommentSerializerUser
from rest_framework.permissions import IsAuthenticated


class ListPostAPIView(ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializerUser
    permission_classes = [IsAuthenticated]


class CreatePostAPIView(CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializerUser
    permission_classes = [IsAuthenticated]


class UpdatePostAPIView(UpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializerUser
    lookup_url_kwarg = "server_id"
    lookup_field = "server_id"
    permission_classes = [IsAuthenticated]


class DeletePostAPIView(DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializerUser
    lookup_url_kwarg = "server_id"
    lookup_field = "server_id"
    permission_classes = [IsAuthenticated]


class ListCommentAPIView(ListAPIView):
    serializer_class = CommentSerializer
    lookup_url_kwarg = "server_id"
    lookup_field = "server_id"
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Comment.objects.filter(post__server_id=self.kwargs["post_server_id"])
        return queryset


class CreateCommentAPIView(CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializerUser
    permission_classes = [IsAuthenticated]
    lookup_url_kwarg = "post_server_id"
    lookup_field = "server_id"

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"post_id_from_url": self.kwargs["post_server_id"]})
        return context


class UpdateCommentAPIView(UpdateAPIView):
    serializer_class = CommentSerializerUser
    lookup_url_kwarg = "comment_server_id"
    lookup_field = "server_id"
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Comment.objects.filter(
            post__server_id=self.kwargs["post_server_id"],
            server_id=self.kwargs["comment_server_id"],
        )
        return queryset


class DeleteCommentAPIView(DestroyAPIView):
    serializer_class = CommentSerializerUser
    lookup_url_kwarg = "comment_server_id"
    lookup_field = "server_id"
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Comment.objects.filter(
            post__server_id=self.kwargs["post_server_id"],
            server_id=self.kwargs["comment_server_id"],
        )
        return queryset
