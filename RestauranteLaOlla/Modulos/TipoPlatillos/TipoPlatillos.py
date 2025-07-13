from gettext import translation
from django.http import HttpResponse
from django.shortcuts import render

from Application.models import Platillo, Tipoplatillo


#region CRUD TIPO PLATILLOS
def Actualizar_TipoPlatillo(request):
    if request.user.is_authenticated:
        try:
            if request.method == "POST":
                tipoplatilloname = request.POST.get("Nombre")
                estado = request.POST.get("estado")
                id = request.POST.get("id")
                print("nombreInsumo "+tipoplatilloname+" estado "+estado)
                print("xdxdxd  "+id)
                tipoplatillo = Tipoplatillo.objects.get(id=id)
                print("proveedor ------------------------------> " + str(tipoplatillo))
                tipoplatillo.nombretp = tipoplatilloname
                tipoplatillo.activo = estado
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
    if request.user.is_authenticated:
        try:
            if request.method == "POST":
                id = request.POST.get("id")
                print("xdxdxd  " + id)
                with translation.atomic():
                    # Obtener el tipo de platillo y marcarlo como inactivo
                    tipoplatillo = Tipoplatillo.objects.get(id=id)
                    tipoplatillo.activo = "Inactivo"
                    tipoplatillo.save()

                    # Obtener los platillos asociados al tipo de platillo y marcarlos como inactivos
                    platillos_asociados = Platillo.objects.filter(idtipoplatillo=tipoplatillo)
                    platillos_asociados.update(activo="Inactivo")
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

def Agregar_TipoPlatillo(request):
    if request.user.is_authenticated:
        try:
            if request.method == "POST":
                tipoplatilloname = request.POST.get("Nombre")
                estado = request.POST.get("Estado")

                tipoplatillo = Tipoplatillo()

                tipoplatillo.nombretp = tipoplatilloname
                tipoplatillo.activo = estado

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
