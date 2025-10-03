from django.urls import path
from .views import *
from . import views


urlpatterns = [
    path('home', HomePage.as_view(), name='home'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('edit_profile/', EditProfileView.as_view(), name='edit_profile'),
    path('users/<str:username>/', FindUserView.as_view(), name='find_user'),
    path('found_users/<str:username>/', SearchUsersView.as_view(), name='search_users'),
    path('followers_list/', FollowersView.as_view(), name='followers_list'),
    path('followings_list/', FollowingsView.as_view(), name='followings_list'),
    path('add_post/', AddPostView.as_view(), name='add_post'),
    path('edit_post/<int:post_id>/', EditPostView.as_view(), name='edit_post'),
    path('edit_post/<int:post_id>/', EditPostView.as_view(), name='edit_post'),
    path('', views.beginning, name='beginning'),
]