from django.urls import path
from . import views

app_name = "main"
urlpatterns = [
    path('list/', views.list, name="list"),
    path('down/<int:pk>/', views.down, name="down"),
    path('up/', views.up, name="up"),
    path('', views.index, name="index"),
    path('test/', views.test, name="test"),
]