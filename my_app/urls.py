
from django.urls import path
from . import views

urlpatterns = [
    
    path('', views.display_homepage),
    path('index', views.index),#dachboard
    path('logout', views.logout),
    path('employees', views.display_employees),
    path('add_employee', views.add_new_employee),
    path('employye_dashboard', views.display_employee_dashboard),
    path('add_product', views.add_new_product),
    path('sales', views.display_sales),
    path('purchases', views.display_purchases),
    path('delete_product', views.delete_product),
    
    path('add_order_to_sale', views.add_product_to_sale),
    
    path('submet_sale_order', views.submet_sale_order),
    path('employee_reports', views.display_employee_reports),
    path('view_sale_order/<int:id>', views.view_sale_order),
    
    path('signup', views.sign_up),

    path('signin', views.sign_in),

    path('about_us', views.about_us),


]