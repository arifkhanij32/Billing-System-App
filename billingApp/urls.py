
from django.urls import path
from . import views

urlpatterns = [
    
    path('home', views.home, name='home'),
    path('billing', views.billing_page, name='billing'),
    path('billsummary', views.bill_summary, name='bill_summary'),  

]
