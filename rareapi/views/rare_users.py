from rest_framework import serializers
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from rareapi.models import RareUser


class RareUserSerializer(serializers.ModelSerializer):
    """
    JSON Serializer for Rare Users
    """
    class Meta:
        model = RareUser
        fields = ("first_name", "last_name", "bio", "profile_image_url", "email", "created_on", "active", "is_staff", "uid")

class RareUserView:
    """
    All the User Views
    """

    def retrieve(self, request, pk):
        """
        function to get single user
        """
        user = RareUser.objects.get(pk=pk)
        serializer = RareUserSerializer(user)
        return Response(serializer.data)

    def create(self, request):
        """
        function to create a new user
        """
        