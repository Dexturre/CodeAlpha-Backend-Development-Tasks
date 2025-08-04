from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('event/<int:event_id>/', views.event_detail, name='event_detail'),
    path('my_registrations/', views.my_registrations, name='my_registrations'),
    path('cancel_registration/<int:registration_id>/', views.cancel_registration, name='cancel_registration'),
]
