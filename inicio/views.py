from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

@login_required
def mostrar_menu(request):
    return render(request, 'menu.html')

def custom_logout(request):
    logout(request)
    return redirect('login')