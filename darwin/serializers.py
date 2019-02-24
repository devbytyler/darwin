from django.contrib.auth.models import User
from rest_framework import serializers

from darwin.models import Board

class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ('name', 'owner',)
