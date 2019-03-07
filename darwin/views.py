from django.contrib.auth.models import User, Group
from django.shortcuts import render
from rest_framework import viewsets, generics, status     
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.authtoken import views

from .serializers import BoardSerializer, IdeaSerializer, UserSerializer, VoteSerializer
from .models import Board, Idea, User, Vote

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'boards': reverse('boards', request=request, format=format),
        'ideas': reverse('ideas', request=request, format=format),
        'users': reverse('users', request=request, format=format),
    })

class BoardList(generics.ListCreateAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class BoardDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Board.objects.all()  
    serializer_class = BoardSerializer

class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()   
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user': UserSerializer(user).data,
        })

@api_view(['GET'])
def user_boards(request, user_id):
    if request.method == 'GET':
        user_boards = Board.objects.filter(owner=user_id)
        serializer = BoardSerializer(user_boards, many=True)
        return Response(serializer.data)


@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticatedOrReadOnly, ))
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
def user(request, user_id):
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
def user_ideas(request, idea_id):
    if request.method == 'GET':
        user_ideas = Idea.objects.filter(id=idea_id)
        serializer = IdeaSerializer(user_ideas, many=True)
        return Response(serializer.data)