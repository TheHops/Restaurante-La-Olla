from django.http import JsonResponse
from django.shortcuts import render

from Application.models import Cargo, Usuario
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

User = get_user_model()

def MiPerfil(request):
    if request.user.is_authenticated:
        try:
            return render(request, "mi_perfil.html", {'Usuario': request.user})
        except Exception as ex:
            print()
            print("#################### E X C E P C I O N ########################")
            print(ex)
            print("########################################################")
            print()
    else:
        # Si no lo ha hecho entonces deberá iniciar sesión
        return render(request, "login.html")