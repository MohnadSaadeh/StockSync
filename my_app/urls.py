
from django.urls import path
from . import views

urlpatterns = [
    
    path('', views.display_homepage),
    path('index', views.index),
    path('logout', views.logout),
    path('employees', views.display_employees),
    path('add_employee', views.add_neww_employee),
    path('employye_dashboard', views.display_employee_dashboard),
    path('add_product', views.add_new_product),
    path('signup', views.sign_up),

    path('signin', views.sign_in),


]