from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rareapi.models import Post, Category, PostTag, Tag, RareUser

class PostView(ViewSet):

    def retrieve(self, request, pk):
        try: 
            post = Post.objects.get(pk=pk)
            serializer = PostSerializer(post)
            return Response(serializer.data)
        except Post.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        try:
            rare_user =  request.query_params.get('uid', None)
            if rare_user is not None:
                rare_user_id = RareUser.objects.get(uid = rare_user)
                posts = Post.objects.filter(rare_user = rare_user_id)
            else:
                posts = Post.objects.all()
            
            serializer = PostSerializer(posts, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({'message': f'An error occurred: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def create(self, request):
        rare_user = RareUser.objects.get(uid=request.data["uid"])
        category = Category.objects.get(pk=request.data["category"])

        post = Post.objects.create(
            rare_user = rare_user,
            title = request.data["title"],
            publication_date = request.data["publicationDate"],
            image_url = request.data["image_url"],
            content = request.data["content"],
            category = category,
            approved = False
        )
        for tag_id in request.data["tags"]:
                
            tag = Tag.objects.get(pk=tag_id)
            PostTag.objects.create(
                post = post,
                tag = tag
            )
        
        serializer = PostSerializer(post)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        
    def update(self, request, pk):
        post = Post.objects.get(pk=pk)
        category = Category.objects.get(pk=request.data["category"])
        post.title = request.data["title"]
        post.image_url = request.data["image_url"]
        post.content = request.data["content"]
        post.category = category
        
        post_tags = PostTag.objects.filter(post_id = post.id)
        for tag in post_tags:
            tag.delete()
            
        post.save()
        
        for tag_id in request.data["tags"]:
                
            tag = Tag.objects.get(pk=tag_id)
            PostTag.objects.create(
                post = post,
                tag = tag
            )
        
        serializer = PostSerializer(post)
        return Response(serializer.data, status=status.HTTP_200_OK)
      
    def destroy(self, request, pk):
        post = Post.objects.get(pk=pk)
        post.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
        
class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'rare_user_id', 'rare_user', 'category', 'title', 'publication_date', 'image_url', 'content', 'approved', 'tags')
        depth = 2
