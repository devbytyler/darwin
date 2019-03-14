from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.api_root, name='root'),
    path('login/', views.Login.as_view(), name='login'),
    path('register/', views.register, name='register'),
    path('boards/<int:board_id>', views.board_page, name='board_page'),
    path('vote/', views.cast_vote, name='cast_vote'),
    
    #API-browser routes
    path('api/',include([
        path('boards/', views.BoardList.as_view(), name='boards'),
        path('boards/<int:pk>/', views.BoardDetail.as_view(), name='board'),

        path('ideas/', views.IdeaList.as_view(), name='ideas'),
        path('ideas/<int:pk>', views.IdeaDetail.as_view(), name='idea'),

        path('votes/', views.VoteList.as_view(), name='votes'),

        path('users/', views.UserList.as_view(), name='users'),
        path('users/<int:pk>/', views.UserDetail.as_view(), name='user'),
        path('users/<int:user_id>/boards/', views.user_boards, name='user_boards'),
        path('users/<int:user_id>/ideas/', views.user_ideas, name='user_ideas'),
        path('users/<int:user_id>/votes/', views.user_votes, name='user_votes'),
    ])),
]   