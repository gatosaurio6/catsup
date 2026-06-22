from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CatProfileViewSet, PostViewSet, CommentViewSet 

router = DefaultRouter()
router.register(r'cats', CatProfileViewSet)
router.register(r'posts', PostViewSet)
router.register(r'comments', CommentViewSet) 

urlpatterns = [
    path('api/', include(router.urls)),
]