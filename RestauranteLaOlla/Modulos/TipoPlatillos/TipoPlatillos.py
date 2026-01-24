from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from django.db import transaction

from Application.models import Platillo, TipoPlatillo


#region CRUD TIPO PLATILLOS

#region Actualizar platillos

@require_POST
def Actualizar_TipoPlatillo(request):

    if not request.user.is_authenticated:
        return render(request, "login.html")
    
    if request.user.IdCargo.Nombre == "Armador" or request.user.IdCargo.Nombre == "Mesero" or request.user.IdCargo.Nombre == "Cajero":
        return redirect("/")

    try:
        with transaction.atomic():
            id_tipo = request.POST.get("id")
            nombre = request.POST.get("Nombre", "").strip()
            estado = request.POST.get("estado")

            # Validación de ID
            if not id_tipo:
                return JsonResponse({
                    'status': 'error',
                    'message': 'ID no proporcionado.'
                }, status=400)

            # Validación del nombre
            if not nombre:
                return JsonResponse({
                    'status': 'error',
                    'message': 'El nombre del tipo de consumo es obligatorio.'
                }, status=400)

            # Verificar existencia
            try:
                tipo = TipoPlatillo.objects.get(Id=id_tipo)
            except TipoPlatillo.DoesNotExist:
                return JsonResponse({
                    'status': 'error',
                    'message': 'El tipo de consumo no existe.'
                }, status=404)

            # Evitar duplicados con otro registro
            if TipoPlatillo.objects.exclude(Id=id_tipo).filter(Nombre__iexact=nombre).exists():
                return JsonResponse({
                    'status': 'error',
                    'message': 'Ya existe otro tipo de consumo con ese nombre.'
                }, status=409)

            # Actualizar
            tipo.Nombre = nombre

            if estado in ["0", "1"]:
                tipo.EsActivo = estado

            tipo.save()

            return JsonResponse({
                'status': 'ok',
                'message': 'Tipo de consumo actualizado correctamente.'
            })

    except Exception as ex:
        print("\n### ERROR EN Actualizar_TipoPlatillo ###")
        print(ex)

        return JsonResponse({
            'status': 'error',
            'message': 'Error interno del servidor.'
        }, status=500)
    
#endregion Actualizar platillos

#region Eliminar platillos

def DarBaja_TipoPlatillo(request):
    if not request.user.is_authenticated:
        return render(request, "login.html")
    
    if request.user.IdCargo.Nombre == "Armador" or request.user.IdCargo.Nombre == "Mesero" or request.user.IdCargo.Nombre == "Cajero":
        return redirect("/")

    try:
        if request.method == "POST":
            id = request.POST.get("id")

            if not id:
                return JsonResponse({"status": "error", "message": "ID no recibido"}, status=400)

            # Obtener el tipo de platillo
            tipoplatillo = TipoPlatillo.objects.filter(Id=id).first()
            if not tipoplatillo:
                return JsonResponse({"status": "error", "message": "El tipo de consumo no existe"}, status=404)

            # Marcar como inactivo
            tipoplatillo.EsActivo = "0"
            tipoplatillo.save()

            # Desactivar platillos asociados
            # Platillo.objects.filter(IdTipoPlatillo=tipoplatillo).update(EsActivo="0")

            return JsonResponse({
                "status": "ok",
                "message": "Tipo de consumo y consumos asociados dados de baja correctamente"
            })

        return JsonResponse({"status": "error", "message": "Método no permitido"}, status=405)

    except Exception as ex:
        print("#################### EXCEPCIÓN ########################")
        print(ex)
        print("########################################################")
        return JsonResponse({"status": "error", "message": "Error interno del servidor"}, status=500)
    
#endregion Eliminar platillos

#region Agregar platillos

@require_POST
def Agregar_TipoPlatillo(request):

    if not request.user.is_authenticated:
        return render(request, "login.html")
    
    if request.user.IdCargo.Nombre == "Armador" or request.user.IdCargo.Nombre == "Mesero" or request.user.IdCargo.Nombre == "Cajero":
        return redirect("/")

    try:
        with transaction.atomic():
            nombre = request.POST.get("Nombre", "").strip()

            # Validación
            if not nombre:
                return JsonResponse({
                    'status': 'error',
                    'message': 'El nombre del tipo de consumo es obligatorio.'
                }, status=400)

            # Verificar si ya existe
            if TipoPlatillo.objects.filter(Nombre__iexact=nombre).exists():
                return JsonResponse({
                    'status': 'error',
                    'message': 'Este tipo de consumo ya existe.'
                }, status=409)

            tipo = TipoPlatillo(
                Nombre=nombre,
                EsActivo="1"
            )
            tipo.save()

            return JsonResponse({
                'status': 'ok',
                'message': 'Tipo de consumo agregado correctamente.'
            })

    except Exception as ex:
        print("### ERROR EN Agregar_TipoPlatillo ###")
        print(ex)

        return JsonResponse({
            'status': 'error',
            'message': 'Error interno del servidor.'
        }, status=500)
        
#endregion Agregar platillos

#endregion CRUD TIPO PLATILLOS
