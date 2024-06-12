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

class RareUserView(ViewSet):
    """
    All the User Views
    """

    def retrieve(self, request, pk):
        """
        Function to get a single user
        """
        try:
            user = RareUser.objects.get(pk=pk)
        except RareUser.DoesNotExist:
            return Response("")
        
        serializer = RareUserSerializer(user)
        return Response(serializer.data)

    def create(self, request):
        """
        function to create a new user
        """
        user = RareUser.objects.create(
            first_name = request.data["first_name"],
            last_name = request.data["last_name"],
            bio = request.data["bio"],
            profile_image_url = request.data["profile_image_url"],
            email = request.data["email"],
            active = True,
            is_staff = False,
            uid = request.data["uid"]
        )
        serializer = RareUserSerializer(user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, pk):
        """
        function to update a user
        """

        user = RareUser.objects.get(pk=pk)
        user.first_name = request.data["first_name"]
        user.last_name = request.data["last_name"]
        user.bio = request.data["bio"]
        user.profile_image_url = request.data["profile_image_url"]
        user.email = request.data["email"]
        user.active = True
        user.is_staff = request.data["is_staff"]
        user.uid = request.data["uid"]
        user.save()


        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def destroy(self, request, pk):
        """
        function to delete a user
        """
        user = RareUser.objects.get(pk=pk)
        user.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)