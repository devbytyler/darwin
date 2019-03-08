from django.contrib.auth.models import User
from rest_framework import serializers

from darwin.models import Board, Idea, Vote, User

class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ('id', 'name', 'owner',)

class IdeaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Idea
        fields = ('id','title', 'description', 'owner', 'board', 'alive')

class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ('id','user', 'idea',)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'first_name', 'last_name', 'email', )