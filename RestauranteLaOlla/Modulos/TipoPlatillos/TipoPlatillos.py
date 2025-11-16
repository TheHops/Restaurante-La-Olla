from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

from Application.models import Platillo, TipoPlatillo


#region CRUD TIPO PLATILLOS
def Actualizar_TipoPlatillo(request):
    if request.user.is_authenticated:
        try:
            if request.method == "POST":
                tipoplatilloname = request.POST.get("Nombre")
                estado = request.POST.get("estado")
                id = request.POST.get("id")
                print("nombreInsumo "+tipoplatilloname+" estado "+estado)
                tipoplatillo = TipoPlatillo.objects.get(Id=id)
                tipoplatillo.Nombre = tipoplatilloname
                tipoplatillo.EsActivo = estado
                tipoplatillo.save()
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

def DarBaja_TipoPlatillo(request):
    if not request.user.is_authenticated:
        return render(request, "login.html")

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

def Agregar_TipoPlatillo(request):
    if request.user.is_authenticated:
        try:
            if request.method == "POST":
                tipoplatilloname = request.POST.get("Nombre")
                # estado = request.POST.get("Estado")

                tipoplatillo = TipoPlatillo()

                tipoplatillo.Nombre = tipoplatilloname
                tipoplatillo.EsActivo = "1"

                tipoplatillo.save()
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
