from rareapi.models import RareUser
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['POST'])
def check_user(request):
    '''Checks to see if User has Associated Gamer

    Method arguments:
      request -- The full HTTP request object
    '''
    uid = request.data['uid']

    # Use the built-in authenticate method to verify
    # authenticate returns the user object or None if no user is found
    user = RareUser.objects.filter(uid=uid).first()

    # If authentication was successful, respond with their token
    if user is not None:
        data = {
            'id': user.id,
            'email': user.email,
            "profile_image_url": user.profile_image_url,
            'is_staff': user.is_staff,
            'active': user.active,
            'uid': user.uid,
            'bio': user.bio,
            'first_name': user.first_name,
            'last_name': user.last_name
        }
        return Response(data)
    else:
        # Bad login details were provided. So we can't log the user in.
        data = { 'valid': False }
        return Response(data)

