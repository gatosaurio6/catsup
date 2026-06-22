from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CatProfileViewSet, PostViewSet

# El router crea automáticamente todas las URLs para el CRUD
router = DefaultRouter()
router.register(r'cats', CatProfileViewSet)
router.register(r'posts', PostViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]