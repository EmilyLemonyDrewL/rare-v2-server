from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rareapi.models import Reaction, PostReaction, RareUser, Post
from rest_framework.decorators import action
import json

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

        serializer = PostReactionSerializer(post_reaction)
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
    
    @action(methods=['get'], detail=True)
    def getReactions(self, request, pk):
        post_reactions = PostReaction.objects.filter(post_id = pk)
        reactions_amounts = []

        for post_reaction in post_reactions:
            found = False
            for reaction in reactions_amounts:
                if post_reaction.reaction_id == reaction.get('id'):
                    reaction['amount'] += 1
                    found = True
                    break
            if not found:
                reactions_amounts.append({'id': post_reaction.reaction.id, 'amount': 1})


        json_data = json.dumps(reactions_amounts)

        return Response(json_data)

class PostReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostReaction
        fields = ('id', 'rare_user_id', 'post_id', 'reaction_id')
