from rest_framework import generics, permissions

from .models import CustomUser
from .serializers import UserSerializer

# Create your views here.


class UserCreateView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer


class UserListView(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer


class UserRetrieveView(generics.RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    lookup_field = "pk"


class UserUpdateView(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated,]
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    lookup_field = "pk"

    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)


class UserDeleteView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated,]
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    lookup_field = "pk"
