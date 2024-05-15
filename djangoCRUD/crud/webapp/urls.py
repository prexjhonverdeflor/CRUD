
from django.urls import path
from . import views


urlpatterns = [
    
    path('', views.home, name=""),
    path('register', views.register, name="register"),
    path('my-login', views.my_login, name="my-login"),
    path('user-logout', views.user_logout, name="user-logout"),

    path('dashboard', views.admin_dashboard, name="dashboard"),
    path('create-record', views.create_record, name="create-record"),
    path('update-record/<int:pk>', views.update_record, name="update-record"),
    path('record/<int:pk>', views.singular_record, name="record"),
    path('delete-record/<int:pk>', views.delete_record, name="delete-record"),

    path('customer', views.customer, name='customer'),
    path('customer-create/', views.customer_create, name='customer_create'),
    path('customer-update/<int:customer_id>', views.customer_update, name='customer_update'),
    path('customer_delete/<int:pk>', views.customer_delete, name="customer_delete"),

    path('bic-setup/', views.bic_setup, name='bic_setup'),
    path('bic-create/', views.bic_setup_create, name='bic_setup_create'),
    path('bic-update/<int:product_code>/', views.bic_setup_update, name='bic_setup_update'),
    path('bic-setup/delete/<str:product_code>/', views.bic_setup_delete, name='bic_setup_delete'),


    path('cashier-dashboard', views.cashier_dashboard, name='mc_register'),
    path('mc-create/', views.mc_register_create, name='mc_register_create'),
    path('mc-update/<int:mc_register_id>', views.mc_register_update, name='mc_register_update'),

    path('peso-net', views.peso_net, name='peso_net'),
    path('peso-create/', views.peso_create, name='peso_create'),
    path('peso-update/<int:peso_net_id>', views.peso_update, name='peso_update'),
    
    path('bic-cashier/', views.bic_cashier, name='bic_cashier'),


]