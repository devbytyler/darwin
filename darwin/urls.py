from django.urls import include, path
from . import views

urlpatterns = [
    path('ideas/', views.ideas),
    path('boards/', views.BoardList.as_view()),
    path('boards/<int:pk>/', views.BoardDetail.as_view()),
    path('user/<int:user_id>/boards/', views.user_boards),
]

# urlpatterns = [
#     path('', views.home, name='home'),
#     path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
#     path('api/', include([
#         path('boards/', views.boards, name='boards'),
#         path('boards/add', views.add_board, name='add_board'),
#         path('boards/<int:pk>/', views.board, name='board'),
#         path('boards/<int:pk>/edit/', views.edit_board, name='edit_board'),
#         path('boards/<int:pk>/delete/', views.delete_board, name='delete_board'),

#         path('boards/<int:board_id>/ideas/', views.ideas, name='idea'),
#         path('boards/<int:board_id>/ideas/<int:pk>', views.idea, name='idea'),
#         path('boards/<int:board_id>/ideas/add', views.add_idea, name='add_idea'),
#         path('boards/<int:board_id>/ideas/<int:pk>/edit', views.edit_idea, name='edit_idea'),
#         path('boards/<int:board_id>/ideas/<int:pk>/delete', views.delete_idea, name='delete_idea'),
#     ])),
    
# ]