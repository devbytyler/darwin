from django.contrib.auth.models import User, Group
from django.shortcuts import render
from rest_framework import viewsets, generics
from .serializers import BoardSerializer

from .models import Board

class BoardList(generics.ListCreateAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer

class BoardDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer

def home(request):
    pass

def boards(request):
    #returns JSON collection of boards
    pass

def add_board(request):
    pass

def board(request, pk):
    pass

def edit_board(request, pk):
    pass

def delete_board(request, pk):
    pass

def ideas(request):
    pass

def idea(request, board_id, pk):
    pass

def add_idea(request, board_id):
    pass

def edit_idea(request, board_id, pk):
    pass

def delete_idea(request, board_id, pk):
    pass