from django.shortcuts import render ,redirect
from . import models
from django.contrib import messages
import bcrypt
from datetime import datetime , timedelta
import datetime




# to display the sign-in page
def about_us(request):
    return render(request, 'about_us.html')




def display_homepage(request):
    return render(request, 'sign-in.html')

def index(request):
    if 'manager_id' in request.session:
        context = {           
            'sixmonthesproducts': models.get_six_monthes_products(),
            'out_stock':models.out_of_stock(),
            'count':models.count_out_stock(),

            }
        return render(request , 'index.html' , context)
    else:
        return redirect('/')
    

def sign_up(request):
    return render(request , 'sign-up.html' )

# if anyone want to Sign is
def sign_in(request):
    if request.method == 'POST':
        # if he is an EMPLOYEE
        if request.POST['account_type'] == "1" : # Emoployee
            errors = models.Employee.objects.login_employee_validator(request.POST)
            if len(errors) > 0:
                for key, value in errors.items():
                    messages.error(request, value )
                return redirect('/')
            else:
                employee_email = request.POST['email'] # here we get the email thet ENSERTED
                employee_password = request.POST['password'] # here we get the password thet ENSERTED
                employee = models.Employee.objects.filter(email=employee_email) # here we get the EMPLOYEE by the email from DB
                if employee: # here we check if the EMPLOYEE exist
                    employee_user = employee[0] # here we get the EMPLOYEE from the list
                    if bcrypt.checkpw(employee_password.encode(), employee_user.password.encode()): # here we chick the password 
                        request.session['employee_id'] = employee_user.id
                        return redirect('/employye_dashboard')
                    else:
                        messages.error(request, "Incorrect Password")
                        # messages.error(request, value , extra_tags = 'admin_login' )
                        return redirect('/')
                messages.error(request, "Email is incorrect")
                return redirect('/')
        # if he is a MANAGER
        else:
            if request.POST['account_type'] == "2" : # Manager
                errors = models.Manager.objects.login_manager_validator(request.POST)
                if len(errors) > 0:
                    for key, value in errors.items():
                        messages.error(request, value )
                    return redirect('/')
                else:
                    manager_email = request.POST['email'] # here we get the email thet ENSERTED
                    manager_password = request.POST['password'] # here we get the password thet ENSERTED
                    manager = models.Manager.objects.filter(email=manager_email) # here we get the MANAGER by the email from DB
                    if manager: # here we check if the MANAGER exist
                        manager_user = manager[0] # here we get the MANAGER from the list
                        #ADDING MANAGER FROME ADMIN
                        if manager_password == manager_user.password :
                            request.session['manager_id'] = manager_user.id
                            return redirect('/index')
                        else:
                            messages.error(request, "Incorrect Password")
                            # messages.error(request, value , extra_tags = 'admin_login' )
                            return redirect('/')
                    messages.error(request, "Email is incorrect")
    else:
        return redirect('/')

                #     if bcrypt.checkpw(manager_password.encode(), manager_user.password.encode()): # here we chick the password 
                #         request.session['manager_id'] = manager_user.id
                #         return redirect('/index')
                #     else:
                #         messages.error(request, "Incorrect Password")
                #         # messages.error(request, value , extra_tags = 'admin_login' )
                #         return redirect('/')
                # messages.error(request, "Email is incorrect")
                # return redirect('/')
    return redirect('/')

def logout(request):
    request.session.clear()
    return redirect('/')

def display_stock_for_manager(request):
    context={
        'products': models.get_all_products(),
        'today': datetime.today().date(),
        'expiry_range': datetime.today().date() + timedelta(days=6*30),
    }
    return render(request, 'stock_manager.html',context)


def add_new_employee(request):
    errors = models.Employee.objects.employee_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/employees')
    else:
        manager = request.session['manager_id']
        emp_f_name = request.POST['f_name']
        emp_l_name = request.POST['l_name']
        emp_emeil = request.POST['email']
        emp_DOB = request.POST['DOB']
        emp_password = request.POST['password']
        emp_conf_password = request.POST['c_password']
        #hash-----Passwords-------
        pw_hash = bcrypt.hashpw(emp_password.encode(), bcrypt.gensalt()).decode()
        pw_hash_confirm = bcrypt.hashpw(emp_conf_password.encode(), bcrypt.gensalt()).decode()
        #hash-----Passwords-------
        models.add_employee(emp_f_name, emp_l_name, emp_emeil, emp_DOB, pw_hash, pw_hash_confirm , manager )
        messages.success(request, "Successfully added an employee!" , extra_tags = 'add_employee')
        return redirect('/employees')

