from django.urls import path
from . import views

urlpatterns = [
    path('signin/', views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),
    path('verification/', views.verification, name='verification'),
    path('my-profile/', views.my_profile, name='my_profile'),
    path('profile/<int:profile_id>/', views.profile_detail, name='profile_detail'),
    path('settings/', views.settings, name='settings'),
    path('logout/', views.logout, name='logout'),
    path('search/', views.search, name='search'),
    path('follow/<int:profile_id>/', views.follow_profile, name='follow_profile'),
    path('unfollow/<int:profile_id>/', views.unfollow_profile, name='unfollow_profile'),
    path('follow-profile-search/<int:profile_id>/', views.follow_profile_search, name='follow_profile_search'),
    path('unfollow-profile-search/<int:profile_id>/', views.unfollow_profile_search, name='unfollow_profile_search'),
]