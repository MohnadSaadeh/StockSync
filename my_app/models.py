from django.db import models
from django.db.models import F, ExpressionWrapper, FloatField ,DecimalField
import re
import datetime
from datetime import datetime , timedelta

from . import views


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

def get_manager(id):#--------------------------------------------Mai
    return Manager.objects.get(id=id)
    
#--------------------------------------------------------------------EMPLOYEE-----------------------
class EmployeeManager(models.Manager):
    def employee_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(postData['f_name']) < 2:
            errors['f_name'] = "First name should be at least 2 characters"
        if len(postData['l_name']) < 2:
            errors['l_name'] = "Last name should be at least 2 characters"
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid email address!"
        if postData['DOB'] == "":
            errors['DOB'] = "Please enter a date"
        if postData['DOB'] > str(datetime.date.today()):
            errors['DOB'] = "Date should be in the past"
        if len(postData['password']) < 8:
            errors['password'] = "Password should be at least 8 characters"
        if postData['c_password'] != postData['password']:
            errors['c_password'] = "Passwords not match"
        return errors
    
    def login_employee_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid email address!"
        if len(postData['password']) < 8:
            errors['c_password'] = "Password should be at least 8 characters"
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

def add_employee(f_name, l_name, email, DOB, password, confirm_password ,manager_id ):
    manager = Manager.objects.get(id=manager_id)
    Employee.objects.create(first_name=f_name, last_name=l_name, email=email, DOB=DOB, password=password, confirm_password=confirm_password , manager = manager )
def get_all_employees():
    return Employee.objects.all()

def get_employee_by_id(id):
    return Employee.objects.get(id=id)






#--------------------------------------------------------------------PRODUCT-----------------------
class ProductManager(models.Manager):
    def product_validator(self, postData):
        errors = {}
        if len(postData['product_name']) < 2:
            errors['product_name'] = "Product name should be at least 2 characters"
        if postData['quantity'] == "":
            errors['quantity'] = "Please enter a quantity"
        if postData['purchasing_price'] == "":
            errors['purchasing_price'] = "Please enter a purchasing price"
        if postData['expiry_date'] == "":
            errors['expiry_date'] = "Please enter an expiry date"
        if postData['expiry_date'] < str(datetime.today().date()):
            errors['expiry_date'] = "Expiry date should be in the future"
        if postData['supplier'] == "":
            errors['supplier'] = "Please enter a supplier"
        return errors

class Product(models.Model):
    product_name = models.CharField(max_length=255)
    quantity = models.IntegerField()
    purchasing_price = models.DecimalField(max_digits=6, decimal_places=2) # 999999.99
    expiry_date  = models.DateField()
    supplier = models.CharField(max_length=255)  # Supplier NAME

    employee = models.ForeignKey(Employee , related_name="products", on_delete=models.CASCADE) # RESTRICT  deleted >>  dont delete the item or ( default="Default", on_delete=models.SET_DEFAULT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ProductManager()
    # purchasing_invoices
    # sale_orders

def get_all_products():
    return Product.objects.all()

def get_product_expired():
    return Product.objects.filter(expiry_date__lt=datetime.date.today())

def delete_clicked_product(request):
    product=Product.objects.get(id=request.POST['product_id'])
    return product.delete()

def get_product(id):#--------------------------------------------Mai
    return Product.objects.get(id=id)

def update_selected_product(request,id):

    product=Product.objects.get(id=id)
    product.product_name=request.POST['product_name']
    product.quantity=request.POST['quantity']
    product.purchasing_price=request.POST['purchasing_price']
    product.expiry_date=request.POST['expiry_date']
    product.supplier=request.POST['supplier']
    product.employee=Employee.objects.get(id=request.session['employee_id'])

    product.save()

def out_of_stock():
    return Product.objects.filter(quantity=0)

def count_out_stock():
    return Product.objects.filter(quantity=0).count()#--------------------------------------------Mai


#--------------- not used -------------------
def get_six_monthes():
    today = datetime.today().date()
    six_months_later = today + timedelta(days=6*30)  # Assuming 30 days per month
    return Product.objects.filter(expiry_date__range=[today, six_months_later]).order_by('expiry_date')
#--------------- not used -------------------

def add_product(product_name, quantity, purchasing_price, expiry_date, supplier, employee_id):
    employee = Employee.objects.get(id=employee_id)
    Product.objects.create(product_name=product_name, quantity=quantity, purchasing_price=purchasing_price, expiry_date=expiry_date, supplier=supplier, employee = employee)
# this function return the products and 
# the total cost of each product 
# (purchasing_price * quantity)
# by adding a new field called total_cost
# with the Product.objects.annotate
def get_six_monthes_products():
    today = datetime.today().date()
    six_months_later = today + timedelta(days=6*30)
    products_with_total_cost = Product.objects.annotate(
        total_cost=F('purchasing_price') * F('quantity')
        ).order_by('expiry_date').filter(expiry_date__range=[today, six_months_later])
    return products_with_total_cost




#--------------------------------------------------------------------PUECHASING-----------------------
class Purchasing_invoice(models.Model):

    # product_name = models.CharField(max_length=255)
    # quantity = models.IntegerField()

    employee = models.ForeignKey(Employee , related_name="purchasing_invoices", on_delete=models.CASCADE) # RESTRICT  deleted >>  dont delete the item or ( default="Default", on_delete=models.SET_DEFAULT)
    products = models.ManyToManyField(Product, related_name="purchasing_invoices")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # products
def get_all_invoices():
    return Purchasing_invoice.objects.all()

#--------------------------------------------------------------------SALE_ORDER-----------------------
class Sale_order(models.Model):

    # product_name = models.CharField(max_length=255) 
    # quantity = models.IntegerField()

    employee = models.ForeignKey(Employee , related_name="sale_orders", on_delete=models.CASCADE) # RESTRICT  deleted >>  dont delete the item or ( default="Default", on_delete=models.SET_DEFAULT)
    products = models.ManyToManyField(Product, related_name="sale_orders")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # products

#---------------------Sale--------------------
def create_sale_order(employee_id):
    employee = Employee.objects.get(id=employee_id)
    return Sale_order.objects.create(employee = employee) # create the invoice

def add_sale_relation(product_id):#------------------------ add the product to the invoice
    product = Product.objects.get(id=product_id)
    sale_order = Sale_order.objects.last()
    return sale_order.products.add(product)

# this is to sale a product
def add_product_to_sale( product_id, quantity ): #--------- minimize the quantity of the product
    product = Product.objects.get(id=product_id)
    product.quantity -= int(quantity)
    return product.save()
#--------------------Sale------------------------





#--------------------purchase--------------------
def create_purchase_order(employee_id):
    employee = Employee.objects.get(id=employee_id)
    return Purchasing_invoice.objects.create(employee = employee) # craete the invoice

def add_purchase_relation(product_id): #--------------------------- add the product to the invoice
    product = Product.objects.get(id=product_id)
    purchase_invoice = Purchasing_invoice.objects.last()
    return purchase_invoice.products.add(product)

def add_product_to_purchase(product_id, quantity): #--------------- maximize the quantity of the product
    product = Product.objects.get(id=product_id)
    product.quantity += int(quantity)
    return product.save() 
#--------------------purchase--------------------


# this is to purchase a product
def get_all_sales_orders():#--------------------------------------------Mai
    return Sale_order.objects.all()

def get_sale_order(id):#--------------------------------------------Mai
    return Sale_order.objects.get(id=id)