from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.authtoken.models import Token
from ..serializers import UserCreateSerializer
from django.contrib.auth import authenticate, login, logout

class SignUp(generics.CreateAPIView):
    # Override the authentication/permissions classes so this endpoint
    # is not authenticated & we don't need any permissions to access it.
    authentication_classes = ()
    permission_classes = ()

    def post(self, request):
        # Create the user using the UserSerializer
        created_user = UserCreateSerializer(data=request.data['user'])
        # Check user is valid
        if created_user.is_valid():
            # Save the user and send back a response!
            created_user.save()
            return Response({'user': created_user.data}, status=status.HTTP_201_CREATED)
        else:
            return Response(created_user.errors, status=status.HTTP_400_BAD_REQUEST)

class SignIn(generics.CreateAPIView):
    # Override the authentication/permissions classes so this endpoint
    # is not authenticated & we don't need any permissions to access it.
    authentication_classes = ()
    permission_classes = ()

    def post(self, request):
        data = request.data['user']
        # use django authenticate to verify password and email match
        user = authenticate(
            request, email=data['email'], password=data['password'])
        # Is our user is successfully authenticated...
        if user is not None:
            login(request, user)
            # use django generate a token and save it to user
            Token.objects.filter(user=user).delete()
            token = Token.objects.create(user=user)
            user.token = token.key
            user.save()
            # return the user with their id, email and token
            return Response({
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'token': token.key
                }
            })
        else:
            return Response({'msg': 'The username and/or password is incorrect.'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

class SignOut(generics.DestroyAPIView):
    def delete(self, request):
        user = request.user
        # Remove this token from the user
        Token.objects.filter(user=user).delete()
        user.token = None
        user.save()
        # Logout will remove all session data
        logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)

class ChangePassword(generics.UpdateAPIView):
    def patch(self, request):
        user = request.user
        old_pw = request.data['passwords']['old']
        new_pw = request.data['passwords']['new']
        # This is included with the Django base user model
        # https://docs.djangoproject.com/en/3.2/ref/contrib/auth/#django.contrib.auth.models.User.check_password
        if not user.check_password(old_pw):
            return Response({'msg': 'Wrong password'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        # set_password will also hash the password
        # https://docs.djangoproject.com/en/3.2/ref/contrib/auth/#django.contrib.auth.models.User.set_password
        user.set_password(new_pw)
        user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
