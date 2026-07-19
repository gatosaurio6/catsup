from django.urls import path
from .views import gp, ep

urlpatterns = [
    path("post/", gp.as_view(), name="general posts"),
    path("post/<int:pk>", ep.as_view(), name="especific post")
]