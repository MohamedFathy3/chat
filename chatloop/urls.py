"""
URL configuration for chatloop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.utils.translation import override
from django.conf import settings
from django.conf.urls.static import static
from chatloop.views import register_user
from chatloop.views import ConectUs
from chatloop.views import viwer
from chatloop.views import chat
from chatloop.views import chatkhaleg
from chatloop.views import dashboard
from django.shortcuts import redirect

# from chatloop.views import chats
# from chatloop.views import choose_role
# from chatloop.views import enter_room_as_guest
# from chatloop.views import chat_room

from . import views

from django.contrib.auth import views as auth_views


urlpatterns = [
    path('register/', register_user, name='register'),
    path('conectus', ConectUs, name='connectus'),
    path('login/', auth_views.LoginView.as_view(), name='login'),  # صفحة تسجيل الدخول
    path('viwer/', viwer, name='viwer'),
    path('chat/', chat, name='chat'),
    path('chatkhaleg/<slug:slug>/', chatkhaleg, name='chatkh'),
    path('dashboard/', dashboard, name='dashboard'),   
    path('', views.home, name='home'),  # الصفحة الرئيسية لعرض الغرف
    path('room/<slug:slug>/', views.room_detail, name='room_detail'),  # عرض تفاصيل الغرفة
    path('room/<slug:slug>/enter/', views.room_enter, name='room_enter'), 
    path('rooms/<slug:slug>/enter/', views.room_enter, name='room_enter'),  # صفحة لاختيار الدخول كعضو أو زائر
    path('guest_login/<slug:slug>/', views.guest_login, name='guest_login'),  # تسجيل دخول الزائر
    path('user_login/<slug:slug>/', views.user_login, name='user_login'),  # تسجيل دخول العضو
    path('chat/<slug:slug>/', views.chatloop, name='chatloop'),
    path('chat/<slug:slug>/guest_logout/', views.guest_logout, name='guest_logout'),
    path('chat/<slug:slug>/user_logout/', views.user_logout, name='user_logout'),
    path('room/<slug:slug>/load_messages/', views.load_messages, name='load_messages'),
    path('room/<slug:slug>/load_new_messages/', views.load_new_messages, name='load_new_messages'),
    path('edit_style/', views.edit_style, name='edit_style'),
    path('edit-profile/', views.edit_profile, name='edit-profile'),
    path('edit-style/', views.edit_style, name='edit-style'),
    path('profile/<int:user_id>/', views.user_profile, name='user_profile'),
    path('profile/<int:user_id>/send_message/', views.send_message, name='send_message'),
    path('load_new_messages/<int:user_id>/', views.load_new_messages, name='load_new_messages'),
    path('room/<slug:slug>/remove_member/<int:member_id>/', views.remove_member_from_room, name='remove_member_from_room'),
    path('room/<slug:slug>/remove_guest/<int:guest_id>/', views.remove_guest_from_room, name='remove_guest_from_room'),

    # path('chats/<slug:slug>/', chats, name='chatss'),
    # path('room/<slug:slug>/enter/', enter_room_as_guest, name='enter_room_as_guest'),
    # path('room/<slug:slug>/choose/', choose_role, name='choose_role'),  # الغرفة بعد دخول الزائر
    # path('room/<slug:slug>/send_message/', send_message, name='send_message'),  # إرسال رسالة
    # path('room/<slug:slug>/', chat_room, name='chatss'),



]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
