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
        """
        function to create a subscription
        """

        follower = RareUser.objects.get(uid=request.data["uid"])
        
        sub = Subscription.objects.create(
            follower = follower,
            author = RareUser.objects.get(author_id=request.data["author_id"])
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

            posts_of_sub = Post.objects.filter(rare_user=author)

            serialzed_author = RareUserSerializer(author)
            serializer = PostSerializer(posts_of_sub, many=True)

            authors.append(serialzed_author)
            posts.append(serializer)

        return Response({'posts': posts, 'authors': authors})
    
    def destroy(self, request, pk):
        """
        function to delete a subscription
        """
        sub = Subscription.objects.get(pk=pk)
        sub.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=False, methods=['GET'], url_path='is_subscribed')
    def is_subscribed(self, request):
        """
        Check if the follower is subscribed to the author
        """
        uid = request.query_params.get('uid')
        author_id = request.query_params.get('author_id')

        if not uid or not author_id:
            return Response({"message": "uid and author_id are required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            follower = RareUser.objects.get(uid=uid)
            author = RareUser.objects.get(pk=author_id)
            
        except RareUser.DoesNotExist:
            return Response({"message": "Follower does not exist"}, status=status.HTTP_404_NOT_FOUND)

        print("follower id: ", follower.id)
        # print(subscription)

        try:
            Subscription.objects.get(follower=follower, author_id=author_id)
            # subscription = Subscription.objects.get(follower=follower)
            is_subscribed = True
        except Subscription.DoesNotExist:
            is_subscribed = False

        return Response({"is_subscribed": is_subscribed}, status=status.HTTP_200_OK)

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