def display_employees(request):
    # if the manad=egr not in the loged on
    if 'manager_id' not in request.session:
        return redirect('/index')
    else:
        context = {
            'employees': models.get_all_employees()
        }
        return render (request, 'profile.html', context )



def display_employee_dashboard(request):
    if 'employee_id' not in request.session:
        return redirect('/index')
    else:
        context = {
            'products': models.get_all_products(),
            'employee': models.get_employee_by_id(request.session['employee_id'])
        }
        return render(request, 'tables.html' , context )



def add_new_product(request):
    errors = models.Product.objects.product_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/employye_dashboard')
    else:
        employee = request.session['employee_id']
        product_name = request.POST['product_name']
        quantity = request.POST['quantity']
        purchasing_price = request.POST['purchasing_price']
        expiry_date = request.POST['expiry_date']
        supplier = request.POST['supplier']
        models.add_product(product_name, quantity, purchasing_price, expiry_date, supplier, employee)
        messages.success(request, "Successfully added a product!", extra_tags = 'add_product')
        return redirect('/employye_dashboard')
sale_order = []

def display_sales(request):
    context = {
            'sale_order': sale_order,
            'products': models.get_all_products(),
            'orders' : models.get_all_sales_orders(),
            'employee': models.get_employee_by_id(request.session['employee_id'])
        }
    return render(request , 'sale_orders.html', context )

def display_purchases(request):
    context = {
            'purchases_order': purchases_order,
            'products': models.get_all_products(),#--------------------------------------------Mai
            'invoices' : models.get_all_invoices(),
            'employee': models.get_employee_by_id(request.session['employee_id']),#--------------------------------------------Mai
        }
    return render(request , 'purchase_invoices.html' ,context)

def delete_product(request):
    models.delete_clicked_product(request)
    return redirect('/employye_dashboard')
#____________________________________SALE___________________________________
def add_product_to_sale(request):
    product_name = request.POST['product_name']
    quantity = request.POST['quantity']
    product_id = models.Product.objects.get(product_name=product_name).id
    sale_order.append ( {'product_name': product_name , 'product_id': product_id , 'quantity': quantity } )
    return redirect('/sales')
    
def submet_sale_order(request):
    employee_id = request.session['employee_id']
    models.create_sale_order(employee_id) #---------CREATE the invoise------- 1
    for key in sale_order :
        product_name = key.get('product_name')
        product_id = key.get('product_id')
        quantity = key.get('quantity')
                                                
        models.add_sale_relation(product_id)#---------GET the product-----AMD------ADD the product------- 4

        models.add_product_to_sale( product_id, quantity )
        
    sale_order.clear()
    return redirect('/sales')
#____________________________________SALE___________________________________

purchases_order = []
#____________________________________PURCHASE___________________________________
def add_product_to_purchase(request):
    product_name = request.POST['product_name']
    quantity = request.POST['quantity']
    product_id = models.Product.objects.get(product_name=product_name).id
    purchases_order.append ( {'product_name': product_name, 'product_id': product_id , 'quantity': quantity } )
    return redirect('/purchases')
    
def submet_purchase_order(request):
    employee_id = request.session['employee_id']
    models.create_purchase_order(employee_id) #---------CREATE the invoise------- 1
    for key in purchases_order :
        product_name = key.get('product_name')
        product_id = key.get('product_id')
        quantity = key.get('quantity')
        
        models.add_purchase_relation(product_id)#---------GET the product-----AMD------ADD the product------- 4
        models.add_product_to_purchase(product_id, quantity)
    purchases_order.clear()
    return redirect('/purchases')
#____________________________________PURCHASE___________________________________



def display_employee_reports(request):
    context = {
        'products': models.get_all_products(),
        'today': datetime.today().date(),
        'expiry_range': datetime.today().date() + timedelta(days=6*30),
        'employee': models.get_employee_by_id(request.session['employee_id'])
    }
    return render (request, 'employee_reports.html', context)

def view_sale_order(request, id):#--------------------------------------------Mai
    context={
        'order': models.get_sale_order(id),

    }
    return render(request, 'view_sale_order.html',context)

def display_edit_form(request,id):
    context={
        'products': models.get_all_products(),
        'product':models.get_product(id),
    }
    return render(request, 'edit_product.html',context)

def update_product(request,id):
    errors = models.Product.objects.product_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f'/edit_product/{id}')
    else:
        models.update_selected_product(request,id)

    return redirect('/employye_dashboard')#--------------------------------------------Mai


def get_date_time():
    return datetime.date.today()# used in models line 69