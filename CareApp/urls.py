
from django.contrib import admin
from django.urls import path, include
from CareApp import views


urlpatterns = [
    path('admin/', admin.site.urls),
     path('', views.home, name='home'),
     path('starter/', views.starter, name='starter'),


      path('appointment/', views.appointment, name='appointment'),

      path('about/', views.about, name='about'), 

      path('show/', views.show, name='show'),

      path('delete/<int:id>', views.delete),

      path('edit/<int:id>', views.edit),

       #Mpesa URLS
    path('pay/', views.pay, name='pay'),

    path('stk/', views.stk, name='stk'),
    path('token/', views.token, name='token'),
    path('payment-result/', views.payment_result, name='payment_result'),
    path('transactions/', views.transactions_list, name='transactions'),


    #Authentication
    path('register/', views.register, name='register'),

    path('login/', views.login, name='login'),

    


    





]