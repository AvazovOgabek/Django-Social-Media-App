from django.urls import path
from . import views

urlpatterns = [
    path('create_post/', views.create_post_view, name='create_post'),
    path('like/<int:post_id>/', views.like_post, name='like_post'),
    path('unlike/<int:post_id>/', views.unlike_post, name='unlike_post'),
    path('unsave/<int:post_id>/', views.unsave_post, name='unsave_post'),
    path('save/<int:post_id>/', views.save_post, name='save_post'),
    path('saves/', views.saves, name='saves'),
]