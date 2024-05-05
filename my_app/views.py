from django.shortcuts import render
# to display the sign-in page
def display_homepage(request):
    return render(request, 'sign-in.html')


def index(request):
    return render(request , 'index.html' )
