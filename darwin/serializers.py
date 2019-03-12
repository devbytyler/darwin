from django.contrib.auth.models import User
from rest_framework import serializers

from darwin.models import Board, Idea, Vote, User

class BoardModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ('id', 'name', 'owner',)

class IdeaModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Idea
        fields = ('id','title', 'description', 'owner', 'board', 'alive')

class VoteModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ('id','user', 'idea',)

class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'first_name', 'last_name', 'email', )



