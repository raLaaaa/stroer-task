from django.test import TestCase
from fakeapi.models import Comment, Post


class PostTest(TestCase):

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
            post=post_one
        )

        comment_two = Comment.objects.create(
            email="test@gmail.com",
            name="Test Name",
            server_id=2,
            body="Blablablabla",
            post=post_two
        )

    def test_posts(self):
        post_one = Post.objects.get(title='Post One Title')
        post_two = Post.objects.get(title='Post Two Title')

        comment_one = Comment.objects.get(email='test@yahoo.de')
        comment_two = Comment.objects.get(email='test@gmail.com')

        self.assertEqual(
            post_one.title, "Post One Title")
        self.assertEqual(
            post_two.title, "Post Two Title")        
        self.assertEqual(
            comment_one.name, "Marcel")
        self.assertEqual(
            comment_two.name, "Test Name")
        self.assertEqual(
            comment_one.post, post_one)
        self.assertEqual(
            comment_two.post, post_two)
        self.assertEqual(
            post_one.user_id, 99999942)
        self.assertEqual(
            post_two.user_id, 99999942)