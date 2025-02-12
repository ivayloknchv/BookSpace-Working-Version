from datetime import datetime
from django.db import models
from django.db import IntegrityError
from django.test import TestCase
from users.models import User
from .models import (Book, Genre, Author, WantToReadBook,
                     CurrentlyReadingBook, ReadBook, BookReview)


class TestGenreModel(TestCase):

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


class TestAuthorModel(TestCase):

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


class TestBookModel(TestCase):

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
        self.assertEqual(', '.join((str(genre) for genre in self.book.genres.all())),
                         'My Genre 1, My Genre 2')

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


class TestWantToReadBookModel(TestCase):

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


class TestCurrentlyReadingBook(TestCase):

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
        currently_reading = WantToReadBook(book=self.book, user=self.user, add_date=datetime.now())
        currently_reading.save()
        self.assertTrue(isinstance(currently_reading, WantToReadBook))
        self.assertTrue(isinstance(currently_reading, models.Model))
        self.assertFalse(isinstance(currently_reading, CurrentlyReadingBook))


class TestReadBook(TestCase):

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

    def test_read_book_creation(self):
        read = ReadBook(book=self.book, user=self.user, read_date=datetime.now())
        read.save()
        self.assertTrue(isinstance(read, ReadBook))
        self.assertTrue(isinstance(read, models.Model))
        self.assertFalse(isinstance(read, WantToReadBook))


class TestBookReview(TestCase):

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

    def test_book_review_creation(self):
        review = BookReview(book=self.book, review_user=self.user, review_score=5, review_date=datetime.now())
        review.save()
        self.assertTrue(isinstance(review, BookReview))
        self.assertEqual(review.review_score, 5)
        self.assertEqual(str(review.review_user), 'user')

