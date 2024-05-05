from django.shortcuts import render

def display_homepage(request):
    return render(request, 'sign-in.html')
