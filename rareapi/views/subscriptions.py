from rest_framework import serializers
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from rareapi.models import Subscription, RareUser
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
        author = RareUser.objects.get(pk=request.data["author_id"])
        )
        serliazer = SubscriptionSerializer(sub)
        return Response(serliazer.data, status=status.HTTP_201_CREATED)
    
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
        follower_id = request.query_params.get('follower_id')
        author_id = request.query_params.get('author_id')
        
        if not follower_id or not author_id:
            return Response({"message": "follower_id and author_id are required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            Subscription.objects.get(follower_id=follower_id, author_id=author_id)
            is_subscribed = True
        except Subscription.DoesNotExist:
            is_subscribed = False

        return Response({"is_subscribed": is_subscribed}, status=status.HTTP_200_OK)

