from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import serializers, status
from rareapi.models import UserTypeChangeRequest, RareUser
from .rare_users import RareUserSerializer


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
        user_type_change_request.modified_user_id = RareUser.objects.get(pk=request.data["modified_user_id"])
        user_type_change_request.admin_one_id = RareUser.objects.get(pk=request.data["admin_one_id"])

        user_type_change_request.save()

        serializer = UserTypeChangeRequestSerializer(user_type_change_request, context={'request': request})

        return Response(serializer.data, status=status.HTTP_201_CREATED)


    def update(self, request, pk):
        user_type_change_request = UserTypeChangeRequest.objects.get(pk=pk)
        admin_one = RareUser.objects.get(pk=request.data["admin_one_id"])
        admin_two = RareUser.objects.get(pk=request.data["admin_two_id"])
        user_type_change_request.admin_one_id = admin_one
        user_type_change_request.admin_two_id = admin_two
        user_type_change_request.save()
        modified_user= RareUser.objects.get(pk=user_type_change_request.modified_user_id.id)

        if user_type_change_request.action == "promotion":
            modified_user.is_staff = True
            modified_user.save()
        elif user_type_change_request.action == "demotion":
            modified_user.is_staff = False
            modified_user.save()



        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        try:
            user_type_change_request = UserTypeChangeRequest.objects.get(pk=pk)
            user_type_change_request.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except UserTypeChangeRequest.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    @action(methods=['post'], detail=True)
    def promotion(self, request, pk=None):
        user_type_change_request = UserTypeChangeRequest.objects.get(pk=pk)
        admin_one = RareUser.objects.get(pk=request.data.get("admin_one_id"))
        modified_user = RareUser.objects.get(pk=user_type_change_request.modified_user_id.id)

        if user_type_change_request.action == "promotion" and admin_one.is_staff:
            user_type_change_request.modified_user_id = modified_user
            user_type_change_request.admin_one_id = admin_one
            user_type_change_request.save()

            response = UserTypeChangeRequestSerializer(user_type_change_request)
            return Response(response.data, status=status.HTTP_201_CREATED)
        else:
            return Response({"detail": "Only staff members can post promotions."}, status=status.HTTP_403_FORBIDDEN)

    @action(methods=['post'], detail=True)
    def approval(self, request, pk=None):
        try:
            admin_two = RareUser.objects.get(pk=request.data.get("admin_two_id"))
            user_type_change_request = UserTypeChangeRequest.objects.get(pk=pk)
            if user_type_change_request.action == "promotion" and user_type_change_request.admin_one_id:
                user_type_change_request.admin_two_id = admin_two
                user_type_change_request.save()
                modified_user= RareUser.objects.get(pk=user_type_change_request.modified_user_id.id)
                modified_user.is_staff = True
                modified_user.save()
        except UserTypeChangeRequest.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)


        rare_user_response = RareUserSerializer(modified_user).data
        user_type_change_response = UserTypeChangeRequestSerializer(user_type_change_request).data

        return Response({
            'rare_user': rare_user_response,
            'user_type_change': user_type_change_response
        }, status=status.HTTP_201_CREATED)

    @action(methods=['post'], detail=True)
    def demotion(self, request, pk=None):
        try:
            user_type_change_request = UserTypeChangeRequest.objects.get(pk=pk)
            modified_user_id = user_type_change_request.modified_user_id
            admin_one = RareUser.objects.get(pk=request.data.get("admin_one_id"))
            if user_type_change_request.action == "demotion":
                user_type_change_request.modified_user_id = modified_user_id
                user_type_change_request.admin_one_id = admin_one
                user_type_change_request.save()
        except UserTypeChangeRequest.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        response = UserTypeChangeRequestSerializer(user_type_change_request)
        return Response(response.data, status=status.HTTP_201_CREATED)

    @action(methods=['post'], detail=True)
    def confirmDemotion(self, request, pk=None):
        try:
            user_type_change_request = UserTypeChangeRequest.objects.get(pk=pk)
            if user_type_change_request.action == "demotion" and user_type_change_request.admin_one_id:
                admin_two = RareUser.objects.get(pk=request.data.get("admin_two_id"))
                user_type_change_request.admin_two_id = admin_two
                user_type_change_request.save()
                modified_user= RareUser.objects.get(pk=user_type_change_request.modified_user_id.id)
                modified_user.is_staff = False
                modified_user.save()
        except UserTypeChangeRequest.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)


        rare_user_response = RareUserSerializer(modified_user).data
        user_type_change_response = UserTypeChangeRequestSerializer(user_type_change_request).data

        return Response({
            'rare_user': rare_user_response,
            'user_type_change': user_type_change_response
        }, status=status.HTTP_201_CREATED)
