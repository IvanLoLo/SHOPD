from django.urls import path
from . import views 


urlpatterns = [
    path('dbhome', views.databaseHome, name='dbHome'),
] 