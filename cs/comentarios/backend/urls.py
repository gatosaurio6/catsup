from django.urls import path
from .views import ComentariosPorPostView, ComentarioCreateView, ComentarioDetailView

urlpatterns = [
    path('post/<int:id_post>/', ComentariosPorPostView.as_view(), name='listar_comentarios'),
    
    path('crear/', ComentarioCreateView.as_view(), name='crear_comentario'),
    
    path('<int:id>/', ComentarioDetailView.as_view(), name='detalle_comentario'),
]