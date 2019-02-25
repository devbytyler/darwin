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
        user = User.objects.create_user(username='user', email='user@myroadmap.io', password='123', first_name='User', last_name='User')

        for i in range(100):
            Board.objects.create(name=f"Board {i}", owner=user)

        print('✅ Created seed data!')

