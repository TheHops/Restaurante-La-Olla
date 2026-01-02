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
    
def EditarDatosPerfil (request):
    if request.user.is_authenticated:
        if request.method != "POST":
            return JsonResponse({
                "status": "error",
                "message": "Método no permitido"
            })
        
        try:
            # Se editarán los datos de perfil (Solamente el correo, teléfono y nombre de usuario)
            # Para el correo y nombre de usuario hay que verificar que no estén repetidos con otro usuario
            usuario = request.user

            # Obtener datos enviados
            email = request.POST.get("txtCorreoEditarPerfil", "").strip()
            telefono = request.POST.get("txtTelefonoEditarPerfil", "").strip()
            username = request.POST.get("txtUserNameEditarPerfil", "").strip()

            # Email repetido (excluyendo al usuario actual)
            if email:
                existe_email = User.objects.filter(
                    email=email
                ).exclude(Id=usuario.Id).exists()

                if existe_email:
                    return JsonResponse({
                        "status": "error",
                        "message": "El correo ya está registrado por otro usuario"
                    })

            # Username repetido (excluyendo al usuario actual)
            if username:
                existe_username = User.objects.filter(
                    username=username
                ).exclude(Id=usuario.Id).exists()

                if existe_username:
                    return JsonResponse({
                        "status": "error",
                        "message": "El nombre de usuario ya está en uso"
                    })
            elif username.strip() == "":
                return JsonResponse({
                    "status": "error",
                    "message": "El nombre de usuario no debe estar vacío"
                })

            # ===============================
            # ACTUALIZACIÓN DE DATOS
            # ===============================

            usuario.email = email if email else None
            usuario.Telefono = telefono if telefono else None
            usuario.username = username

            usuario.save()
            
            return JsonResponse({"status": "ok", "message": "Los datos de su perfil fueron modificados con éxito"})
        except Exception as ex:
            print()
            print("#################### E X C E P C I O N ########################")
            print(ex)
            print("########################################################")
            print()
    else:
        # Si no lo ha hecho entonces deberá iniciar sesión
        return render(request, "login.html")