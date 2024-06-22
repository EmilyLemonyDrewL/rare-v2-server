from rest_framework import serializers
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from rareapi.models import Subscription, RareUser, Post
from rest_framework.decorators import action

class SubscriptionSerializer(serializers.ModelSerializer):
    """
    serializer for subscription
    """
    class Meta:
        model = Subscription
        fields = ("follower", "author", "created_on")

class SubscriptionView(ViewSet):

    def create(self, request):
        follower = RareUser.objects.get(uid=request.data["uid"])
        author = RareUser.objects.get(pk=request.data["author_id"])
        
        sub = Subscription.objects.create(
            follower = follower,
            author = author
        )
        
        serliazer = SubscriptionSerializer(sub)
        return Response(serliazer.data, status=status.HTTP_201_CREATED)
    
    def list(self, request):
        follower = RareUser.objects.get(uid=request.data["uid"])
        subscriptions = Subscription.objects.filter(follower=follower)

        posts = []
        authors = []

        for sub in subscriptions:
            
            author = RareUser.objects.get(uid=sub.author_id)
            posts_of_author = Post.objects.filter(rare_user=author)

            serialzed_author = RareUserSerializer(author)
            serializer_posts = PostSerializer(posts_of_author, many=True)

            authors.append(serialzed_author)
            posts.append(serializer_posts)

        return Response({'posts': posts, 'authors': authors})
    
    @action(detail=False, methods=['post'])
    def is_subscribed(self, request):
        """
        Check if the follower is subscribed to the author
        """

        author = RareUser.objects.get(pk=request.data["author_id"])
        follower = RareUser.objects.get(uid=request.data["uid"])

        if Subscription.objects.filter(follower=follower, author=author).exists():
            is_subscribed = True
        else:
            is_subscribed = False

        return Response({"is_subscribed": is_subscribed}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def delete_sub(self, request):
        
        follower = RareUser.objects.get(uid=request.data["uid"])
        author = RareUser.objects.get(pk=request.data["author_id"])
        
        sub = Subscription.objects.filter(author=author, follower=follower)
        sub.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

class PostSerializer(serializers.ModelSerializer):
    comment_count = serializers.IntegerField(default=None)
    class Meta:
        model = Post
        fields = ('id', 'rare_user_id', 'rare_user', 'category', 'title', 'publication_date', 'image_url', 'content', 'approved', 'tags', 'comment_count')
        depth = 2

class RareUserSerializer(serializers.ModelSerializer):
    """
    JSON Serializer for Rare Users
    """
    class Meta:
        model = RareUser
        fields = ("id", "first_name", "last_name", "bio", "profile_image_url", "email", "created_on", "active", "is_staff", "uid")