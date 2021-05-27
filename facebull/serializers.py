from rest_framework import serializers
from .models import User, Post, Like
from .tasks import enrich_user_task

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            email=validated_data['email'], # what's validated data doing ? 
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )
        user.set_password(validated_data['password'])
        user.save()
        enrich_user_task.delay(user.email)
        return user

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['content']

    def create(self, validated_data):
        post = Post(
            author=self.context['request'].user,
            content=validated_data['content']
        )
        post.save()
        return post

class LikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Like
        fields = []
    
    def create(self, validated_data):
        like = Like(
            author=self.context['request'].user,
            post=Post.objects.get(id=self.context['post_id']),
        )
        like.save()
        return like
    
    def to_representation(self, instance):
        return {
            'author': instance.author.email,
            'post': instance.post.id
        }