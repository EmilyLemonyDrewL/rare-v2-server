from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rareapi.models import Post, Category, PostTag, Tag, RareUser, Comment
from .comments import CommentSerializer
from rest_framework.decorators import action
from django.db.models import Count

class PostSerializer(serializers.ModelSerializer):
    comment_count = serializers.IntegerField(default=None)
    class Meta:
        model = Post
        fields = ('id', 'rare_user_id', 'rare_user', 'category', 'title', 'publication_date', 'image_url', 'content', 'approved', 'tags', 'comment_count')
        depth = 2


class PostView(ViewSet):
    
    def retrieve(self, request, pk):
        try: 
            post = Post.objects.annotate(comment_count=Count('comments')).get(pk=pk)
            serializer = PostSerializer(post)
            return Response(serializer.data)
        except Post.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        try:
            rare_user =  request.query_params.get('uid', None)
            if rare_user is not None:
                rare_user_id = RareUser.objects.get(uid = rare_user)
                posts = Post.objects.filter(rare_user = rare_user_id).annotate(comment_count=Count('comments'))

            else:
                posts = Post.objects.annotate(comment_count=Count('comments')).all()
            
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
    
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    
    # This action method gets all comments associated with a single post
    @action(methods=['get'], detail=True, url_path='comments')
    def comments(self, request, pk=None):
        try:
            post = self.get_object()
            comments = Comment.objects.filter(post_id=pk)
            serializer = CommentSerializer(comments, many=True)
            return Response(serializer.data)
        except Post.DoesNotExist:
            return Response({'message': 'Post not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    # This action method posts comments on a single post
    @action(methods=['post'], detail=True)
    def post_comment(self, request, pk):
        try:
            # Retrieve rare_user and post based on request data
            author = RareUser.objects.get(pk=request.data["author"])
            post = Post.objects.get(pk=pk)
            comment = Comment.objects.create(
                author=author,
                post=post,
                content=request.data["content"]
            )
            return Response({'message': 'Comment has been successfully added'}, status=status.HTTP_201_CREATED)
        except RareUser.DoesNotExist:
            return Response({'message': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)
        
        except Post.DoesNotExist:
            return Response({'message': 'Post does not exist'}, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        