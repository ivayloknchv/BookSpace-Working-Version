from django.core.management.base import BaseCommand
from books_database.models import Book, Genre, Author
import pandas as pd


class Command(BaseCommand):
    help = 'Import books and genres from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file')

    def handle(self, *args, **options):
        csv_file = options['csv_file']
        self.import_from_csv(csv_file)

    def import_from_csv(self, csv_file):
        df = pd.read_csv(csv_file)

        for idx, row in df.iterrows():

            title = row['book_title']
            author = row['author']
            cover_url = row['cover_image_uri']
            genres = [genre.strip().strip("'") for genre in row['genres'][1:-1].split(',')]
            description = row['book_details']

            author_model, author_created = Author.objects.get_or_create(name=author)

            book, created_flag = Book.objects.get_or_create(
                title=title,
                defaults={'author' : author_model, 'cover_url': cover_url, 'description' : description}
            )


            for genre in genres:
                category_model, category_created = Genre.objects.get_or_create(name=genre)
                book.genres.add(category_model)


            book.save()
            self.stdout.write(f"Processed book: {title} by {author}")