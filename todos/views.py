from .models import Todo
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import TodoSerializer


class TodoViewSet(viewsets.ModelViewSet):
    ## The Main Query for the index route
    queryset = Todo.objects.all()
    # The serializer class for serializing output
    serializer_class = TodoSerializer
    # optional permission class set permission level
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]  #Could be [permissions.IsAuthenticated]


from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import generics, permissions, status
from django.contrib.auth.models import User
from .serializers import UserSerializer, TokenSerializer
from django.contrib.auth import authenticate, login
from rest_framework.response import Response


class LoginView(generics.ListCreateAPIView):
    """
    POST user/login/
    """

    # This permission class will overide the global permission class setting
    # Permission checks are always run at the very start of the view, before any other code is allowed to proceed.
    # The permission class here is set to AllowAny, which overwrites the global class to allow anyone to have access to login.
    permission_classes = (permissions.AllowAny, )
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        username = request.data.get("username", "")
        password = request.data.get("password", "")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # login saves the user’s ID in the session,
            # using Django’s session framework.
            login(request, user)
            refresh = RefreshToken.for_user(user)
            serializer = TokenSerializer(
                data={
                    # using DRF JWT utility functions to generate a token
                    "token": str(refresh.access_token)
                })
            serializer.is_valid()
            return Response(serializer.data)
        return Response(status=status.HTTP_401_UNAUTHORIZED)