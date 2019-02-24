from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class User(AbstractUser):
    """ This is inherited from the AbstractUser class
    id
    password
    last_login
    is_superuser
    username
    first_name
    last_name
    email
    is_staff
    is_active
    date_joined
    """
    pass

class Idea(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=2048)
    owner = models.ForeignKey("User", related_name='ideas_owned', on_delete=models.CASCADE) #all ideas owned by a user will be deleted when that user is deleted.
    users = models.ManyToManyField("User", related_name='ideas_liked', verbose_name="users who are voting for this idea")
    board = models.ForeignKey('Board', related_name='ideas', on_delete=models.CASCADE) #all ideas on a board will be deleted when that board is deleted.
    alive = models.BooleanField(default=True)

class Board(models.Model):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey('User', related_name='boards', on_delete=models.CASCADE) #all boards owned by user will be deleted when that user is deleted.

class Vote(models.Model):
    idea = models.ForeignKey("Idea", related_name="votes", on_delete=models.CASCADE)
    user = models.ForeignKey("User", related_name="votes", on_delete=models.CASCADE)

class Chat(models.Model):
    idea = models.ForeignKey("Idea", related_name="chats", on_delete=models.CASCADE)
    user = models.ForeignKey("User", related_name="chats", on_delete=models.CASCADE)
    message = models.TextField()