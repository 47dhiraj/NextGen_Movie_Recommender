from time import sleep

from django.core.management import call_command
from django.core.management.base import BaseCommand
from tqdm import tqdm


class Command(BaseCommand):

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Creating Table, could take upto 5 min'))
        call_command('makemigrations')
        call_command('migrate')
        self.stdout.write(self.style.SUCCESS('Table created successfully'))
        self.stdout.write(self.style.SUCCESS('Running Basic Setup'))

        call_command('loaddata', 'movie_admin/fixtures/User.json')
        call_command('loaddata', 'movie_admin/fixtures/Movies.json')
        call_command('loaddata', 'movie_admin/fixtures/DjangoSite.json')
        call_command('loaddata', 'movie_admin/fixtures/SocialApp.json')

        progress_bar = tqdm(desc='Processing', total=100, bar_format='{l_bar}{bar:40}{r_bar}{bar:10b}', colour='green')
        progress_bar.update(100)

        progress_bar.close()

        self.stdout.write(self.style.SUCCESS('Data added successfully'))
