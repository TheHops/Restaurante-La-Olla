
from Application.models import Insumosvarios, Platillo, Proveedor, Tipoplatillo 
from django.shortcuts import render

#region INVENTARIO

def inventario(request):
    if request.user.is_authenticated:
        try:
            Insumos = Insumosvarios.objects.order_by("id")

            return render(request, "inventario_insumos.html", {'Insumos': Insumos})
        except Exception as ex:
            print()
            print("#################### E X C E P C I O N ########################")
            print(ex)
            print("########################################################")
            print()
    else:
        # Si no lo ha hecho entonces deberá iniciar sesión
        return render(request, "login.html")

def inventario_platillos(request):
    if request.user.is_authenticated:
        try:
            Platillos = Platillo.objects.order_by("id")
            PlatilloType = Tipoplatillo.objects.all()
            print("*******************************************************")
            print(PlatilloType)
            return render(request, "inventario_platillos.html", {'Platillos': Platillos, 'TypePlatillo': PlatilloType})
        except Exception as ex:
            print()
            print("#################### E X C E P C I O N ########################")
            print(ex)
            print("########################################################")
            print()
    else:
        # Si no lo ha hecho entonces deberá iniciar sesión
        return render(request, "login.html")

def inventario_tipoplatillo(request):
    if request.user.is_authenticated:
        try:
            PlatilloType = Tipoplatillo.objects.all()
            return render(request, "inventario_tipoPlatillo.html", {'TypePlatillo': PlatilloType})
        except Exception as ex:
            print()
            print("#################### E X C E P C I O N ########################")
            print(ex)
            print("########################################################")
            print()
    else:
        # Si no lo ha hecho entonces deberá iniciar sesión
        return render(request, "login.html")

def inventario_proveedores(request):
    if request.user.is_authenticated:
        try:
            Proveedores = Proveedor.objects.order_by("activo")

            return render(request, "inventario_proveedores.html", {'Proveedores': Proveedores})
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
