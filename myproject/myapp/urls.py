from django.urls import path
from . import views

urlpatterns = [
    path('send_dictionary/', views.send_dictionary, name='send_dictionary'),
]
