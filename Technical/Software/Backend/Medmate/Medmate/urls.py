"""MedMate URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path
from medapi.api.views import client_registration_view, client_login_view, fetch_all_valid_locations_view,change_client_location_view, order_request_view, operator_ack_view, request_status_view,set_robot_status_view,get_all_requests_view,fetch_all_locations_view,operator_login_view

urlpatterns = [
    path('admin/', admin.site.urls),
    #Client Requests
    path('client_register',client_registration_view),
    path('client_login',client_login_view),
    path('change_client_location',change_client_location_view),
    path('order',order_request_view),
    path('get_all_requests',get_all_requests_view),
    #operator Requests
    path('operator_login',operator_login_view),
    path('set_request_status/<requestId>/<status>',request_status_view),
    path('operator_ack/<requestId>',operator_ack_view),
    path('set_robot_status',set_robot_status_view),
    #Generic Requests
    path('get_valid_locations/<hKey>',fetch_all_valid_locations_view),
    path('get_all_locations/<hKey>/<cachedTs>',fetch_all_locations_view),
]
