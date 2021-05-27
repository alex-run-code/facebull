from django.test import TestCase
from django.urls import include, path, reverse
from rest_framework.test import APITestCase, URLPatternsTestCase
from .models import User, Post, Like
from .factories import UserFactory
# Create your tests here.


class FacebullTests(APITestCase):
    def setUp(self):
        self.user = UserFactory(email='alexandre@mail.com', password='Password123!')
        user_credentials = {'email':self.user.email, 'password':'Password123!'}
        response = self.client.post(reverse('token_obtain_pair'), data=user_credentials)
        self.access_token = response.json()['access']

    def test_create_user(self):
        """
        A user should be created
        """
        new_user = {
            'email':'alex@gmail.com',
            'password':'123456Abc!',
            'first_name':'alexandre',
            'last_name':'jean',
        }
        response = self.client.post(reverse('signup'), new_user)
        user = User.objects.get(email=new_user['email'])
        self.assertEqual(response.status_code, 201)
        self.assertEqual(user.email, new_user['email'])

    def test_user_login(self):
        """
        User should receive a pair of token
        """
        user = UserFactory(email='user@mail.com', password='Password123!')
        user_credentials = {
            'email':'user@mail.com',
            'password':'Password123!'}
        response = self.client.post(reverse('token_obtain_pair'), data=user_credentials)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('refresh' in response.json().keys())
        self.assertTrue('access' in response.json().keys())

    def test_user_login_refresh(self):
        """
        The endpoint should returned a refreshed access token, but not another refresh token
        """
        user = UserFactory(email='user@mail.com', password='Password123!')
        user_credentials = {
            'email':'user@mail.com',
            'password':'Password123!'}
        response = self.client.post(reverse('token_obtain_pair'), data=user_credentials)
        refresh_token = response.json()['refresh']
        response_refresh = self.client.post(reverse('token_refresh'), {'refresh':refresh_token})
        self.assertEqual(response.status_code, 200)
        self.assertTrue('access' in response_refresh.json().keys())
        self.assertTrue('refresh' not in response_refresh.json().keys())

    def test_user_profile(self):
        """
        The endpoint should the user's data
        """
        user = UserFactory(email='user@mail.com', password='Password123!')
        user_credentials = {
            'email':'user@mail.com',
            'password':'Password123!'}
        response = self.client.post(reverse('token_obtain_pair'), data=user_credentials)
        access_token = response.json()['access']
        profile = self.client.get(reverse('profile'), HTTP_AUTHORIZATION='Bearer ' + access_token)
        self.assertEqual(profile.status_code, 200)
        self.assertEqual(len(profile.json().keys()), 5)

    def test_user_create_post(self):
        """
        A post should be created
        """
        user = UserFactory(email='user@mail.com', password='Password123!')
        user_credentials = {
            'email':'user@mail.com',
            'password':'Password123!'}
        response = self.client.post(reverse('token_obtain_pair'), data=user_credentials)
        access_token = response.json()['access']
        data = {'content':'This is my post.'}
        publish = self.client.post(reverse('publish'), data=data, HTTP_AUTHORIZATION='Bearer ' + access_token)
        self.assertEqual(len(Post.objects.filter(author=user)),1)
        self.assertEqual(publish.status_code, 201)

    def test_user_edit_post(self):
        """
        The post should be edited
        """
        initial_post = {'content':'This is the initial post.'}
        publish = self.client.post(reverse('publish'), data=initial_post, HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        self.assertEqual(publish.status_code, 201)

        edited_post = {'content':'This is the edited post.'}
        post_id = Post.objects.all().first().id
        edit = self.client.put(reverse('access', kwargs={'pk':post_id}), data=edited_post, HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        self.assertEqual(edit.status_code, 200)
        self.assertEqual(Post.objects.get(id=post_id).content, edited_post['content'])

    def test_user_delete_post(self):
        """
        The post should be deleted
        """
        initial_post = {'content':'This is the initial post.'}
        publish = self.client.post(reverse('publish'), data=initial_post, HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        self.assertEqual(publish.status_code, 201)

        post_id = Post.objects.all().first().id
        delete = self.client.delete(reverse('access', kwargs={'pk':post_id}), HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        self.assertEqual(delete.status_code, 204)
        self.assertEqual(len(Post.objects.all()),0)

    def test_user_like_post(self):
        """
        A like should be created with the right author 
        and for the right post
        """
        initial_post = {'content':'This is the initial post.'}
        publish = self.client.post(reverse('publish'), data=initial_post, HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        self.assertEqual(publish.status_code, 201)

        post_id = Post.objects.all().first().id
        like = self.client.post(reverse('like', kwargs={'post_id':post_id}), HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        like_obj = Like.objects.all().first()
        self.assertEqual(like.status_code, 201)
        self.assertEqual(like_obj.author, self.user)
        self.assertEqual(like_obj.post.id, post_id)

    def test_user_unlike_post(self):
        """
        The like should be deleted
        """
        initial_post = {'content':'This is the initial post.'}
        publish = self.client.post(reverse('publish'), data=initial_post, HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        self.assertEqual(publish.status_code, 201)

        post_id = Post.objects.all().first().id
        like = self.client.post(reverse('like', kwargs={'post_id':post_id}), HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        self.assertEqual(like.status_code, 201)
        self.assertEqual(len(Like.objects.all()), 1)

        unlike = self.client.delete(reverse('unlike', kwargs={'post_id':post_id}), HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        self.assertEqual(like.status_code, 201)
        self.assertEqual(len(Like.objects.all()), 0)