from django.http import HttpResponse
from django.shortcuts import render

from Application.models import Insumosvarios, Unidadmedida


#region CRUD INSUMOS


def Actualizar_Insumo(request):
    if request.user.is_authenticated:
        try:
            if request.method == "POST":
                nombreInsumo = request.POST.get("insumoNombre")
                presentacionInsumo = request.POST.get("insumoPresentacion")
                stock = request.POST.get("insumoStock")
                estado = request.POST.get("insumoestado")
                unidadmedida = request.POST.get("insumoUM")
                id = request.POST.get("idInsumo")
                print("nombreInsumo "+nombreInsumo + " presentacion "+presentacionInsumo +
                    " stock "+stock+" estado "+estado + " unidadmedida "+unidadmedida)
                print("xdxdxd  "+id)
                insumo = Insumosvarios.objects.get(id=id)
                print("proveedor ------------------------------> " + str(insumo))
                insumo.nombreinsumo = nombreInsumo
                insumo.presentacion = presentacionInsumo
                insumo.stock = stock
                insumo.activo = estado
                insumo.Unidadmedida = unidadmedida
                insumo.save()
                return HttpResponse("sdsdfsdfsd")
        except Exception as ex:
            print()
            print("#################### E X C E P C I O N ########################")
            print(ex)
            print("########################################################")
            print()    
    else:
        # Si no lo ha hecho entonces deberá iniciar sesión
        return render(request, "login.html")

def DarBaja_Insumo(request):
    if request.user.is_authenticated:
        try:
            if request.method == "POST":
                id = request.POST.get("id")
                print("xdxdxd  "+id)
                insumo = Insumosvarios.objects.get(id=id)
                print("proveedor ------------------------------> " + str(insumo))
                insumo.activo = "Inactivo"
                insumo.save()
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

def AgregarInsumo(request):
    if request.user.is_authenticated:
        try:
            if request.method == "POST":
                nombreInsumo = request.POST.get("insumoNombre")
                presentacionInsumo = request.POST.get("insumoPresentacion")
                stock = request.POST.get("insumoStock")
                estado = request.POST.get("insumoestado")
                unidadmedida = request.POST.get("insumoUM")
                print("nombreInsumo "+nombreInsumo + " presentacion "+presentacionInsumo +
                    " stock "+stock+" estado "+estado + " unidadmedida "+unidadmedida)

                insumo = Insumosvarios()
                insumo.nombreinsumo = nombreInsumo
                insumo.presentacion = presentacionInsumo
                insumo.stock = stock
                insumo.activo = estado
                unidadM = Unidadmedida.objects.get(id=unidadmedida)
                insumo.idunidadmedida = unidadM
                insumo.save()
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
