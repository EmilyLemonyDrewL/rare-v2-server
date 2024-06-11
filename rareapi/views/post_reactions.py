from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rareapi.models import Reaction, PostReaction, RareUser, Post

class PostReactionView(ViewSet):

    def retrieve(self, request, pk):
        try:
            post_reaction = PostReaction.objects.get(pk=pk)
            serializer = PostReactionSerializer(post_reaction)
            return Response(serializer.data)
        except post_reaction.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        post_reactions = PostReaction.objects.all()
        serializer = PostReactionSerializer(post_reactions, many=True)
        return Response(serializer.data)

    def create(self, request):

        rare_user = RareUser.objects.get(pk=request.data['rare_user_id'])
        post = Post.objects.get(pk=request.data['post_id'])
        reaction = Reaction.objects.get(pk=request.data['reaction_id'])

        post_reaction = PostReaction.objects.create(
            rare_user = rare_user,
            post = post,
            reaction = reaction,
        )

        serializer = PostReactionViewSerializer(post_reaction)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        post_reaction = PostReaction.objects.get(pk=pk)
        rare_user = RareUser.objects.get(pk=request.data['rare_user_id'])
        post_reaction.rare_user = rare_user
        post = Post.objects.get(pk=request.data['post_id'])
        post_reaction.post = post
        reaction = Reaction.objects.get(pk=request.data['reaction_id'])
        post_reaction.reaction = reaction
        post_reaction.save()

        serializer = PostReactionSerializer(post_reaction)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, pk):
        post_reaction = PostReaction.objects.get(pk=pk)
        post_reaction.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

class PostReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostReaction
        fields = ('id', 'rare_user_id', 'post_id', 'reaction_id')
