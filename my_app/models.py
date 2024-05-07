from django.db import models
import re
#--------------------------------------------------------------------MANAGER-----------------------
class ManagerManager(models.Manager):
    def manager_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(postData['admin_first_name']) < 2:
            errors['admin_first_name'] = "First name should be at least 2 characters"
        if len(postData['admin_last_name']) < 2:
            errors['admin_last_name'] = "Last name should be at least 2 characters"
        if not EMAIL_REGEX.match(postData['admin_email']):
            errors['admin_email'] = "Invalid email address!"
        if len(postData['admin_phone']) < 10:
            errors['admin_phone'] = "Phone number should be at least 10 characters"
        if len(postData['admin_password']) < 8:
            errors['admin_password'] = "Password should be at least 8 characters"
        if postData['admin_repete_password'] != postData['admin_password']:
            errors['admin_repete_password'] = "Passwords do not match"
        return errors
    
    def login_manager_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid email address!"
        if len(postData['password']) < 8:
            errors['password'] = "Password should be at least 8 characters"
        return errors

# Create your models here.
# the manager teble
# manager can add many imployees
class Manager(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    phone = models.IntegerField()
    password = models.CharField(max_length=255)
    confirm_password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ManagerManager()
    # employees


#--------------------------------------------------------------------EMPLOYEE-----------------------
class EmployeeManager(models.Manager):
    def employee_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(postData['admin_first_name']) < 2:
            errors['admin_first_name'] = "First name should be at least 2 characters"
        if len(postData['admin_last_name']) < 2:
            errors['admin_last_name'] = "Last name should be at least 2 characters"
        if not EMAIL_REGEX.match(postData['admin_email']):
            errors['admin_email'] = "Invalid email address!"
        if len(postData['admin_phone']) < 10:
            errors['admin_phone'] = "Phone number should be at least 10 characters"
        if len(postData['admin_password']) < 8:
            errors['admin_password'] = "Password should be at least 8 characters"
        if postData['admin_repete_password'] != postData['admin_password']:
            errors['admin_repete_password'] = "Passwords do not match"
        return errors
    
    def login_employee_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid email address!"
        if len(postData['password']) < 8:
            errors['admin_password'] = "Password should be at least 8 characters"
        return errors

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

    manager = models.ForeignKey(Manager , related_name="employees", on_delete=models.CASCADE) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = EmployeeManager()
    # products
    # purchasing_invoice
    # sale_orders



#--------------------------------------------------------------------PRODUCT-----------------------
class Product(models.Model):
    product_name = models.CharField(max_length=255)
    quantity = models.IntegerField()
    purchasing_price = models.DecimalField(max_digits=6, decimal_places=2) # 999999.99
    expiry_date  = models.DateField()
    supplier = models.CharField(max_length=255)  # Supplier NAME

    employee = models.ForeignKey(Employee , related_name="products", on_delete=models.CASCADE) # RESTRICT  deleted >>  dont delete the item or ( default="Default", on_delete=models.SET_DEFAULT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # purchasing_invoices
    # sale_orders

#--------------------------------------------------------------------PUECHASING-----------------------
class Purchasing_invoice(models.Model):
    product_name = models.CharField(max_length=255) 
    quantity = models.IntegerField()

    employee = models.ForeignKey(Employee , related_name="purchasing_invoices", on_delete=models.CASCADE) # RESTRICT  deleted >>  dont delete the item or ( default="Default", on_delete=models.SET_DEFAULT)
    products = models.ManyToManyField(Product, related_name="purchasing_invoices")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # products

#--------------------------------------------------------------------SALE_ORDER-----------------------
class Sale_order(models.Model):
    product_name = models.CharField(max_length=255) 
    quantity = models.IntegerField()

    employee = models.ForeignKey(Employee , related_name="sale_orders", on_delete=models.CASCADE) # RESTRICT  deleted >>  dont delete the item or ( default="Default", on_delete=models.SET_DEFAULT)
    products = models.ManyToManyField(Product, related_name="sale_orders")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # products