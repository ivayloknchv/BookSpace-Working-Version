from django.urls import reverse
from django.test import TestCase, Client
from activities.models import FollowActivity
from users.models import User, FollowRelation
from django.contrib.auth.models import AbstractUser


class UserTest(TestCase):

    def test_user_creations(self):
        user = User(first_name='My', last_name='User', username='username', password='bjngfdmk')
        user.save()

        self.assertTrue(isinstance(user, User))
        self.assertTrue(issubclass(type(user), AbstractUser))
        self.assertEqual(str(user), 'username')


class FollowTest(TestCase):

    def test_follow_relation_creations(self):
        user1 = User(first_name='My', last_name='User', username='username1', password='bjngfdmk')
        user1.save()
        user2 = User(first_name='My', last_name='User', username='username2', password='bjngfdmk')
        user2.save()

        follow = FollowRelation(follower=user1, followed=user2)
        follow.save()

        self.assertTrue(isinstance(follow, FollowRelation))


class UserViewsTest(TestCase):

    def setUp(self):
        self.client = Client()

        self.user1 = User.objects.create_user(first_name='My', last_name='User',
                                              username='username1', password='password123')
        self.user2 = User.objects.create_user(first_name='My', last_name='User',
                                              username='username2', password='password123')

    def test_login_success(self):
        response = self.client.post(reverse('login'), {'username': 'username1', 'password': 'password123'})
        self.assertEqual(response.status_code, 302)

    def test_login_invalid_credentials(self):
        response = self.client.post(reverse('login'), {'username': 'username1', 'password': 'password1234'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue('Invalid credentials!' in list(message.message for message in response.context['messages']))

    def test_login_already_logged(self):
        self.client.force_login(self.user1)
        response = self.client.post(reverse('login'), {'username': 'username1', 'password': 'password123'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))

    def test_logout(self):
        self.client.force_login(self.user1)
        response=self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)

    def test_view_edit_profile(self):
        self.client.force_login(self.user1)
        response=self.client.get(reverse('edit_profile'))
        self.assertEqual(response.status_code, 200)

    def test_view_profile(self):
        self.client.force_login(self.user1)
        response = self.client.get(reverse('profile', kwargs={'username' : self.user1.username}))
        self.assertEqual(response.status_code, 200)

    def test_follow_user(self):
        self.client.force_login(self.user1)
        self.client.get(reverse('follow_user', kwargs={'username': self.user2.username}))
        self.assertTrue(FollowRelation.objects.filter(follower=self.user1, followed=self.user2).exists())
        self.assertTrue(FollowActivity.objects.filter(initiator=self.user1, followed_user=self.user2).exists())

    def test_unfollow_user(self):
        FollowRelation(follower=self.user1, followed=self.user2).save()
        self.client.force_login(self.user1)
        self.client.get(reverse('unfollow_user', kwargs={'username': self.user2.username}))
        self.assertFalse(FollowRelation.objects.filter(follower=self.user1, followed=self.user2).exists())

    def test_delete_account_success(self):
        self.client.force_login(self.user1)
        response = self.client.post(reverse('delete_account'), {'password_input' : 'password123'})
        self.assertFalse(User.objects.filter(username='username1').exists())
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))

    def test_delete_account_fail(self):
        self.client.force_login(self.user1)
        response = self.client.post(reverse('delete_account'), {'password_input': 'password1234'})
        self.assertTrue(User.objects.filter(username='username1').exists())
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('edit_profile'))

    def test_want_to_read_books(self):
        self.client.force_login(self.user1)
        response = self.client.get(reverse('want_to_read_books', kwargs={'username': self.user1.username}))
        self.assertEqual(response.status_code, 200)

    def test_currently_reading_books(self):
        self.client.force_login(self.user1)
        response = self.client.get(reverse('currently_reading_books', kwargs={'username': self.user1.username}))
        self.assertEqual(response.status_code, 200)

    def test_read_books(self):
        self.client.force_login(self.user1)
        response = self.client.get(reverse('read_books', kwargs={'username': self.user1.username}))
        self.assertEqual(response.status_code, 200)

    def test_reviewed_books(self):
        self.client.force_login(self.user1)
        response = self.client.get(reverse('reviewed_books', kwargs={'username': self.user1.username}))
        self.assertEqual(response.status_code, 200)

    def test_view_followers(self):
        self.client.force_login(self.user1)
        response = self.client.get(reverse('followers', kwargs={'username': self.user1.username}))
        self.assertEqual(response.status_code, 200)

    def test_view_following(self):
        self.client.force_login(self.user1)
        response = self.client.get(reverse('following', kwargs={'username': self.user1.username}))
        self.assertEqual(response.status_code, 200)