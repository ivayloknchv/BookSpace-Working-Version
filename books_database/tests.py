from datetime import datetime
from django.db import models
from django.db import IntegrityError
from django.test import TestCase, Client
from django.urls import reverse
from users.models import User
from .models import (Book, Genre, Author, WantToReadBook,
                     CurrentlyReadingBook, ReadBook, BookReview)
from .views import handle_want_to_read, handle_currently_reading, handle_read, handle_reset, remove_review
from activities.models import WantToReadActivity, ReadActivity, CurrentlyReadingActivity


class GenreModelTest(TestCase):

    def test_genre_creation(self):
        genre = Genre(name='My Genre')
        genre.save()
        self.assertTrue(isinstance(genre, Genre))
        self.assertEqual(str(genre), 'My Genre')

    def test_genres_unique_names(self):
        genre = Genre(name='My Genre')
        genre.save()

        with self.assertRaises(IntegrityError):
            Genre.objects.create(name='My Genre')

    def test_genre_slug(self):
        genre = Genre(name='My Genre')
        genre.save()
        self.assertEqual(genre.slug, 'my-genre')

    def test_genre_url(self):
        genre = Genre(name='My Genre')
        genre.save()
        self.assertEqual(genre.get_absolute_url(), '/genres/my-genre/')


class AuthorModelTest(TestCase):

    def test_author_creation(self):
        author = Author(name='My Author')
        author.save()
        self.assertTrue(isinstance(author, Author))
        self.assertEqual(str(author), 'My Author')

    def test_authors_unique_names(self):
        author = Author(name='My Author')
        author.save()

        with self.assertRaises(IntegrityError):
            Author.objects.create(name='My Author')

    def test_author_slug(self):
        author= Author(name='My Author')
        author.save()
        self.assertEqual(author.slug, f'my-author-{author.pk}')

    def test_authors_unique_slugs(self):
        author1 = Author(name='My author')
        author1.save()
        author2 = Author(name='My Author')
        author2.save()
        self.assertNotEqual(str(author1), str(author2))
        self.assertNotEqual(author1.slug, author2.slug)

    def test_author_url(self):
        author = Author(name='My Author')
        author.save()
        self.assertEqual(author.get_absolute_url(), f'/authors/my-author-{author.pk}/')


class BookModelTest(TestCase):

    def setUp(self):
        self.genre1 = Genre(name='My Genre 1')
        self.genre1.save()
        self.genre2 = Genre(name='My Genre 2')
        self.genre2.save()

        self.author = Author(name='Author')
        self.author.save()

        self.book = Book(title='My Title', author=self.author,
                    cover_url='https://d28hgpri8am2if.cloudfront.net/book_images/onix/cvr9781787550360/classic-book'
                              '-cover-foiled-journal-9781787550360_hr.jpg', description='My Description')
        self.book.save()
        self.book.genres.add(self.genre1, self.genre2)

        self.user1 = User(first_name='User1', last_name='User1', username='user1')
        self.user1.save()
        self.user1.preferred_genres.add(self.genre1)

        self.user2 = User(first_name='User2', last_name='User2', username='user2')
        self.user2.save()
        self.user2.preferred_genres.add(self.genre2)

    def test_book_creation(self):
        self.assertTrue(isinstance(self.book, Book))
        self.assertEqual(str(self.book), 'My Title by Author')

    def test_unique_book_titles(self):
        with self.assertRaises(IntegrityError):
            Book.objects.create(title='My Title')

    def test_book_slug(self):
        slug_test = f'my-title-{self.book.pk}'
        self.assertEqual(self.book.slug, slug_test)

    def test_book_url(self):
        self.assertEqual(self.book.get_absolute_url(), '/book/my-title-1/')

    def test_average_user_score_1(self):
        review1 = BookReview(book=self.book, review_user=self.user1, review_score=1, review_date=datetime.now())
        review1.save()
        review2 = BookReview(book=self.book, review_user=self.user2, review_score=3, review_date=datetime.now())
        review2.save()
        self.assertEqual(self.book.avg_review, 2)

    def test_average_user_score_2(self):
        review1 = BookReview(book=self.book, review_user=self.user1, review_score=4, review_date=datetime.now())
        review1.save()
        review2 = BookReview(book=self.book, review_user=self.user2, review_score=3, review_date=datetime.now())
        review2.save()
        self.assertEqual(self.book.avg_review, 3.5)

    def test_book_stars_count(self):
        review1 = BookReview(book=self.book, review_user=self.user1, review_score=5, review_date=datetime.now())
        review1.save()
        review2 = BookReview(book=self.book, review_user=self.user2, review_score=3, review_date=datetime.now())
        review2.save()
        review3 = BookReview(book=self.book, review_user=self.user2, review_score=3, review_date=datetime.now())
        review3.save()

        stars_count = self.book.reviews_by_stars_count

        self.assertEqual(stars_count[5], 1)
        self.assertEqual(stars_count[3], 2)
        self.assertEqual(stars_count[1], 0)
        self.assertNotEqual(stars_count[4],10)
        self.assertNotEqual(stars_count[2], 1)


