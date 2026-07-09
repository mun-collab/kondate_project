from django.urls import path
from . import views
from django.contrib import admin
from django.urls import path, include
from .views import SignUpView

urlpatterns = [
    path('', views.index, name='index'),
    # recommend の行を削除するか、以下のように views.py にある名前だけに絞ります
    path('save_result/', views.save_result, name='save_result'),
    path('history/', views.history_list, name='history_list'),
    path('delete/<int:history_id>/', views.delete_history, name='delete_history'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('post/', views.post_meal, name='post_meal'),
    path('posts/', views.post_list, name='post_list'),
]