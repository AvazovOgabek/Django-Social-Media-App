from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('comments/<int:pk>/', views.post_comments, name='post_comments'),

]