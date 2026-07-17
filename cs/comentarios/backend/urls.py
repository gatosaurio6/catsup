from django.urls import path
from .views import lc, cc
urlpatterns = [
    path('post/<int:id_post>/', lc, name='listar_comentarios'),
    path('comentar/', cc, name='comentar')
]