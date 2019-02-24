from django.contrib import admin
from .models import Board, Chat, Idea, User, Vote

admin.site.register(Board) 
admin.site.register(Chat) 
admin.site.register(Idea) 
admin.site.register(User) 
admin.site.register(Vote)