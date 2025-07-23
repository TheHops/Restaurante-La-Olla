#region Personal

import json
from django.http import HttpResponse
from django.shortcuts import render

from Application.models import Cargo, Usuario

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

def AgregarPersonal(request):
    if request.user.is_authenticated:
        try:
            if request.method == "POST":
                nombre = request.POST.get("Nombre")
                apellido = request.POST.get("Apellido")
                usuario = request.POST.get("User")
                passw = request.POST.get("Pass")
                correo = request.POST.get("Correo")
                telefono = request.POST.get("Telefono")
                cargo = request.POST.get("Cargo")
                tipoCargo = Cargo.objects.get(Id=cargo)

                # se verifica si existe buscandolo
                nombreUsuario = Usuario.objects.filter(username = usuario)
                
                if not nombreUsuario:

                    personal = Usuario.objects.create_user(
                        Nombres=nombre,
                        Apellidos=apellido,
                        username=usuario,
                        password=passw,
                        email=correo,
                        Telefono=telefono,
                        IdCargo=tipoCargo
                    )
                    
                    print(personal)

                    # Le damos los privilegios de superusuario en caso de que el usuario sea administrador
                    if cargo == "1":
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

def DarBajaPersonal(request):
    if request.user.is_authenticated:
        try:
            if request.method == "POST":
                id = request.POST.get("ID")
                personal = Usuario.objects.get(Id=id)
                personal.EsActivo = "0"
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
