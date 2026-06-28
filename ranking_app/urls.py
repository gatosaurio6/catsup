from django.urls import path
from . import views

urlpatterns = [
    # Esta ruta será: http://127.0.0.1:8000/api/ranking/top10/
    path('top10/', views.TopCatsListView.as_view(), name='top_ten'),
]