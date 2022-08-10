from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.models import update_last_login


from .models import Post, Vote, Request

class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source = 'author.username')
    author_id = serializers.ReadOnlyField(source = 'author.id')
    votes = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'title', 'url', 'author', 'author_id', 'created', 'votes']

    def get_votes(self, post):
        return Vote.objects.filter(post=post).count()


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ['id', 'created']


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)
        token['username'] = user.username
        update_last_login(None, user)
        return token

