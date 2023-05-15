"""CASYU URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from zipfile import Path
from django.contrib import admin
from django.urls import path
from home import views

urlpatterns = [
    path('',views.home, name='home'),
    path('trying',views.trying, name='changing_password.html'),
    #when we'll visit / then it will show the page which will be on views.py of name home function 
    # path()
    path('signup',views.signup, name='signup.html'),
    path('signin',views.signin, name='signin.html'),
    path('forget_password',views.forgot_password, name='forget_password.html'),
    path('otp_verification',views.otp,name='otp_verification.html'),
    path('changing_password',views.changing_password,name='changing_password.html'),
    path('logout',views.logout, name='logout.html'),
    path('bargin',views.bargin,name='bargin.html'),
    path('sending_request',views.sending_request,name='sending_request.html'),
    path('pending_request',views.pending_request,name='pending_request.html'),
    path('delete_request',views.delete_request,name='pending_request.html'),
    path('bargin_request',views.bargin_request,name='pending_request.html'),
    path('accept_request',views.accept_request,name='pending_request.html'),
    path('accepted_request',views.accepted,name='accept_request.html'),
    path('fileupload',views.hotel_image_view, name='fileupload.html'),
    path('hotel_images', views.display_hotel_images, name = 'displayimages.html'),
    # path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',views.activate, name='activate'), 
    path('service_signup',views.signup_service,name='signup_service.html'),
    path('service_signin',views.sign_service,name='service_signin.html'),
    path('service_forget_password',views.service_forgot_password, name='service_forget_ped.html'),
    path('service_otp_verification',views.service_otp,name='service_otp.html'),
    path('service_changing_password',views.service_changing_password,name='service_changing_pwd.html'),
    path('service_logout',views.service_logout, name='service_logout.html'),
    path('service_recieve_request',views.service_recieve_request,name='ser_receive_request.html'),
    path('service_delete_request',views.service_delete_request,name='ser_receive_request.html'),
    path('service_bargin_request',views.service_bargin_request,name='ser_receive_request.html'),
    path('service_accept_request',views.service_accept_request,name='ser_receive_request.html'),
    path('service_accepted_request',views.service_accepted,name='ser_accept_request.html'),
]
