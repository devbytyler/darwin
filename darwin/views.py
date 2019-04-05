from django.contrib.auth.models import User, Group
from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, generics, status, serializers  
from rest_framework.authtoken import views
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.response import Response
from rest_framework.reverse import reverse

from .serializers import BoardModelSerializer, IdeaModelSerializer, UserModelSerializer, VoteModelSerializer, CommentModelSerializer
from .models import Board, Idea, User, Vote, Comment


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'boards': reverse('boards', request=request, format=format),
        'ideas': reverse('ideas', request=request, format=format),
        'users': reverse('users', request=request, format=format),
        'votes': reverse('votes', request=request, format=format),
    })


class Login(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user': UserModelSerializer(user).data,
        })


@api_view(['POST'])
@permission_classes((AllowAny, ))
def register(request):
    serializer = UserModelSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user': UserModelSerializer(user).data,
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BoardList(generics.ListCreateAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardModelSerializer

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        board = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        ideas = Idea.objects.filter(board=board)
        idea_serializer = IdeaModelSerializer(ideas, context={'request': request}, many=True)
        votes_remaining = board.votes_per_user - Vote.objects.filter(user=request.user, idea__in=ideas).count()

        return Response({
            "id": board.id,
            "name": board.name,
            "owner": board.owner.id,
            "votes_remaining": votes_remaining,
            "is_owner": True if request.user == board.owner else False,
            "ideas": idea_serializer.data,
        }, status=status.HTTP_201_CREATED, headers=headers)


class BoardDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Board.objects.all()  
    serializer_class = BoardModelSerializer


# @api_view(['GET', 'POST'])
# def ideas(request):
#     if request.method == 'GET':
#         ideas = Idea.objects.all()
#         serializer = IdeaSerializer(ideas, many=True)
#         return Response(serializer.data)
#     elif request.method == 'POST':
#         serializer = IdeaSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class IdeaList(generics.ListCreateAPIView):
    queryset = Idea.objects.all()
    serializer_class = IdeaModelSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class IdeaDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Idea.objects.all()  
    serializer_class = IdeaModelSerializer


class VoteList(generics.ListAPIView):
    queryset = Vote.objects.all()
    serializer_class = VoteModelSerializer


class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()   
    serializer_class = UserModelSerializer


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserModelSerializer


class CommentsList(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentModelSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@api_view(['GET'])
def user_boards(request, user_id):
    if request.method == 'GET':
        user_boards = Board.objects.filter(owner=user_id)
        serializer = BoardModelSerializer(user_boards, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def user_ideas(request, idea_id):
    if request.method == 'GET':
        user_ideas = Idea.objects.filter(id=idea_id)
        serializer = IdeaModelSerializer(user_ideas, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def user_votes(request, user_id):
    if request.method == 'GET':
        user_votes = Vote.objects.filter(user_id=user_id)
        serializer = VoteModelSerializer(user_votes, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def board_page(request, board_id):
    board = Board.objects.filter(id=board_id).first()
    ideas = Idea.objects.filter(board=board)
    idea_serializer = IdeaModelSerializer(ideas, context={'request': request}, many=True)
    votes_remaining = board.votes_per_user - Vote.objects.filter(user=request.user, idea__in=ideas).count()

    return Response({
        "id": board.id,
        "name": board.name,
        "owner": board.owner.id,
        "is_voting": board.is_voting,
        "current_round":board.current_round,
        "votes_remaining": votes_remaining,
        "is_owner": True if request.user == board.owner else False,
        "ideas": idea_serializer.data,
    })
    
@api_view(['POST'])
def cast_vote(request):
    serializer = VoteModelSerializer(data=request.data)
    idea_id = request.data['idea']
    existing_vote = Vote.objects.filter(idea_id=idea_id, user=request.user)
    if existing_vote:
        existing_vote.delete()
        return Response({'removed': True}, status=status.HTTP_200_OK)
    if serializer.is_valid():   
        vote = serializer.save(user=request.user)
        return Response({'id': vote.id}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
def end_round(request, board_id):
    board = Board.objects.filter(id=board_id).first()
    board.is_voting = False
    board.save()

    cutoff = request.data["cutoff"]
    ideas = Idea.objects.filter(board_id=board_id)
    idea_index_to_num_votes= {}
    for i, idea in enumerate(ideas):
        idea_index_to_num_votes[i] = idea.get_vote_count()
    ideas_to_kill = {k:v for k,v in idea_index_to_num_votes.items() if v < cutoff}
    for k,v in ideas_to_kill.items():
       ideas[k].alive = False 
       ideas[k].save()
    Vote.objects.filter(idea__board=board).delete()

    return Response({}, status=status.HTTP_200_OK)

@api_view(['POST'])
def start_round(request, board_id):
    board = Board.objects.filter(id=board_id).first()
    board.is_voting = True
    board.current_round += 1
    board.votes_per_user = request.data['round_votes']
    board.save()

    return Response({}, status=status.HTTP_200_OK)

