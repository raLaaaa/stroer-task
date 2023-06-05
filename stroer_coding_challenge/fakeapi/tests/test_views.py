import json
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from fakeapi.models import Comment, Post
from fakeapi.serializers.post_serializer_user import PostSerializerUser
from fakeapi.serializers.post_serializer import PostSerializer
from fakeapi.serializers.comment_serializer import CommentSerializer
from fakeapi.serializers.comment_serializer_user import CommentSerializerUser


client = Client()


def setup_auth():
    test_user = User.objects.create(username="user")
    test_user.set_password("1234")
    test_user.save()
    test_user_token = Token.objects.create(user=test_user)
    client.defaults["HTTP_AUTHORIZATION"] = "Bearer " + str(test_user_token)


class AuthTest(TestCase):
    def setUp(self):
        test_user = User.objects.create(username="user")
        test_user.set_password("1234")
        test_user.save()

        self.valid_payload = {
            "username": "user",
            "password": "1234",
        }

        self.invalid_payload = {
            "username": "user",
            "password": "12345",
        }

    def test_valid_auth(self):
        response = client.post(
            reverse("auth"),
            data=json.dumps(self.valid_payload),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_auth(self):
        response = client.post(
            reverse("auth"),
            data=json.dumps(self.invalid_payload),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class GetAllPostsTest(TestCase):
    def setUp(self):
        post_one = Post.objects.create(
            title="Post One Title",
            body="Post One Body",
            server_id=-1,
        )

        post_one.server_id = post_one.id
        post_one.save()

        post_two = Post.objects.create(
            title="Post Two Title",
            body="Post Two Body",
            server_id=-1,
        )

        post_two.server_id = post_two.id
        post_two.save()

        comment_one = Comment.objects.create(
            email="test@yahoo.de",
            name="Marcel",
            server_id=1,
            body="Blablablabla",
            post=post_one,
        )

        comment_two = Comment.objects.create(
            email="test@gmail.com",
            name="Test Name",
            server_id=2,
            body="Blublublublu",
            post=post_two,
        )

        setup_auth()

    def test_get_all_posts(self):
        response = client.get(reverse("post_list"))

        posts = Post.objects.all()
        serializer = PostSerializerUser(posts, many=True)

        self.assertEqual(serializer.data, response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetAllCommentsOfPostTest(TestCase):
    def setUp(self):
        post_one = Post.objects.create(
            title="Post One Title",
            body="Post One Body",
            server_id=-1,
        )

        post_one.server_id = post_one.id
        post_one.save()

        post_two = Post.objects.create(
            title="Post Two Title",
            body="Post Two Body",
            server_id=-1,
        )

        post_two.server_id = post_two.id
        post_two.save()

        comment_one = Comment.objects.create(
            email="test@yahoo.de",
            name="Marcel",
            server_id=1,
            body="Blablablabla",
            post=post_one,
        )

        comment_two = Comment.objects.create(
            email="test@gmail.com",
            name="Test Name",
            server_id=2,
            body="Blublublublu",
            post=post_two,
        )

        setup_auth()

    def test_get_all_posts(self):
        response = client.get(reverse("comment_list", args="1"))

        comments = Comment.objects.filter(post__id=1)
        serializer = CommentSerializer(comments, many=True)

        self.assertEqual(serializer.data, response.data)
        self.assertEqual(comments.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class CreateNewPostTest(TestCase):
    def setUp(self):
        self.valid_payload = {
            "title": "Test Title",
            "body": "Lorem Ipsum is simply dummy",
        }

        self.invalid_payload = {
            "invalid": "",
            "invalid_two": 4,
        }

        setup_auth()

    def test_create_valid_post(self):
        response = client.post(
            reverse("post_create"),
            data=json.dumps(self.valid_payload),
            content_type="application/json",
        )

        number_of_posts = Post.objects.count()
        self.assertEqual(number_of_posts, 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_post(self):
        response = client.post(
            reverse("post_create"),
            data=json.dumps(self.invalid_payload),
            content_type="application/json",
        )

        number_of_posts = Post.objects.count()
        self.assertEqual(number_of_posts, 0)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class CreateNewCommentTest(TestCase):
    def setUp(self):
        self.valid_payload = {
            "name": "Test Title",
            "email": "testuser@example.com",
            "body": "Lorem Ipsum is simply dummy",
        }

        self.invalid_payload = {
            "email": "invalid email address",
        }

        post_one = Post.objects.create(
            title="Post One Title",
            body="Post One Body",
            server_id=-1,
        )

        post_one.server_id = post_one.id
        post_one.save()

        setup_auth()

    def test_create_valid_comment(self):
        response = client.post(
            reverse("comment_create", args=("1")),
            data=json.dumps(self.valid_payload),
            content_type="application/json",
        )

        number_of_comments = Comment.objects.count()
        number_of_posts = Post.objects.count()
        self.assertEqual(number_of_posts, 1)
        self.assertEqual(number_of_comments, 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_comment(self):
        response = client.post(
            reverse("comment_create", args=("1")),
            data=json.dumps(self.invalid_payload),
            content_type="application/json",
        )

        number_of_comments = Comment.objects.count()
        number_of_posts = Post.objects.count()
        self.assertEqual(number_of_posts, 1)
        self.assertEqual(number_of_comments, 0)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UpdateSinglePostTest(TestCase):
    def setUp(self):
        self.valid_payload = {
            "title": "Test Title Updated",
            "body": "Lorem Ipsum is simply updated. Lorem Ipsum.",
        }

        self.invalid_payload = {
            "title_wrong": "Test Title Updated",
            "body_wrong": "Lorem Ipsum is simply updated. Lorem Ipsum.",
        }

        post_one = Post.objects.create(
            title="Post One Title Not Updated",
            body="Post One Body Not Updated",
            server_id=-1,
        )

        post_one.server_id = post_one.id
        post_one.save()

        setup_auth()

    def test_valid_update_post(self):
        response = client.put(
            reverse("post_update", args=("1")),
            data=json.dumps(self.valid_payload),
            content_type="application/json",
        )

        post = Post.objects.get(server_id=1)
        serializer = PostSerializerUser(post, many=False)

        self.assertEqual(serializer.data, response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_update_post(self):
        response = client.put(
            reverse("post_update", args=("1")),
            data=json.dumps(self.invalid_payload),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UpdateSingleCommentTest(TestCase):
    def setUp(self):
        self.valid_payload = {
            "name": "Test Title",
            "email": "testuser@example.com",
            "body": "Lorem Ipsum is simply dummy",
        }

        self.invalid_payload = {
            "title_wrong": "Test Title Updated",
            "body_wrong": "Lorem Ipsum is simply updated. Lorem Ipsum.",
        }

        post_one = Post.objects.create(
            title="Post One Title Not Updated",
            body="Post One Body Not Updated",
            server_id=-1,
        )

        post_one.server_id = post_one.id
        post_one.save()

        comment_one = Comment.objects.create(
            email="test@yahoo.de",
            name="Marcel",
            server_id=1,
            body="Blablablabla",
            post=post_one,
        )

        setup_auth()

    def test_valid_update_comment(self):
        response = client.put(
            reverse("comment_update", args=("1", "1")),
            data=json.dumps(self.valid_payload),
            content_type="application/json",
        )

        comment = Comment.objects.get(server_id=1)
        serializer = CommentSerializerUser(comment, many=False)

        self.assertEqual(serializer.data, response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_update_comment(self):
        response = client.put(
            reverse("post_update", args=("1")),
            data=json.dumps(self.invalid_payload),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class DeleteSinglePostTest(TestCase):
    def setUp(self):
        post_one = Post.objects.create(
            title="Post One Title Not Updated",
            body="Post One Body Not Updated",
            server_id=-1,
        )

        comment_one = Comment.objects.create(
            email="test@yahoo.de",
            name="Marcel",
            server_id=1,
            body="Blablablabla",
            post=post_one,
        )

        post_one.server_id = post_one.id
        post_one.save()

        setup_auth()

    def test_valid_delete_post(self):
        response = client.delete(reverse("post_delete", args=("1")))

        number_of_comments = Comment.objects.count()
        number_of_posts = Post.objects.count()

        self.assertEqual(number_of_posts, 0)
        self.assertEqual(number_of_comments, 0)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_delete_post(self):
        response = client.delete(reverse("post_delete", args=("2")))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class DeleteSingleCommentTest(TestCase):
    def setUp(self):
        post_one = Post.objects.create(
            title="Post One Title Not Updated",
            body="Post One Body Not Updated",
            server_id=-1,
        )

        comment_one = Comment.objects.create(
            email="test@yahoo.de",
            name="Marcel",
            server_id=1,
            body="Blablablabla",
            post=post_one,
        )

        post_one.server_id = post_one.id
        post_one.save()

        setup_auth()

    def test_valid_delete_comment(self):
        response = client.delete(reverse("comment_delete", args=("1", "1")))

        number_of_comments = Comment.objects.count()
        number_of_posts = Post.objects.count()

        self.assertEqual(number_of_posts, 1)
        self.assertEqual(number_of_comments, 0)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_delete_post(self):
        response = client.delete(reverse("post_delete", args=("9")))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
