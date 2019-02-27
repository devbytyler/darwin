from django.contrib.auth.models import User
from rest_framework import serializers

from darwin.models import Board, Idea, Vote

class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ('name', 'owner',)

class IdeaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Idea
        fields = ('title', 'description', 'owner', 'board', 'alive')

class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ('user', 'idea',)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ('username', 'password',)