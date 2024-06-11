from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rareapi.models import UserTypeChangeRequest, RareUser

class UserTypeChangeRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTypeChangeRequest
        fields = ('id', 'action', 'admin_one_id', 'admin_two_id', 'modified_user_id')

class UserTypeChangeRequestsView(ViewSet):
    def list(self, request):
        user_type_change_requests = UserTypeChangeRequest.objects.all()
        serializer = UserTypeChangeRequestSerializer(user_type_change_requests, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        try:
            user_type_change_request = UserTypeChangeRequest.objects.get(pk=pk)
            serializer = UserTypeChangeRequestSerializer(user_type_change_request)
            return Response(serializer.data)
        except UserTypeChangeRequest.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        user_type_change_request = UserTypeChangeRequest()
        user_type_change_request.action = request.data["action"]
        user_type_change_request.admin_one_id = RareUser.objects.get(pk=request.data["admin_one_id"])
        user_type_change_request.admin_two_id = RareUser.objects.get(pk=request.data["admin_two_id"])
        user_type_change_request.modified_user_id = RareUser.objects.get(pk=request.data["modified_user_id"])

        user_type_change_request.save()

        serializer = UserTypeChangeRequestSerializer(user_type_change_request, context={'request': request})

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        user_type_change_request = UserTypeChangeRequest.objects.get(pk=pk)
        user_type_change_request.action = request.data["action"]
        user_type_change_request.admin_one_id = RareUser.objects.get(pk=request.data["admin_one_id"])
        user_type_change_request.admin_two_id = RareUser.objects.get(pk=request.data["admin_two_id"])
        user_type_change_request.modified_user_id = RareUser.objects.get(pk=request.data["modified_user_id"])

        user_type_change_request.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        try:
            user_type_change_request = UserTypeChangeRequest.objects.get(pk=pk)
            user_type_change_request.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except UserTypeChangeRequest.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
