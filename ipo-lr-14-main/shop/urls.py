from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('store/', views.store, name='store'),
    path('spec/', views.qualification_list, name='qualification_list'),
    path('spec/<str:id>/', views.qualification_detail, name='qualification_detail'),
]