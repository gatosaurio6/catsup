from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.exceptions import PermissionDenied
from .models import comentario
from .serializers import ComentarioSerializer

# 1. leer
class ComentariosPorPostView(generics.ListAPIView):
    serializer_class = ComentarioSerializer

    def get_queryset(self):
        id_post_url = self.kwargs['id_post']
        return comentario.objects.filter(id_post=id_post_url).order_by('-fecha_publicacion')

# 2. crear
class ComentarioCreateView(generics.CreateAPIView):
    queryset = comentario.objects.all()
    serializer_class = ComentarioSerializer
    permission_classes = [IsAuthenticatedOrReadOnly] # teni q estar logeado

    def perform_create(self, serializer):
        serializer.save(id_usuario=self.request.user.id)

# 3. actualizar y borrar
class ComentarioDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = comentario.objects.all()
    serializer_class = ComentarioSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = 'id'

    def perform_update(self, serializer):
        if self.get_object().id_usuario != self.request.user.id:
            raise PermissionDenied("¡Acceso denegado! No puedes editar un comentario que no es tuyo.")
        serializer.save()

    def perform_destroy(self, instance):
        # la misma protección para la eliminación
        if instance.id_usuario != self.request.user.id:
            raise PermissionDenied("¡Acceso denegado! No puedes borrar un comentario que no es tuyo.")
        instance.delete()