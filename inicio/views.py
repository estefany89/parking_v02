from django.shortcuts import render

def mostrar_menu(request):
    return render(request, 'menu.html')