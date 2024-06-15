from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rareapi.models import Post, PostTag, Tag

class PostTagView(ViewSet):
    def create(self, request):
        tag_ids = request.data["tag_ids"]
        post_id = request.data["post_id"]
        for tag_id in tag_ids:
                
            post = Post.objects.get(pk=post_id)
            tag = Tag.objects.get(pk=tag_id)

            PostTag.objects.create(
                post = post,
                tag = tag
            )

        return Response(status=status.HTTP_201_CREATED)
    
    def destroy(self, request, pk):
        post_tag = PostTag.objects.get(pk=pk)
        post_tag.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class PostTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostTag
        fields = ('id', 'post_id', 'tag_id')
