from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rareapi.models import Post, Category, PostTag, Tag

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
    
    def list_by_user(self, request, pk):
        rare_user_id = Post.objects.get(pk=request.data["uid"])
        posts = Post.objects.all(rare_user_id)
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    def create(self, request):
        rare_user = Post.objects.get(pk=request.data["uid"])
        
        post = Post.objects.create(
            rare_user = rare_user,
            title = request.data["title"],
            publication_date = request.data["publicationDate"],
            image_url = request.data["imageUrl"],
            content = request.data["content"],
            approved = False
        )
        post.save()
        
        # for category in request.data.get("categories", []):
        #         add_category = Ca
        
        for tag_id in request.data.get("tags", []):
            add_tag = Tag.objects.get(pk=tag_id)
            PostTag.objects.create(post=post, tag=add_tag)
        
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
        fields = ('id', 'rare_user_id', 'category_id', 'title', 'publication_date', 'image_url', 'content', 'approved', 'tags')
        depth = 1
