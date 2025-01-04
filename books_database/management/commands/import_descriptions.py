from django.core.management.base import BaseCommand

from books_database.models import Book, Genre, Author
import pandas as pd


class Command(BaseCommand):
    help = 'Import books and genres from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file')

    def handle(self, *args, **options):
        csv_file = options['csv_file']
        self.import_descriptions(csv_file)

    def import_descriptions(self, csv_file):
        df = pd.read_csv(csv_file)
        for idx, row in df.iterrows():
            title = row['book_title']
            description = row['book_details']

            if Book.objects.filter(title=title).exists():
                book = Book.objects.get(title=title)
                if book.description == 'No description':
                    book.description = description
                    book.save()
                    self.stdout.write(f"Processed book: {title}")