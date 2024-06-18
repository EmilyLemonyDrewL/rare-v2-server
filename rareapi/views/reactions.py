from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rareapi.models import Reaction, PostReaction, RareUser, Post
from rest_framework.decorators import action

class ReactionView(ViewSet):

    def retrieve(self, request, pk):
        try:
            reaction = Reaction.objects.get(pk=pk)
            serializer = ReactionSerializer(reaction)
            return Response(serializer.data)
        except reaction.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        reactions = Reaction.objects.all()
        serializer = ReactionSerializer(reactions, many=True)
        return Response(serializer.data)

    def create(self, request):

        reaction = Reaction.objects.create(
            label = request.data['label'],
            image_url = request.data['image_url'],
        )

        serializer = ReactionSerializer(reaction)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        reaction = Reaction.objects.get(pk=pk)
        reaction.label = request.data['label']
        reaction.image_url = request.data['image_url']
        reaction.save()

        serializer = ReactionSerializer(reaction)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, pk):
        reaction = Reaction.objects.get(pk=pk)
        reaction.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    @action(methods=['post'], detail=False)
    def check_if_emoji_exists(self, request):
        image_url = request.data.get('emoji')

        user = RareUser.objects.get(uid=request.data.get('user_id'))
        post = Post.objects.get(pk=request.data.get('post_id'))
        exists = Reaction.objects.filter(image_url=image_url).exists()

        if exists:
            
            reaction = Reaction.objects.get(image_url=image_url)
            alreadySelected = PostReaction.objects.filter(post=post, rare_user=user, reaction = reaction).exists()

            if alreadySelected:             
                post_reaction = PostReaction.objects.filter(post=post, rare_user=user, reaction= reaction)
                post_reaction.delete()
            else:
                PostReaction.objects.create(
                    rare_user = user,
                    post = post,
                    reaction = reaction
                )
        else:
            reaction = Reaction.objects.create(
                label = "emoji",
                image_url = image_url
            )
            PostReaction.objects.create(
                rare_user = user,
                post = post,
                reaction = reaction
            )   

        return Response(status=status.HTTP_200_OK)

class ReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reaction
        fields = ('id', 'label', 'image_url')
