from django.urls import path
from . import views

urlpatterns = [
    path('posts', views.posts, name='posts'),
    path('post_detail/<int:pk>/', views.post_detail, name='post_detail'),
    path('post_new', views.post_new, name='post_new'),
    path('user/<int:id>/', views.user_profile, name='user_profile'),
    path('admin/users/info', views.users_info, name='users_info'),
    path('post/<int:pk>/edit', views.post_edit, name='post_edit'),
    path('post/<int:pk>/delete', views.post_delete, name='post_delete'),
    path('json/response', views.json_response),
    path('string <response>', views.string_response)
]
