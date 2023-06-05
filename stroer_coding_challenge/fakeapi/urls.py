from django.urls import path

from . import views

urlpatterns = [
    path("posts/", views.ListPostAPIView.as_view(), name="post_list"),  # works
    path(
        "posts/create/", views.CreatePostAPIView.as_view(), name="post_create"
    ),  # works
    path(
        "posts/update/<int:server_id>/",
        views.UpdatePostAPIView.as_view(),
        name="post_update",
    ),  # works
    path(
        "posts/delete/<int:server_id>/",
        views.DeletePostAPIView.as_view(),
        name="post_delete",
    ),  # works
    path(
        "posts/<int:post_server_id>/comments/",
        views.ListCommentAPIView.as_view(),
        name="comment_list",
    ),  # works
    path(
        "posts/<int:post_server_id>/comments/create/",
        views.CreateCommentAPIView.as_view(),
        name="comment_create",
    ),  #
    path(
        "posts/<int:post_server_id>/comments/update/<int:comment_server_id>/",
        views.UpdateCommentAPIView.as_view(),
        name="comment_update",
    ),
    path(
        "posts/<int:post_server_id>/comments/delete/<int:comment_server_id>/",
        views.DeleteCommentAPIView.as_view(),
        name="comment_delete",
    ),
]
