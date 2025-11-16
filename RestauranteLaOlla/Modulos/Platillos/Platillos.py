
from csv import reader
import traceback
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from Application.models import Platillo, TipoPlatillo
from django.core.files.storage import default_storage

#region CRUD PLATILLOS

#region ActualizarPlatillos
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
                platillo = Platillo.objects.get(Id=id_Platillo)
                print("OBTUVO EL ID")
                platillo.Nombre = platilloname
                tipo = TipoPlatillo.objects.get(Id=tipoplatillo)
                platillo.IdTipoPlatillo = tipo
                platillo.Precio = precio
                platillo.EsActivo = estado
                platillo.Descripcion = descripcion
                if imagen:
                    # Guardar la imagen en el sistema de archivos
                    file_path = default_storage.save('platillos/' + imagen.name, imagen)
                    platillo.ImagenUrl = file_path
                    
                platillo.save()
                return HttpResponse("")
        except Exception as ex:
            print("\n############### EXCEPCIÓN ###############")
            print(traceback.format_exc())
            print("#########################################\n")
            return JsonResponse({'error': str(ex)}, status=500)
    else:
        # Si no lo ha hecho entonces deberá iniciar sesión
        return reader(request, "login.html")
    
#endregion ActualizarPlatillos

#region EliminarPlatillos

def DarBaja_Platillo(request):
    if not request.user.is_authenticated:
        return reader(request, "login.html")

    try:
        if request.method == "POST":
            id_platillo = request.POST.get("id")

            if not id_platillo:
                return JsonResponse({
                    'status': 'error',
                    'message': 'ID de platillo no proporcionado.'
                }, status=400)

            try:
                platillo = Platillo.objects.get(Id=id_platillo)
            except Platillo.DoesNotExist:
                return JsonResponse({
                    'status': 'error',
                    'message': 'El platillo no existe.'
                }, status=404)

            platillo.EsActivo = "0"
            platillo.save()

            return JsonResponse({
                'status': 'ok',
                'message': 'Platillo dado de baja correctamente.'
            })

        return JsonResponse({
            'status': 'error',
            'message': 'Método no permitido.'
        }, status=405)

    except Exception as ex:
        print("\n######## EXCEPCIÓN ########")
        print(ex)
        print("###########################\n")

        return JsonResponse({
            'status': 'error',
            'message': 'Error interno del servidor.'
        }, status=500)
        
#endregion EliminarPlatillos

#region AgregarPlatillos

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
                platillo.Nombre = platilloname
                tipo = TipoPlatillo.objects.get(Id=tipoplatillo)
                platillo.IdTipoPlatillo = tipo
                platillo.Precio = precio
                platillo.EsActivo = estado
                platillo.Descripcion = descripcion

                if imagen:
                    # Guardar la imagen en el sistema de archivos
                    file_path = default_storage.save('platillos/' + imagen.name, imagen)
                    platillo.ImagenUrl = file_path
                
                platillo.save()
                return HttpResponse("")
        except Exception:
            print()
            print("#################### E X C E P C I O N ########################")
            print("--------------------'agregar_platillo'--------------------")
            print(traceback.format_exc())
            print("########################################################")
            print()
    else:
        # Si no lo ha hecho entonces deberá iniciar sesión
        return render(request, "login.html")
    
#endregion AgregarPlatillos

#endregion
