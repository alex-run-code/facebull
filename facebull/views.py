from django.shortcuts import render
from rest_framework import generics
from .models import User, Post, Like
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import UserSerializer, PostSerializer, LikeSerializer
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from .permissions import IsAuthorOrReadOnly
from django.shortcuts import get_object_or_404
# Create your views here.


class SignUp(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer


class Profile(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        content = {
            'email': str(request.user.email),
            'first_name': str(request.user.first_name),
            'last_name': str(request.user.first_name),
            'ip_joined': str(request.user.ip_joined),
            'holiday': str(request.user.holiday),
        }
        return Response(content)


class Publish(generics.CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer


class AccessPost(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthorOrReadOnly]
    serializer_class = PostSerializer
    queryset = Post.objects.all()


class LikePost(generics.CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = LikeSerializer
    queryset = Like.objects.all()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['post_id'] = self.kwargs['post_id']
        return context


class UnlikePost(generics.DestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = LikeSerializer()
    queryset = Like.objects.all()

    def get_object(self):
        queryset = self.get_queryset()
        like = get_object_or_404(queryset, author=self.request.user, post=self.kwargs['post_id'])
        return like

