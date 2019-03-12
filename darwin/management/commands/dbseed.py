# import datetime
import random

from django.core.management.base import BaseCommand

from faker import Faker

from darwin.models import Board, Idea, User, Vote

class Command(BaseCommand):
    help = 'Seed the datas'

    def handle(self, *args, **options):
        fake = Faker()
        print('Creating users...')
        super_user = User.objects.create_superuser(username='super', email='super@darwin.io', password='123', first_name='Super', last_name='User')
        
        for i in range(10):
            User.objects.create_user(username=f'user{i}', email=fake.email(), password='123', first_name=fake.first_name())

        for i in range(12):
            Board.objects.create(name=fake.word(), owner_id=random.randint(1,10))

        for i in range(50):
            Idea.objects.create(title=fake.sentence(nb_words=6), description=fake.paragraph(), owner_id=random.randint(1,10), board_id=random.randint(1,12))
        print('✅ Created seed data!')

