from IPython.core.release import author
from sympy import content

from users.models import User
from django.urls import reverse
from django.test import TestCase, Client
from forum.models import Post, Thread, Category, LikeRelation


class CategoryModelTest(TestCase):

    def test_category_creation(self):
        category = Category(name='Category', description='Description')
        category.save()
        self.assertTrue(isinstance(category, Category))
        self.assertEqual(str(category), 'Category')
        self.assertEqual(category.slug, 'category')


class ThreadModelTest(TestCase):

    def test_thread_creation(self):
        user = User.objects.create_user(first_name='My', last_name='User',
                                        username='username', password='password123')
        category = Category(name='Category', description='Description')
        category.save()
        thread = Thread(author=user, category=category, title='Title')
        thread.save()

        self.assertTrue(isinstance(thread, Thread))
        self.assertEqual(str(thread), 'Title')
        self.assertEqual(thread.slug, 'title-1')


class PostModelTest(TestCase):

    def test_post_creation(self):
        user = User.objects.create_user(first_name='My', last_name='User',
                                        username='username', password='password123')
        category = Category(name='Category', description='Description')
        category.save()
        thread = Thread(author=user, category=category, title='Title')
        thread.save()
        post = Post(author=user, thread=thread, caption='Caption')
        post.save()
        self.assertTrue(isinstance(post, Post))
        self.assertEqual(str(post), '1')


class LikeRelationModelTest(TestCase):

    def test_like_relation_creation(self):
        user = User.objects.create_user(first_name='My', last_name='User',
                                        username='username', password='password123')
        category = Category(name='Category', description='Description')
        category.save()
        thread = Thread(author=user, category=category, title='Title')
        thread.save()
        post = Post(author=user, thread=thread, caption='Caption')
        post.save()
        like = LikeRelation(user=user, post=post)
        like.save()
        self.assertTrue(isinstance(like, LikeRelation))
        self.assertEqual(str(like), 'username liked username\'s post in Title')

class ForumViewsTest(TestCase):

    def setUp(self):
        self.client = Client()

        self.user1 = User.objects.create_user(first_name='My', last_name='User',
                                              username='username1', password='password123')
        self.user2 = User.objects.create_user(first_name='My', last_name='User',
                                              username='username2', password='password123')

        self.category = Category(name='Category', description='Description')
        self.category.save()

        self.thread = Thread(author=self.user1, category=self.category, title='Thread')
        self.thread.save()

        self.post = Post(author=self.user2, thread=self.thread, caption='Post')
        self.post.save()

    def test_show_homepage(self):
        self.client.force_login(self.user1)
        response = self.client.post(reverse('forum_homepage'))
        self.assertEqual(response.status_code, 200)

    def test_show_category(self):
        self.client.force_login(self.user1)
        response = self.client.post(reverse('show_category', kwargs={'slug' : self.category.slug}))
        self.assertEqual(response.status_code, 200)

    def test_create_thread(self):
        self.client.force_login(self.user1)
        response = self.client.post(reverse('create_thread', kwargs={'slug': self.category.slug}))
        self.assertEqual(response.status_code, 200)

    def test_save_thread(self):
        self.client.force_login(self.user1)
        response = self.client.post(reverse('save_thread', kwargs={'slug': self.category.slug}),
                                    {'title':'Title', 'caption':'Caption'})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Thread.objects.filter(title='Title', author=self.user1).exists())

    def test_view_thread(self):
        self.client.force_login(self.user1)
        response = self.client.post(reverse('view_thread', kwargs={'slug': self.thread.slug}))
        self.assertEqual(response.status_code, 200)

    def test_add_reply_valid(self):
        self.client.force_login(self.user2)
        response = self.client.post(reverse('add_reply', kwargs={'slug': self.thread.slug}),
                                    {'caption' : 'Reply'})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Post.objects.filter(author=self.user2, thread=self.thread, caption='Reply').exists())


    def test_add_reply_invalid(self):
        self.client.force_login(self.user2)
        response = self.client.post(reverse('add_reply', kwargs={'slug': self.thread.slug}))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Post.objects.filter(author=self.user2, thread=self.thread, caption='Reply').exists())

    def test_like_post(self):
        self.client.force_login(self.user2)
        response = self.client.post(reverse('like_post', kwargs={'pk': self.post.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(LikeRelation.objects.filter(user=self.user2, post=self.post).exists())

    def test_unlike_post(self):
        self.client.force_login(self.user2)
        LikeRelation(user=self.user2, post=self.post).save()
        response = self.client.post(reverse('unlike_post', kwargs={'pk': self.post.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(LikeRelation.objects.filter(user=self.user2, post=self.post).exists())