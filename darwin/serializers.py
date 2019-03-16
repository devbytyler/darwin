from django.contrib.auth.models import User
from rest_framework import serializers

from darwin.models import Board, Idea, Vote, User, Comment

class BoardModelSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Board
        fields = ('id', 'name', 'owner',)


class CommentModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('user', 'idea', 'message')


class IdeaModelSerializer(serializers.ModelSerializer):
    comments = CommentModelSerializer(many=True,read_only=True)
    total_votes = serializers.SerializerMethodField()
    owner = serializers.PrimaryKeyRelatedField(read_only=True)
    alive = serializers.BooleanField(read_only=True)

    class Meta:
        model = Idea
        fields = ('id','title', 'description', 'owner', 'board', 'alive', 'total_votes', 'comments',)

    def get_total_votes(self, obj):
        return obj.get_vote_count()


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

