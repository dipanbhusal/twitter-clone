from django.contrib.auth import get_user_model
from django.http import response

from django.test import TestCase
from rest_framework.test import APIClient

from .models import Tweet
# Create your tests here.

User = get_user_model()
class TweetTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username = "dpn", password = "randompassword")
        self.user2 = User.objects.create_user(username = "dpn-2", password = "randompassword")
        Tweet.objects.create(content = "This is first test tweet", user  = self.user)
        Tweet.objects.create(content = "This is second test tweet", user  = self.user)
        Tweet.objects.create(content = "This is third test tweet", user  = self.user2)
    
    def test_tweet_created(self):
        tweet_obj = Tweet.objects.create(content = "This is fourth test tweet", user  = self.user)
        self.assertEqual(tweet_obj.id, 4)
        self.assertEqual(tweet_obj.user, self.user)

    def get_client(self):
        client = APIClient()
        client.login(username = self.user.username , password = "randompassword")
        return client 

    def test_tweet_list(self):
        client = self.get_client()
        response = client.get("/api/tweets/")
        self.assertEqual(response.status_code, 200)
    
    def test_tweet_detail_api_view(self):
        client = self.get_client()
        response = client.get('/api/tweets/1/')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        _id = data.get('id')
        self.assertEqual(_id, 1)

    def test_tweet_action_like(self):
        client = self.get_client()
        response = client.post("/api/tweets/action/", {"id" : 1, "action":"like"})
        self.assertEqual(response.status_code, 200)

    
    
    def test_tweet_delete_api_view(self):
        client = self.get_client()
        response = client.delete('/api/tweets/1/delete/')
        self.assertEqual(response.status_code, 200)
        response_not_owner = client.delete('/api/tweets/3/delete/')
        self.assertEqual(response_not_owner.status_code, 401)

    