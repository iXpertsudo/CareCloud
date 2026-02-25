
from django.contrib import admin
from django.urls import path, include
from CareApp import views


urlpatterns = [
    path('admin/', admin.site.urls),
     path('', views.home, name='home'),
     path('starter/', views.starter, name='starter'),


      path('appointment/', views.appointment, name='appointment'),

      path('about/', views.about, name='about'), 

]