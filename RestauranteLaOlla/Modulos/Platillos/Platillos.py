
import traceback
from django.http import JsonResponse
from django.shortcuts import render, redirect
from Application.models import Platillo, TipoPlatillo
from django.core.files.storage import default_storage
from django.views.decorators.http import require_POST
from django.db import transaction

#region CRUD PLATILLOS

@require_POST
def Actualizar_Platillos(request):
    if not request.user.is_authenticated:
        return render(request, "login.html")
    
    if request.user.IdCargo.Nombre == "Cocinero" or request.user.IdCargo.Nombre == "Mesero" or request.user.IdCargo.Nombre == "Cajero":
        return redirect("/")

    try:
        with transaction.atomic():
            platillo_id = request.POST.get("id")
            nombre = request.POST.get("Nombre")
            precio = request.POST.get("Precio")
            tipo_id = request.POST.get("tipoplatillo")
            estado = request.POST.get("estado")
            descripcion = request.POST.get("Descripcion")
            imagen = request.FILES.get("Imagen")

            # Validaciones básicas
            if not platillo_id or not nombre or not precio or not tipo_id:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Faltan datos obligatorios.'
                }, status=400)

            try:
                platillo = Platillo.objects.get(Id=platillo_id)
            except Platillo.DoesNotExist:
                return JsonResponse({
                    'status': 'error',
                    'message': 'El consumo no existe.'
                }, status=404)

            try:
                tipo = TipoPlatillo.objects.get(Id=tipo_id)
            except TipoPlatillo.DoesNotExist:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Tipo de consumo no válido.'
                }, status=404)

            # Asignar campos
            platillo.Nombre = nombre
            platillo.IdTipoPlatillo = tipo
            platillo.Precio = precio
            platillo.EsActivo = estado
            platillo.Descripcion = descripcion

            # Si viene nueva imagen, actualizarla
            if imagen:
                ruta = default_storage.save(f'platillos/{imagen.name}', imagen)
                platillo.ImagenUrl = ruta

            platillo.save()

            return JsonResponse({
                'status': 'ok',
                'message': '¡Consumo modificado exitosamente!'
            })

    except Exception as ex:
        print("\n### ERROR EN Actualizar_Platillos ###")
        print(traceback.format_exc())

        return JsonResponse({
            'status': 'error',
            'message': 'Error interno del servidor.'
        }, status=500)

#region EliminarPlatillos

def DarBaja_Platillo(request):
    if not request.user.is_authenticated:
        return render(request, "login.html")
    
    if request.user.IdCargo.Nombre == "Cocinero" or request.user.IdCargo.Nombre == "Mesero" or request.user.IdCargo.Nombre == "Cajero":
        return redirect("/")

    try:
        if request.method == "POST":
            id_platillo = request.POST.get("id")

            if not id_platillo:
                return JsonResponse({
                    'status': 'error',
                    'message': 'ID de consumo no proporcionado.'
                }, status=400)

            try:
                platillo = Platillo.objects.get(Id=id_platillo)
            except Platillo.DoesNotExist:
                return JsonResponse({
                    'status': 'error',
                    'message': 'El consumo no existe.'
                }, status=404)

            platillo.EsActivo = "0"
            platillo.save()

            return JsonResponse({
                'status': 'ok',
                'message': '¡Consumo eliminado exitosamente!'
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

@require_POST
def Agregar_Platillo(request):
    if not request.user.is_authenticated:
        return render(request, "login.html")
    
    if request.user.IdCargo.Nombre == "Cocinero" or request.user.IdCargo.Nombre == "Mesero" or request.user.IdCargo.Nombre == "Cajero":
        return redirect("/")

    try:
        with transaction.atomic():  # Para asegurar que todo se guarda correctamente
            nombre = request.POST.get("Nombre")
            precio = request.POST.get("Precio")
            tipo_id = request.POST.get("tipoplatillo")
            descripcion = request.POST.get("Descripcion")
            imagen = request.FILES.get("Imagen")

            # Validaciones básicas
            if not nombre or not precio or not tipo_id:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Faltan datos obligatorios.'
                }, status=400)

            try:
                tipo = TipoPlatillo.objects.get(Id=tipo_id)
            except TipoPlatillo.DoesNotExist:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Tipo de consumo no válido.'
                }, status=404)

            platillo = Platillo(
                Nombre=nombre,
                IdTipoPlatillo=tipo,
                Precio=precio,
                EsActivo="1",
                Descripcion=descripcion,
            )

            # Guardar imagen si existe
            if imagen:
                ruta = default_storage.save(f'platillos/{imagen.name}', imagen)
                platillo.ImagenUrl = ruta

            platillo.save()

            return JsonResponse({
                'status': 'ok',
                'message': '¡Consumo agregado exitosamente!'
            })

    except Exception as ex:
        print("### ERROR EN Agregar_Platillo ###")
        print(ex)

        return JsonResponse({
            'status': 'error',
            'message': 'Error interno del servidor.'
        }, status=500)
    
#endregion AgregarPlatillos

#endregion
