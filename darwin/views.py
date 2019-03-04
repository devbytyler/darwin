from django.contrib.auth.models import User, Group
from django.shortcuts import render
from rest_framework import status
from rest_framework import viewsets, generics
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import BoardSerializer, IdeaSerializer, UserSerializer, VoteSerializer
from .models import Board, Idea, User, Vote  

class BoardList(generics.ListCreateAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer

class BoardDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Board.objects.all()  
    serializer_class = BoardSerializer


@api_view(['GET'])
def user_boards(request, user_id):
    if request.method == 'GET':
        user_boards = Board.objects.filter(owner=user_id)
        serializer = BoardSerializer(user_boards, many=True)
        return Response(serializer.data)


@api_view(['GET', 'POST'])   
def ideas(request):
    if request.method == 'GET':
        ideas = Idea.objects.all()
        serializer = IdeaSerializer(ideas, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = IdeaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST','GET'])   
def users(request, user_id):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'GET':
        user = User.objects.filter(id=user_id)
        serializer = UserSerializer(user, many=True)
        return Response(serializer.data)
 
@api_view(['GET'])
def user_votes(request, user_id):
    if request.method == 'GET':
        user_votes = Vote.objects.filter(user_id=user_id)
        serializer = VoteSerializer(user_votes, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def idea_votes(request, idea_id):
    if request.method == 'GET':
        idea_votes = Vote.objects.filter(owner=idea_id)
        serializer = VoteSerializer(idea_votes, many=True)
        return Response(serializer.data)





# def home(request):
#     pass    

# def boards(request):
#     #returns JSON collection of boards
#     pass

# def add_board(request):
#     pass

# def board(request, pk):
#     pass

# def edit_board(request, pk):
#     pass

# def delete_board(request, pk):
#     pass

# def ideas(request):
#     pass

# def idea(request, board_id, pk):
#     pass

# def add_idea(request, board_id):
#     pass

# def edit_idea(request, board_id, pk):
#     pass

# def delete_idea(request, board_id, pk):
#     pass