class BookStatusTest(TestCase):

    def setUp(self):
        self.author = Author(name='My Author')
        self.author.save()

        self.genre = Genre(name='My Genre')
        self.genre.save()

        self.book = Book(title='My Title', author=self.author)
        self.book.save()
        self.book.genres.add(self.genre)

        self.user = User(first_name='User', last_name='User', username='user')
        self.user.save()

    def test_want_to_read_creation(self):
        want_to_read = WantToReadBook(book=self.book, user=self.user, add_date=datetime.now())
        want_to_read.save()
        self.assertTrue(isinstance(want_to_read, WantToReadBook))
        self.assertTrue(isinstance(want_to_read, models.Model))
        self.assertFalse(isinstance(want_to_read, CurrentlyReadingBook))

    def test_currently_reading_creation(self):
        currently_reading = WantToReadBook(book=self.book, user=self.user, add_date=datetime.now())
        currently_reading.save()
        self.assertTrue(isinstance(currently_reading, WantToReadBook))
        self.assertTrue(isinstance(currently_reading, models.Model))
        self.assertFalse(isinstance(currently_reading, CurrentlyReadingBook))

    def test_read_book_creation(self):
        read = ReadBook(book=self.book, user=self.user, read_date=datetime.now())
        read.save()
        self.assertTrue(isinstance(read, ReadBook))
        self.assertTrue(isinstance(read, models.Model))
        self.assertFalse(isinstance(read, WantToReadBook))

    def test_book_review_creation(self):
        review = BookReview(book=self.book, review_user=self.user, review_score=5, review_date=datetime.now())
        review.save()
        self.assertTrue(isinstance(review, BookReview))
        self.assertEqual(review.review_score, 5)
        self.assertEqual(str(review), f'Review for {self.book.title} - {review.review_score}')


