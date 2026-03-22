#region Personal

import traceback

from django.http import JsonResponse
from django.shortcuts import render, redirect

from Application.models import Cargo, Usuario
from django.views.decorators.http import require_POST
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

import random
import string

User = get_user_model()

def personal(request):
    if request.user.is_authenticated:
        if request.user.IdCargo.Nombre == "Armador" or request.user.IdCargo.Nombre == "Mesero" or request.user.IdCargo.Nombre == "Cajero":
            return redirect("/")
        
        try:
            personal = Usuario.objects.filter(EsActivo="1")
            cargos = Cargo.objects.filter(EsActivo="1")

            return render(request, "personal.html", {'Personal': personal, 'Cargos': cargos, 'User': request.user})
        except Exception as ex:
            print("\n\n############### E X C E P C I Ó N ###############")
            print(traceback.format_exc())
            print("#####################################################\n\n")
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
    
    if request.user.IdCargo.Nombre == "Armador" or request.user.IdCargo.Nombre == "Mesero" or request.user.IdCargo.Nombre == "Cajero":
        return redirect("/")

    try:
        nombre = request.POST.get("Nombre", "").strip()
        apellido = request.POST.get("Apellido", "").strip()
        usuario = request.POST.get("User", "").strip()
        passw = request.POST.get("Pass", "")
        correo = request.POST.get("Correo")
        telefono = request.POST.get("Telefono", "")
        cargo = request.POST.get("Cargo", "")

        # Validación simple
        if not (nombre and apellido and usuario and passw and cargo):
            return JsonResponse({
                'status': 'error',
                'message': 'Campos obligatorios faltantes'})
         
        # Validar contenido de correo   
        if correo is not None and correo.strip() == "":
            correo = None

        # Validar correo único si no es NULL
        if correo is not None:
            if Usuario.objects.filter(email=correo).exists():
                return JsonResponse({
                'status': 'error',
                'message': 'El correo ya está registrado en otra cuenta'
            })

        # ¿Existe ya el username?
        if Usuario.objects.filter(username=usuario).exists():
            return JsonResponse({
                'status': 'error',
                'message': 'El nombre de usuario ya existe'})

        # Obtener cargo
        try:
            tipoCargo = Cargo.objects.get(Id=cargo)
        except Cargo.DoesNotExist:
            return JsonResponse({
                'status': 'error',
                'message': 'El cargo seleccionado no existe'})

        # Crear usuario
        personal = Usuario.objects.create(
            Nombres=nombre,
            Apellidos=apellido,
            username=usuario,
            password=passw,
            email=correo,
            Telefono=telefono,
            IdCargo=tipoCargo,
            DebeCambiarPass=True
        )
        personal.set_password(passw)
        personal.save()

        # Si el cargo es administrador, dar permisos
        if str(cargo) == "1":
            personal.is_staff = True
            personal.save()
            
        # if correo == "" or None:
        #     personal.email = None
        #     personal.save()

        return JsonResponse({
            'status': 'ok',
            'message': '¡Personal agregado exitosamente!'
        })

    except Exception as ex:
        print("\n\n############### E X C E P C I Ó N ###############")
        print(traceback.format_exc())
        print("#####################################################\n\n")

        return JsonResponse({
            'status': 'error',
            'message': 'Error interno en el servidor'
        }, status=500)
        
#endregion Agregar personal

#region Modificar personal

@require_POST
def ModificarPersonal(request):
    if not request.user.is_authenticated:
        return render(request, "login.html")
    
    if request.user.IdCargo.Nombre == "Armador" or request.user.IdCargo.Nombre == "Mesero" or request.user.IdCargo.Nombre == "Cajero":
        return redirect("/")

    try:
        usuario = request.POST.get("User", "").strip()
        personal_id = request.POST.get("IDPersonal")
        correo = request.POST.get("Correo", "")
        new_pass = request.POST.get("NewPass", "")
        telefono = request.POST.get("Telefono", "")
        cargo = request.POST.get("Cargo", "")
        estado = request.POST.get("Estado", "")
        nombres = request.POST.get("NameUsuario", "").strip()
        apellidos = request.POST.get("LastNameUsuario", "").strip()

        # Obtener registro
        try:
            personal = Usuario.objects.get(Id=personal_id)
        except Usuario.DoesNotExist:
            return JsonResponse({
                'status': 'error',
                'message': 'El usuario no existe'
            })
            
        # Validar contenido de correo   
        if correo is not None and correo.strip() == "":
            correo = None

        # Validar correo único si no es NULL
        if correo is not None:
            if Usuario.objects.filter(email=correo).exclude(Id=personal_id).exists():
                return JsonResponse({
                'status': 'error',
                'message': 'El correo ya está registrado en otra cuenta'})

        # Si cambia el username, validar que no exista otro igual
        if usuario != personal.username:
            if Usuario.objects.filter(username=usuario).exclude(Id=personal_id).exists():
                return JsonResponse({
                    'status': 'error',
                    'message': 'El nombre de usuario ya existe'
                })

        # Obtener cargo
        try:
            tipoCargo = Cargo.objects.get(Id=cargo)
        except Cargo.DoesNotExist:
            return JsonResponse({
                'status': 'error',
                'message': 'El cargo seleccionado no existe'
            })

        # Aplicar cambios
        personal.username = usuario
        personal.email = correo
        personal.Telefono = telefono
        personal.IdCargo = tipoCargo
        personal.EsActivo = estado
        personal.Nombres = nombres
        personal.Apellidos = apellidos

        # Asignar permisos si es admin
        if str(cargo) == "1":
            personal.is_staff = True
            personal.is_superuser = True
        else:
            personal.is_staff = False
            personal.is_superuser = False

        # Solo si ingresó nueva contraseña
        if new_pass.strip():
            personal.set_password(new_pass)

        personal.save()

        return JsonResponse({
            'status': 'ok',
            'message': '¡Personal modificado exitosamente!'
        })

    except Exception as ex:
        print("\n\n############### E X C E P C I Ó N ###############")
        print(traceback.format_exc())
        print("#####################################################\n\n")
        
        return JsonResponse({
            'status': 'error',
            'message': 'Error interno en el servidor.'
        }, status=500)
    
