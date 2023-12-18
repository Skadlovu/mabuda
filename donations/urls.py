from django.urls import path
from .views import donation_view

app_name = 'donation'  

urlpatterns = [
    path('donate/', donation_view, name='donate'),
    path('thank-you/', thank_you_view, name='thank_you'),
]
