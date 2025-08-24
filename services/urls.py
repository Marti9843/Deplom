from django.urls import path
from . import views

app_name = 'services'

urlpatterns = [
    path('booking/', views.booking, name='booking'),
    path('load-activities/', views.load_activities, name='load_activities'),

    # Група URL для послуг
    path('fitness/', views.fitness, name='fitness'),
    path('pool/', views.pool, name='pool'),
    path('yoga/', views.yoga, name='yoga'),
    path('massage/', views.massage, name='massage'),
]