class ViewsTest(TestCase):

    def setUp(self):
        self.client = Client()

        self.author1 = Author(name='Author 1')
        self.author1.save()
        self.author2 = Author(name='Author 2')
        self.author2.save()

        self.genre1 = Genre(name='Genre 1')
        self.genre1.save()
        self.genre2 = Genre(name='Genre 2')
        self.genre2.save()

        self.book1 = Book(title='Title 1', author=self.author1)
        self.book1.save()
        self.book1.genres.add(self.genre1, self.genre2)
        self.book2 = Book(title='Title 2', author=self.author2)
        self.book2.save()
        self.book2.genres.add(self.genre2)

        self.user = User(first_name='User',last_name='User', username='user', password='asfgj3Afk')
        self.user.save()

    def test_all_authors_view(self):
        response = self.client.get(reverse('authors'))
        self.assertEqual(response.status_code, 200)

    def test_author_view_valid(self):
        response1 = self.client.get(reverse('preview_author', kwargs={'slug' : self.author1.slug}))
        response2 = self.client.get(reverse('preview_author', kwargs={'slug': self.author2.slug}))
        self.assertEqual(response1.status_code, 200)
        self.assertEqual(response2.status_code, 200)

    def test_author_view_invalid(self):
        response = self.client.get(reverse('preview_author', kwargs={'slug': 'random-slug'}))
        self.assertEqual(response.status_code, 404)

    def test_all_genres_view(self):
        response = self.client.get(reverse('genres'))
        self.assertEqual(response.status_code, 200)

    def test_genre_view_valid(self):
        response1 = self.client.get(reverse('preview_genre', kwargs={'slug' : self.genre1.slug}))
        response2 = self.client.get(reverse('preview_genre', kwargs={'slug': self.genre2.slug}))
        self.assertEqual(response1.status_code, 200)
        self.assertEqual(response2.status_code, 200)

    def test_genre_view_invalid(self):
        response = self.client.get(reverse('preview_genre', kwargs={'slug': 'random-slug'}))
        self.assertEqual(response.status_code, 404)

    def test_book_view_valid(self):
        response1 = self.client.get(reverse('book', kwargs={'slug' : self.book1.slug}))
        response2 = self.client.get(reverse('book', kwargs={'slug': self.book2.slug}))
        self.assertEqual(response1.status_code, 200)
        self.assertEqual(response2.status_code, 200)

    def test_book_view_invalid(self):
        response = self.client.get(reverse('book', kwargs={'slug': 'random-slug'}))
        self.assertEqual(response.status_code, 404)

    def test_want_to_read_a_book_with_currently_reading(self):
        """Test moving a book from Currently Reading to Want To Read status"""

        CurrentlyReadingBook(book=self.book2, user=self.user, add_date=datetime.now()).save()
        handle_want_to_read(self.user, self.book2)

        self.assertTrue(WantToReadBook.objects.filter(book=self.book2, user=self.user).exists())
        self.assertFalse(CurrentlyReadingBook.objects.filter(book=self.book2, user=self.user).exists())
        self.assertTrue(WantToReadActivity.objects.filter(initiator=self.user, book=self.book2).exists())

    def test_want_to_read_a_book_with_read(self):
        """Test moving a book from Read to Want To Read status"""

        ReadBook(book=self.book1, user=self.user, read_date=datetime.now()).save()
        handle_want_to_read(self.user, self.book1)

        self.assertTrue(WantToReadBook.objects.filter(book=self.book1, user=self.user).exists())
        self.assertFalse(ReadBook.objects.filter(book=self.book1, user=self.user).exists())
        self.assertTrue(WantToReadActivity.objects.filter(initiator=self.user, book=self.book1).exists())

    def test_currently_reading_with_want_to_read(self):
        """Test moving a book from Want to Read to Currently Reading status"""

        WantToReadBook(book=self.book1, user=self.user, add_date=datetime.now()).save()
        handle_currently_reading(self.user, self.book1)

        self.assertTrue(CurrentlyReadingBook.objects.filter(book=self.book1, user=self.user).exists())
        self.assertFalse(WantToReadBook.objects.filter(book=self.book1, user=self.user).exists())
        self.assertTrue(CurrentlyReadingActivity.objects.filter(initiator=self.user, book=self.book1).exists())

    def test_currently_reading_with_read(self):
        """Test moving a book from Read to Currently Reading status"""

        ReadBook(book=self.book2, user=self.user, read_date=datetime.now()).save()
        handle_currently_reading(self.user, self.book2)

        self.assertTrue(CurrentlyReadingBook.objects.filter(book=self.book2, user=self.user).exists())
        self.assertFalse(WantToReadBook.objects.filter(book=self.book2, user=self.user).exists())
        self.assertTrue(CurrentlyReadingActivity.objects.filter(initiator=self.user, book=self.book2).exists())

    def test_read_with_want_to_read(self):
        """Test moving a book from Want to Read to Read status"""

        WantToReadBook(book=self.book1, user=self.user, add_date=datetime.now()).save()
        handle_read(self.user, self.book1)

        self.assertTrue(ReadBook.objects.filter(book=self.book1, user=self.user).exists())
        self.assertFalse(WantToReadBook.objects.filter(book=self.book1, user=self.user).exists())
        self.assertTrue(ReadActivity.objects.filter(initiator=self.user, book=self.book1).exists())

    def test_read_with_currently_reading(self):
        """Test moving a book from Want to Read to Read status"""

        CurrentlyReadingBook(book=self.book2, user=self.user, add_date=datetime.now()).save()
        handle_read(self.user, self.book2)

        self.assertTrue(ReadBook.objects.filter(book=self.book2, user=self.user).exists())
        self.assertFalse(CurrentlyReadingBook.objects.filter(book=self.book2, user=self.user).exists())
        self.assertTrue(ReadActivity.objects.filter(initiator=self.user, book=self.book2).exists())

    def test_handle_reset_currently_reading(self):
        CurrentlyReadingBook(book=self.book1, user=self.user, add_date=datetime.now()).save()
        handle_reset(self.user, self.book1)
        self.assertFalse(CurrentlyReadingBook.objects.filter(book=self.book1, user=self.user).exists())

    def test_handle_reset_want_to_read(self):
        WantToReadBook(book=self.book2, user=self.user, add_date=datetime.now()).save()
        handle_reset(self.user, self.book2)
        self.assertFalse(WantToReadBook.objects.filter(book=self.book2, user=self.user).exists())

    def test_handle_reset_read(self):
        ReadBook(book=self.book2, user=self.user, read_date=datetime.now()).save()
        handle_reset(self.user, self.book2)
        self.assertFalse(ReadBook.objects.filter(book=self.book2, user=self.user).exists())

    def test_remove_review(self):
        BookReview(book=self.book2, review_user=self.user, review_date=datetime.now()).save()
        self.client.force_login(self.user)
        self.client.post(reverse('remove_review', kwargs={'slug': self.book2.slug}))
        self.assertFalse(BookReview.objects.filter(book=self.book2, review_user=self.user).exists())

