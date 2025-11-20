#region Personal

import json
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

from Application.models import Cargo, Usuario
from django.views.decorators.http import require_POST
from django.db import transaction

def personal(request):
    if request.user.is_authenticated:
        try:
            personal = Usuario.objects.filter(EsActivo="1")
            cargos = Cargo.objects.filter(EsActivo="1")

            return render(request, "personal.html", {'Personal': personal, 'Cargos': cargos})
        except Exception as ex:
            print()
            print("#################### E X C E P C I O N ########################")
            print(ex)
            print("########################################################")
            print()
    else:
        # Si no lo ha hecho entonces deberá iniciar sesión
        return render(request, "login.html")

def cargo(request):
    if request.user.is_authenticated:
        return render(request, "cargo.html")
    else:
        # Si no lo ha hecho entonces deberá iniciar sesión
        return render(request, "login.html")
#endregion


#region CRUD PERSONAL

#region Agregar personal

@require_POST
def AgregarPersonal(request):
    if not request.user.is_authenticated:
        return render(request, "login.html")

    try:
        nombre = request.POST.get("Nombre", "").strip()
        apellido = request.POST.get("Apellido", "").strip()
        usuario = request.POST.get("User", "").strip()
        passw = request.POST.get("Pass", "")
        correo = request.POST.get("Correo", "")
        telefono = request.POST.get("Telefono", "")
        cargo = request.POST.get("Cargo", "")

        # Validación simple
        if not (nombre and apellido and usuario and passw and cargo):
            return JsonResponse({
                'status': 'error',
                'message': 'Campos obligatorios faltantes.'
            }, status=400)

        # ¿Existe ya el username?
        if Usuario.objects.filter(username=usuario).exists():
            return JsonResponse({
                'status': 'error',
                'message': 'El usuario ya existe.'
            })

        # Obtener cargo
        try:
            tipoCargo = Cargo.objects.get(Id=cargo)
        except Cargo.DoesNotExist:
            return JsonResponse({
                'status': 'error',
                'message': 'El cargo seleccionado no existe.'
            }, status=400)

        # Crear usuario
        personal = Usuario.objects.create_user(
            Nombres=nombre,
            Apellidos=apellido,
            username=usuario,
            password=passw,
            email=correo,
            Telefono=telefono,
            IdCargo=tipoCargo
        )

        # Si el cargo es administrador, dar permisos
        if str(cargo) == "1":
            personal.is_staff = True
            personal.is_superuser = True
            personal.save()

        return JsonResponse({
            'status': 'ok',
            'message': 'Personal agregado correctamente.'
        })

    except Exception as ex:
        print("### ERROR ###")
        print(ex)
        print("#############")

        return JsonResponse({
            'status': 'error',
            'message': 'Error interno en el servidor.'
        }, status=500)
        
#endregion Agregar personal

#region Modificar personal

def ModificarPersonal(request):
    if request.user.is_authenticated:
        try:
            if request.method == "POST":
                usuario = request.POST.get("User")
                id = request.POST.get("IDPersonal")
                personal = Usuario.objects.get(Id=id)

                if usuario == personal.username:
                    if personal.EsActivo == "0":
                        nombreUsuario = Usuario.objects.filter(username=usuario).exclude(EsActivo="0").exists()
                    else:
                        nombreUsuario = False
                else:
                    nombreUsuario = Usuario.objects.filter(username=usuario).exclude(EsActivo='0').exists()

                if not nombreUsuario:
                    email = request.POST.get("Correo")
                    password = request.POST.get("NewPass")
                    numero = request.POST.get("Telefono")
                    newCargo = request.POST.get("Cargo")
                    estado = request.POST.get("Estado")
                    nameUsuario = request.POST.get("NameUsuario")
                    lastNameUsuario = request.POST.get("LastNameUsuario")
                    tipoCargo = Cargo.objects.get(Id=newCargo)
            
                    personal.email = email
                    personal.Telefono = numero
                    personal.IdCargo = tipoCargo
                    personal.EsActivo = estado
                    personal.Nombres = nameUsuario
                    personal.Apellidos = lastNameUsuario
                    if newCargo == "1":
                        personal.is_staff = True
                        personal.is_superuser = True

                    if password:
                        personal.set_password(password)

                    if Usuario != personal.username and Usuario.objects.filter(username=Usuario).exists():
                        response_data = {'message': '0'}  # nombreUsuario ya existe en otro registro
                    else:
                        personal.save()
                        response_data = {'message': '1'}  # usuario modificado correctamente
                else:
                    response_data = {'message': '3'}  # nombreUsuario inactivo

                return HttpResponse(json.dumps(response_data), content_type="application/json")
        except Exception as ex:
            print()
            print("#################### E X C E P C I O N ########################")
            print(ex)
            print("########################################################")
            print()
    else:
        # Si no lo ha hecho entonces deberá iniciar sesión
        return render(request, "login.html")
    
#endregion Modificar personal

#region Eliminar personal

def DarBajaPersonal(request):
    if not request.user.is_authenticated:
        return render(request, "login.html")

    if request.method == "POST":
        try:
            id_personal = request.POST.get("ID")

            if not id_personal:
                return JsonResponse({'status': 'error', 'message': 'ID no proporcionado'}, status=400)

            personal = Usuario.objects.get(Id=id_personal)
            personal.EsActivo = "0"
            personal.save()

            return JsonResponse({'status': 'success', 'message': 'Usuario dado de baja correctamente'})
        
        except Usuario.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Usuario no encontrado'}, status=404)

        except Exception as ex:
            print("\n#################### EXCEPCIÓN ########################")
            print(ex)
            print("########################################################\n")
            return JsonResponse({'status': 'error', 'message': 'Error interno del servidor'}, status=500)
    
    return JsonResponse({'status': 'error', 'message': 'Método no permitido'}, status=405)

#endregion Eliminar personal

#endregion CRUD PERSONAL
