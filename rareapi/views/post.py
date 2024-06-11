from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rareapi.models import Post

class PostView(ViewSet):

    def retrieve(self, request, pk):
        try: 
            post = Post.objects.get(pk=pk)
            serializer = PostSerializer(post)
            return Response(serializer.data)
        except Post.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
      
    def create(self, request):
        rare_user = Post.objects.get(pk=request.data["rare_user_id"])
        
        post = Post.objects.create(
            rare_user = rare_user,
            title = request.data["title"],
            publication_date = request.data["publicationDate"],
            image_url = request.data["imageUrl"],
            content = request.data["content"],
            approved = False
        )
        post.save()
        serializer = PostSerializer(post)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        
    def update(self, request, pk):
        post = Post.objects.get(pk=pk)
        post.title = request.data["title"]
        post.publication_date = request.data["publicationDate"]
        post.image_url = request.data["imageUrl"]
        post.content = request.data["content"]
        
        serializer = PostSerializer(post)
        return Response(serializer.data, status=status.HTTP_200_OK)
      
    def destroy(self, request, pk):
        post = Post.objects.get(pk=pk)
        post.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
              
class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model: Post
        fields = ('id', 'rare_user_id', 'category_id', 'title', 'publication_date', 'image_url', 'content', 'approved')
        depth = 1
