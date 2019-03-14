from django.contrib import admin
from .models import Board, Comment, Idea, User, Vote

admin.site.register(Board) 
admin.site.register(Comment) 
admin.site.register(Idea) 
admin.site.register(User) 
admin.site.register(Vote)