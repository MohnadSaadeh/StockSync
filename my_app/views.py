from django.shortcuts import render ,redirect
from . import models
from django.contrib import messages
import bcrypt



# to display the sign-in page
def display_homepage(request):
    return render(request, 'sign-in.html')

def index(request):
    return render(request , 'index.html' )

def sign_up(request):
    return render(request , 'sign-up.html' )










# if anyone want to Sign is
def sign_in(request):
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
                    return redirect('/index')
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