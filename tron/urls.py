from django.urls import path
from .views import start_research


urlpatterns = [
    path('check_address/<str:address>/', start_research, name='check_address')
]