#endregion Modificar personal

#region Eliminar personal

def DarBajaPersonal(request):
    if not request.user.is_authenticated:
        return render(request, "login.html")
    
    if request.user.IdCargo.Nombre == "Armador" or request.user.IdCargo.Nombre == "Mesero" or request.user.IdCargo.Nombre == "Cajero":
        return redirect("/")

    if request.method == "POST":
        try:
            id_personal = request.POST.get("ID")

            if not id_personal:
                return JsonResponse({'status': 'error', 'message': 'ID no proporcionado'})

            personal = Usuario.objects.get(Id=id_personal)
            personal.EsActivo = "0"
            personal.save()

            return JsonResponse({'status': 'ok', 'message': '¡Personal dado de baja exitosamente!'})
        
        except Usuario.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Usuario no encontrado'})

        except Exception as ex:
            print("\n\n############### E X C E P C I Ó N ###############")
            print(traceback.format_exc())
            print("#####################################################\n\n")
            
            return JsonResponse({'status': 'error', 'message': 'Error interno del servidor'})
    
    return JsonResponse({'status': 'error', 'message': 'Método no permitido'})

#endregion Eliminar personal

#region Restablecer contraseña

def generar_pass_temporal():
    letras = string.ascii_uppercase   # ABCDE...
    numeros = string.digits           # 0123456789
    especiales = "!@#$%^&*()_+-=<>?"

    # Construcción en el orden exacto solicitado
    parte1 = random.choice(letras) + random.choice(letras)    # 2 letras mayúsculas
    parte2 = random.choice(numeros) + random.choice(numeros)  # 2 números
    parte3 = random.choice(letras) + random.choice(letras)    # 2 letras mayúsculas
    parte4 = random.choice(numeros)                            # 1 número
    parte5 = random.choice(especiales)                         # 1 carácter especial

    return parte1 + parte2 + parte3 + parte4 + parte5

def RestablecerPass(request):
    if not request.user.is_authenticated:
        return render(request, "login.html")
    
    if request.user.IdCargo.Nombre == "Armador" or request.user.IdCargo.Nombre == "Mesero" or request.user.IdCargo.Nombre == "Cajero":
        return redirect("/")

    if request.method == "POST":
        try:
            id_personal = request.POST.get("ID")

            if not id_personal:
                return JsonResponse({'status': 'error', 'message': 'ID no proporcionado'})

            # Buscar al usuario
            usuario = Usuario.objects.get(Id=id_personal)

            # Generar contraseña temporal
            nueva_pass = generar_pass_temporal()

            # Guardarla en el usuario (encriptada)
            usuario.password = make_password(nueva_pass)
            usuario.DebeCambiarPass = True
            usuario.save()

            return JsonResponse({'status': 'ok', 'message': '¡Contraseña restablecida exitosamente!', 'new_pass': nueva_pass})
        
        except Usuario.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Usuario no encontrado'})

        except Exception as ex:
            print("\n\n############### E X C E P C I Ó N ###############")
            print(traceback.format_exc())
            print("#####################################################\n\n")
            
            return JsonResponse({'status': 'error', 'message': 'Error interno del servidor'})
    
    return JsonResponse({'status': 'error', 'message': 'Método no permitido'})

#endregion Restablecer contraseña

#region Filtrar personal

def filtrar_personal(request):
    if not request.user.is_authenticated:
        return render(request, "login.html")
    
    roles_restringidos = ["Armador", "Mesero", "Cajero"]
    if request.user.IdCargo.Nombre in roles_restringidos:
        return redirect("/")
    
    ver_eliminados = request.GET.get("verEliminados") == "1"

    queryset = Usuario.objects.exclude(Id=request.user.Id)

    if ver_eliminados:
        personal = queryset.order_by("Id")
    else:
        # Filtramos por activos sobre el queryset que ya excluyó al usuario actual
        personal = queryset.filter(EsActivo="1").order_by("Id")

    contexto = {
        "Personal": personal,
        "VerEliminados": "1" if ver_eliminados else "0"
    }

    return render(request, "personal_filtrados.html", contexto)

#endregion Filtrar personal

#endregion CRUD PERSONAL
