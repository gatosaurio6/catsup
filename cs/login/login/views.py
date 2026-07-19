from rest_framework import generics
from rest_framework.permissions import AllowAny
from .models import Usuario
from .serializers import RegisterSerializer

class RegisterView(generics.CreateAPIView):
    queryset = Usuario.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer