from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('products/', views.product_list, name='product_list'),
    path('products/update/<int:pk>/', views.update_product, name='update_product'),  # Update a product
    path('products/delete/<int:pk>/', views.delete_product, name='delete_product'),  # Delete a product
    path('billing/', views.billing_page, name='billing_page'),
    path('billing/summary/<int:purchase_id>/', views.bill_summary, name='bill_summary'),
    path('purchases/', views.purchase_list, name='purchase_list'),
    path('purchase/delete/<int:purchase_id>/', views.delete_purchase, name='delete_purchase'),
    path('purchases/<int:purchase_id>/', views.purchase_detail, name='purchase_detail'),
    path('denominations/', views.denomination_list, name='denomination_list'),
    path('denominations/add/', views.add_denomination, name='add_denomination'),
    path('denominations/<int:denomination_id>/update/', views.update_denomination, name='update_denomination'),
    path('denominations/delete/<int:denomination_id>/', views.delete_denomination, name='delete_denomination'),  # Delete URL
]
