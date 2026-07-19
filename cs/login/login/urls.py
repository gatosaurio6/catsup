from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegisterView

urlpatterns = [
    # Ruta registrar nuevo usuario
    path('register/', RegisterView.as_view(), name='register'),
    
    # Ruta inicio sesión
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    
    # Ruta refresh
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]