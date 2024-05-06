from django.db import models

# Create your models here.
# the manager teble
# manager can add many imployees
class Manager(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    password = models.CharField(max_length=255)
    confirm_password = models.CharField(max_length=255)
    phone = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # employees

# EMP adds many Products
# EMP can make many purchasing invoices
# EMP can make many sales orders
class Employee(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    DOB = models.DateField()
    password = models.CharField(max_length=255)
    confirm_password = models.CharField(max_length=255)
    manager = models.ForeignKey(Manager , related_name="employees", on_delete=models.RESTRICT) # RESTRICT if the manager deleted >>  dont delete the employees
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # products
    # purchasing_invoice
    # sale_orders



class Product(models.Model):
    product_name = models.CharField(max_length=255)
    quantity = models.IntegerField()
    purchasing_price = models.DecimalField(max_digits=6, decimal_places=2) # 999999.99
    expiry_date  = models.DateField()
    supplier = models.CharField(max_length=255)  # Supplier NAME
    employee = models.ForeignKey(Employee , related_name="products", on_delete=models.RESTRICT) # RESTRICT  deleted >>  dont delete the item or ( default="Default", on_delete=models.SET_DEFAULT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # purchasing_invoices
    # sale_orders


class Purchasing_invoice(models.Model):
    product_name = models.CharField(max_length=255) 
    quantity = models.IntegerField()
    employee = models.ForeignKey(Employee , related_name="purchasing_invoices", on_delete=models.RESTRICT) # RESTRICT  deleted >>  dont delete the item or ( default="Default", on_delete=models.SET_DEFAULT)
    products = models.ManyToManyField(Product, related_name="purchasing_invoices")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # products

class Sale_order(models.Model):
    product_name = models.CharField(max_length=255) 
    quantity = models.IntegerField()
    employee = models.ForeignKey(Employee , related_name="sale_orders", on_delete=models.RESTRICT) # RESTRICT  deleted >>  dont delete the item or ( default="Default", on_delete=models.SET_DEFAULT)
    products = models.ManyToManyField(Product, related_name="sale_orders")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # products