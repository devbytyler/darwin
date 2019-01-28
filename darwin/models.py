from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class User(AbstractUser):
    """ This comes from the AbstractUser class
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