from django.http import JsonResponse
from django.shortcuts import render

from Application.models import Cargo, Usuario
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

User = get_user_model()

#region Inicio

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

#endregion Inicio

#region EditarPerfil
    
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
            
            return JsonResponse({"status": "ok", "message": "¡Los datos de su perfil fueron modificados con éxito!"})
        except Exception as ex:
            print()
            print("#################### E X C E P C I O N ########################")
            print(ex)
            print("########################################################")
            print()
    else:
        # Si no lo ha hecho entonces deberá iniciar sesión
        return render(request, "login.html")
    
#endregion EditarPerfil

#region EditarPass
    
def CambiarPass (request):
    if request.user.is_authenticated:
        if request.method != "POST":
            return JsonResponse({
                "status": "error",
                "message": "Método no permitido"
            })
        
        try:
            old_pass = request.POST.get("OldPass")
            new_pass = request.POST.get("NewPass")
            verify_pass = request.POST.get("VerifyPass")

            # 🔹 Verificar campos obligatorios
            if not old_pass or not new_pass or not verify_pass:
                return JsonResponse({
                    "status": "error",
                    "message": "Debe completar todos los campos"
                })

            user = request.user

            # 🔹 Verificar contraseña actual
            if not user.check_password(old_pass):
                return JsonResponse({
                    "status": "error",
                    "message": "La contraseña actual es incorrecta"
                })

            # 🔹 Verificar coincidencia
            if new_pass != verify_pass:
                return JsonResponse({
                    "status": "error",
                    "message": "Las contraseñas no coinciden"
                })

            # 🔹 Validar contraseña con Django
            try:
                validate_password(new_pass, user=request.user)
            except ValidationError as e:
                return JsonResponse({
                    "status": "error",
                    "message": " ".join(e.messages)
                })

            # 🔹 Cambiar contraseña
            user = request.user
            user.set_password(new_pass)
            user.DebeCambiarPass = False
            user.save()

            # 🔹 Mantener sesión activa
            update_session_auth_hash(request, user)

            return JsonResponse({
                "status": "ok",
                "message": "¡La contraseña fue cambiada con éxito!"
            })
        except Exception as ex:
            print()
            print("#################### E X C E P C I O N ########################")
            print(ex)
            print("########################################################")
            print()
    else:
        # Si no lo ha hecho entonces deberá iniciar sesión
        return render(request, "login.html")
    
#endregion EditarPass