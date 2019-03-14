from django.contrib.auth.models import User
from rest_framework import serializers

from darwin.models import Board, Idea, Vote, User, Chat

class BoardModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ('id', 'name', 'owner',)

class ChatModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('owner', 'body')

class IdeaModelSerializer(serializers.ModelSerializer):
    comments = ChatModelSerializer(many=True,read_only=True)
    class Meta:
        model = Idea
        fields = ('id','title', 'description', 'owner', 'board', 'alive','comments')


class VoteModelSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(required=False, queryset=User.objects.all())

    class Meta:
        model = Vote
        fields = ('id','user', 'idea',)


class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'first_name', 'last_name', 'email', )

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

