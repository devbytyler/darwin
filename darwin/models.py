from django.contrib.auth.models import AbstractUser
from django.db import models

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
    board = models.ForeignKey('Board', related_name='ideas', on_delete=models.CASCADE) #all ideas on a board will be deleted when that board is deleted.
    alive = models.BooleanField(default=True)

    def get_vote_count(self):
        return self.votes.all().count()


class Board(models.Model):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey('User', related_name='boards', on_delete=models.CASCADE) #all boards owned by user will be deleted when that user is deleted.
    code = models.CharField(max_length=20, null=True)
    is_voting = models.BooleanField(default=False)
    votes_per_user = models.IntegerField(default=3)         
    current_round = models.IntegerField(default=0)


class Vote(models.Model):
    idea = models.ForeignKey("Idea", related_name="votes", on_delete=models.CASCADE)
    user = models.ForeignKey("User", related_name="votes", on_delete=models.CASCADE)


class Comment(models.Model):
    idea = models.ForeignKey("Idea", related_name="comments", on_delete=models.CASCADE)
    user = models.ForeignKey("User", related_name="comments", on_delete=models.CASCADE)
    message = models.TextField()
    created = models.DateTimeField(auto_now=True)