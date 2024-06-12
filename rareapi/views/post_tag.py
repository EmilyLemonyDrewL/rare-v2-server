from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rareapi.models import Post, PostTag, Tag

class PostTagView(ViewSet):
    def create(self, request):
        post = Post.objects.get(pk=request.data["post_id"])
        tag = Tag.objects.get(pk=request.data["tag_id"])
        
        post_tag = PostTag.objects.create(
            post = post,
            tag = tag
        )
        serializer = PostTagSerializer(post_tag)
        return Response(serializer.data)
    
    def destroy(self, request, pk):
        post_tag = PostTag.objects.get(pk=pk)
        post_tag.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class PostTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostTag
        fields = ('id', 'post_id', 'tag_id')
