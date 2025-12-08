#region Personal

from django.http import JsonResponse
from django.shortcuts import render

from Application.models import Cargo, Usuario
from django.views.decorators.http import require_POST
from django.contrib.auth import get_user_model

User = get_user_model()

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

        print(correo)

        # Crear usuario
        personal = Usuario.objects.create(
            Nombres=nombre,
            Apellidos=apellido,
            username=usuario,
            password=passw,
            email=correo,
            Telefono=telefono,
            IdCargo=tipoCargo
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
        print("### ERROR ###")
        print(ex)
        print("#############")

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
            if Usuario.objects.filter(email=correo).exists():
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
        print("### ERROR EN ModificarPersonal ###")
        print(ex)
        return JsonResponse({
            'status': 'error',
            'message': 'Error interno en el servidor.'
        }, status=500)
    
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

            return JsonResponse({'status': 'ok', 'message': '¡Personal dado de baja exitosamente!'})
        
        except Usuario.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Usuario no encontrado'}, status=404)

        except Exception as ex:
            print("\n#################### EXCEPCIÓN ########################")
            print(ex)
            print("########################################################\n")
            return JsonResponse({'status': 'error', 'message': 'Error interno del servidor'}, status=500)
    
    return JsonResponse({'status': 'error', 'message': 'Método no permitido'}, status=405)

#endregion Eliminar personal

#region Filtrar personal

def filtrar_personal(request):
    if not request.user.is_authenticated:
        return render(request, "login.html")

    ver_eliminados = request.GET.get("verEliminados") == "1"

    if ver_eliminados:
        personal = Usuario.objects.order_by("Id")
    else:
        personal = Usuario.objects.filter(EsActivo="1").order_by("Id")

    contexto = {
        "Personal": personal,
        "VerEliminados": "1" if ver_eliminados else "0"
    }

    return render(request, "personal_filtrados.html", contexto)

#endregion Filtrar personal

#endregion CRUD PERSONAL
