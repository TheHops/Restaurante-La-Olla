#region Personal

import json
from django.http import HttpResponse
from django.shortcuts import render

from Application.models import Cargo, Usuario

def personal(request):
    if request.user.is_authenticated:
        try:
            personal = Usuario.objects.all()
            cargos = Cargo.objects.filter(EsActivo="Activo")

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

def AgregarPersonal(request):
    if request.user.is_authenticated:
        try:
            if request.method == "POST":
                Nombre = request.POST.get("Nombre")
                Apellido = request.POST.get("Apellido")
                usuario = request.POST.get("User")
                passw = request.POST.get("Pass")
                correo = request.POST.get("Correo")
                telefono = request.POST.get("Telefono")
                cargo = request.POST.get("Cargo")
                tipoCargo = Cargo.objects.get(id=cargo)

                nombreUsuario = Usuario.objects.filter(nombreusuario = usuario)
                if not nombreUsuario:

                    personal = Usuario.objects.create_user(
                        nombres=Nombre,
                        apellidos=Apellido,
                        username=usuario,
                        nombreusuario=usuario,
                        password=passw,
                        email=correo,
                        correopers=correo,
                        telefonopers=telefono,
                        idcargo=tipoCargo
                    )

                    # Le damos los privilegios de superusuario en caso de que el usuario sea administrador
                    if cargo == "1":
                        personal.is_staff = True
                    elif cargo == "3":
                        personal.is_staff = True
                        personal.is_superuser = True

                    personal.save()
                    response_data = {'message': '1'} #usuario agregado
                else:
                    response_data = {'message': '0'} #usuario no agregado
                    
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

def ModificarPersonal(request):
    if request.user.is_authenticated:
        try:
            if request.method == "POST":
                Usuario = request.POST.get("User")
                ID = request.POST.get("IDPersonal")
                personal = Usuario.objects.get(id=ID)

                if Usuario == personal.nombreusuario:
                    if personal.activo == 0:
                        nombreUsuario = Usuario.objects.filter(nombreusuario=Usuario).exclude(activo='Inactivo').exists()
                    else:
                        nombreUsuario = False
                else:
                    nombreUsuario = Usuario.objects.filter(nombreusuario=Usuario).exclude(activo='Inactivo').exists()

                if not nombreUsuario:
                    Email = request.POST.get("Correo")
                    Password = request.POST.get("NewPass")
                    Numero = request.POST.get("Telefono")
                    NewCargo = request.POST.get("Cargo")
                    Estado = request.POST.get("Estado")
                    NameUsuario = request.POST.get("NameUsuario")
                    LastNameUsuario = request.POST.get("LastNameUsuario")
                    tipoCargo = Cargo.objects.get(id=NewCargo)
            
                    personal.email = Email
                    personal.correopers = Email
                    personal.telefonopers = Numero
                    personal.idcargo_id = tipoCargo
                    personal.activo = Estado
                    personal.nombres = NameUsuario
                    personal.apellidos = LastNameUsuario
                    if NewCargo == "1":
                        personal.is_staff = True
                    elif NewCargo == "3":
                        personal.is_staff = True
                        personal.is_superuser = True

                    if Password:
                        personal.set_password(Password)

                    if Usuario != personal.nombreusuario and Usuario.objects.filter(nombreusuario=Usuario).exists():
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

def DarBajaPersonal(request):
    if request.user.is_authenticated:
        try:
            if request.method == "POST":
                id = request.POST.get("ID")
                personal = Usuario.objects.get(id=id)
                personal.activo = "Inactivo"
                personal.save()
                return HttpResponse("")
        except Exception as ex:
            print()
            print("#################### E X C E P C I O N ########################")
            print(ex)
            print("########################################################")
            print()
    else:
        # Si no lo ha hecho entonces deberá iniciar sesión
        return render(request, "login.html")
#endregion CRUD PERSONAL
