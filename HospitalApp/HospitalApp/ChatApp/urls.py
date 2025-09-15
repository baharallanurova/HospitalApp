from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'chat'

urlpatterns = [
    path('', views.chat_home, name='home'),
    path('logout/', auth_views.LogoutView.as_view(template_name="chat/logout.html"), name='logout'),
    path('home/<int:pk>/', views.chat_home, name='home-with-pk'),
    path('profile/', views.profile, name='profile'),
    path('send/', views.send_chat, name='send'),
    path('messages/', views.get_messages, name='get-messages'),
    path('conversations/', views.get_conversations, name='get-conversations'),
]