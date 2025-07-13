
from csv import reader
from django.http import HttpResponse
from django.shortcuts import render
from Application.models import Platillo, Tipoplatillo
from django.core.files.storage import default_storage

#region CRUD PLATILLOS


def Actualizar_Platillos(request):
    if request.user.is_authenticated:
        try:
            if request.method == "POST":
                platilloname = request.POST.get("Nombre")
                precio = request.POST.get("Precio")
                tipoplatillo = request.POST.get("tipoplatillo")
                print(tipoplatillo)
                estado = request.POST.get("estado")
                descripcion = request.POST.get("Descripcion")
                id_Platillo = request.POST.get("id")
                imagen = request.FILES.get("Imagen")
                print(id_Platillo)
                platillo = Platillo.objects.get(id=id_Platillo)
                print("OBTUVO EL ID")
                platillo.nombreplatillo = platilloname
                tipo = Tipoplatillo.objects.get(id=tipoplatillo)
                platillo.idtipoplatillo = tipo
                platillo.precioplatillo = precio
                platillo.activo = estado
                platillo.descripcionplatillo = descripcion
                if imagen:
                    # Guardar la imagen en el sistema de archivos
                    file_path = default_storage.save('platillos/' + imagen.name, imagen)
                    platillo.imagen_platillo = file_path
                    
                platillo.save()
                return HttpResponse("")
        except Exception as ex:
            print()
            print("#################### E X C E P C I O N ########################")
            print(ex)
            print("########################################################")
            print()
    else:
        # Si no lo ha hecho entonces deberá iniciar sesión
        return reader(request, "login.html")

def DarBajar_Platillo(request):
    if request.user.is_authenticated:
        try:
            if request.method == "POST":
                id = request.POST.get("id")
                print("xdxdxd  "+id)
                platillo = Platillo.objects.get(id=id)
                print("proveedor ------------------------------> " + str(platillo))
                platillo.activo = "Inactivo"
                platillo.save()
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

def Agregar_Platillo(request):
    if request.user.is_authenticated:
        try:
            if request.method == "POST":
                platilloname = request.POST.get("Nombre")
                precio = request.POST.get("Precio")
                tipoplatillo = request.POST.get("tipoplatillo")
                estado = request.POST.get("estado")
                descripcion = request.POST.get("Descripcion")
                imagen = request.FILES.get("Imagen")
                # imagen = request.FILES["Imagen"]

                print("----------------------------------------------")
                print(imagen)
            
                platillo = Platillo()
                platillo.nombreplatillo = platilloname
                tipo = Tipoplatillo.objects.get(id=tipoplatillo)
                platillo.idtipoplatillo = tipo
                platillo.precioplatillo = precio
                platillo.activo = estado
                platillo.descripcionplatillo = descripcion

                if imagen:
                    # Guardar la imagen en el sistema de archivos
                    file_path = default_storage.save('platillos/' + imagen.name, imagen)
                    platillo.imagen_platillo = file_path
                
                platillo.save()
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
#endregion
