from django.urls import path
from . import views

app_name = 'services'

urlpatterns = [
    path('booking/', views.booking, name='booking'),
    path('fitness/', views.fitness, name='fitness'),
    path('pool/', views.pool, name='pool'),
    path('yoga/', views.yoga, name='yoga'),
    path('massage/', views.massage, name='massage'),
]