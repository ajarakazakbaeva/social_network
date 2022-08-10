import json
from datetime import datetime, timedelta

from rest_framework import generics, permissions, mixins, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import Post, Vote, Request
from .serializers import PostSerializer, VoteSerializer, MyTokenObtainPairSerializer



class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


# class VoteList(generics.ListAPIView):
#     serializer_class = VoteSerializer
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly]
#
#
#     def get_queryset(self):
#         queryset = Vote.objects.all()
#         start = self.request.query_params.get('start')
#         if start is not None:
#             start_date = datetime.strptime(start, '%m-%d-%Y').date()
#             queryset = queryset.filter(created__gte=start_date)
#         return queryset


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def analytics(request):
    number_of_votes = {}
    queryset = Vote.objects.all()
    start = request.query_params.get('start')
    end = request.query_params.get('end')
    if start is not None and start!='' and end is not None and end!='':
        start_date = datetime.strptime(start, '%d-%m-%Y').date()
        end_date = datetime.strptime(end, '%d-%m-%Y').date()
        if start_date<end_date:
            date = start_date
            while date<=end_date:
                number_of_votes[str(date)]=queryset.filter(created__gte=date, created__lte=date+timedelta(days=1)).count()
                date+= timedelta(days=1)
        else:
            raise ValidationError('Start date should be earlier than end date ')
    else:
        raise ValidationError('Please, provide start and end dates for votes analytics')
    return Response(number_of_votes)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_analytics(request):
    user_data = {}
    user = request.user
    user_data['username'] = user.username
    user_data['last_login_date'] = user.last_login
    user_activity = Request.objects.filter(user=user).latest('id')
    user_data['last_activity_endpoint'] = user_activity.endpoint
    user_data['last_activity_date'] = user_activity.created_at
    return Response(user_data)


class PostRetrieveDestroy(generics.RetrieveDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        post = Post.objects.filter(pk = kwargs['pk'], author=self.request.user)
        if post.exists():
            return self.destroy(request, *args, **kwargs)
        else:
            raise ValidationError('You do not have a permission to delete this post :) ')


class VoteCreate(generics.CreateAPIView, mixins.DestroyModelMixin):
    serializer_class = VoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        post = Post.objects.get(pk=self.kwargs['pk'])
        return Vote.objects.filter(voter=user, post=post)

    def perform_create(self, serializer):
        if self.get_queryset().exists():
            raise ValidationError('You have already voted for this post :) ')
        else:
            serializer.save(created = datetime.now(), voter=self.request.user, post=Post.objects.get(pk=self.kwargs['pk']))

    def delete(self, request, *args, **kwargs):
        if self.get_queryset().exists():
            self.get_queryset().delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            raise ValidationError('You never voted for this post :) ')


class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer


