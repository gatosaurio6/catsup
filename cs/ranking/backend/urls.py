from django.urls import path
from .views import rv, total

urlpatterns = [
    path("votar/",rv.as_view(), name="registarvoto"),
    path("total/", total.as_view(), name="pt")
]