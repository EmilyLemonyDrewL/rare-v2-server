from django.http import HttpResponseServerError
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rareapi.models import Comment, Post, RareUser
from .rare_users import RareUserSerializer

class CommentView(ViewSet):

    def retrieve(self, request, pk):
        try:
            comment = Comment.objects.get(pk=pk)
            serializer = CommentSerializer(comment)
            return Response(serializer.data)
        except comment.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        post_id = request.query_params.get('post_id', None)
        if post_id is not None:
            comments = Comment.objects.filter(post_id=post_id)
        else:
            comments = Comment.objects.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    def create(self, request):

        author = RareUser.objects.get(pk=request.data['rare_user_id'])
        post = Post.objects.get(pk=request.data['post_id'])

        comment = Comment.objects.create(
            author = author,
            post=post,
            content = request.data['content'],
        )

        serializer = CommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        comment = Comment.objects.get(pk=pk)
        comment.content = request.data['content']
        comment.save()

        serializer = CommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, pk):
        comment = Comment.objects.get(pk=pk)
        comment.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

class CommentSerializer(serializers.ModelSerializer):
    author = RareUserSerializer()
    class Meta:
        model = Comment
        fields = ('id', 'post', 'author', 'post', 'content', 'created_on')
        read_only_fields = ['created_on']
