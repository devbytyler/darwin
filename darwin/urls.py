from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.api_root, name='root'),
    path('login/', views.Login.as_view(), name='login'),
    path('register/', views.register, name='register'),
    path('ideas/', views.ideas, name='ideas'),
    path('boards/', views.BoardList.as_view(), name='boards'),
    path('boards/<int:pk>/', views.BoardDetail.as_view(), name='board'),
    path('user/<int:user_id>/boards/', views.user_boards, name='user_board'),
    path('users/', views.UserList.as_view(), name='users'),
    path('users/<int:pk>/', views.UserDetail.as_view(), name='user'),
    path('users/<int:user_id>/votes/', views.user_votes, name='user_votes'),
    path('users/<int:idea_id>/ideas/', views.user_ideas, name='user_ideas'),
]   