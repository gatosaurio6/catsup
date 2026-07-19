from rest_framework import generics
from .models import comentario
from .serializers import ComentarioSerializer

# leer
class ComentariosPorPostView(generics.ListAPIView):
    serializer_class = ComentarioSerializer

    def get_queryset(self):
        id_post_url = self.kwargs['id_post']
        return comentario.objects.filter(id_post=id_post_url).order_by('-fecha_publicacion')

# crea
class ComentarioCreateView(generics.CreateAPIView):
    queryset = comentario.objects.all()
    serializer_class = ComentarioSerializer

class ComentarioDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = comentario.objects.all()
    serializer_class = ComentarioSerializer
    lookup_field = 'id'