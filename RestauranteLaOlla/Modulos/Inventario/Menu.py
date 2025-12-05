from Application.models import Platillo, TipoPlatillo 
from django.shortcuts import render
import traceback
from django.http import JsonResponse

#region Inventario

#region Platillos

def inventario_platillos(request):
    if request.user.is_authenticated:
        try:
            Platillos = (
                Platillo.objects
                .filter(IdTipoPlatillo__EsActivo="1")   # Solo tipos activos
                .select_related("IdTipoPlatillo")       # Trae el tipo junto al platillo
                .order_by("Id")
            )
            PlatilloType = TipoPlatillo.objects.all()
            
            return render(request, "inventario_platillos.html", {'Platillos': Platillos, 'TypePlatillo': PlatilloType})
        except Exception as ex:
            print()
            print("#################### E X C E P C I O N ########################")
            print("--------------------'inventario_platillos'--------------------")
            print(traceback.format_exc())
            print("########################################################")
            return JsonResponse({'error': str(ex)}, status=500)
    else:
        # Si no lo ha hecho entonces deberá iniciar sesión
        return render(request, "login.html")
    
def filtrar_platillos(request):
    if not request.user.is_authenticated:
        return render(request, "login.html")

    ver_eliminados = request.GET.get("verEliminados") == "1"

    if ver_eliminados:
        platillos = Platillo.objects.select_related("IdTipoPlatillo").order_by("Id")
    else:
        platillos = Platillo.objects.select_related("IdTipoPlatillo").filter(EsActivo="1").order_by("Id")
        
    print("####################################")
    print(ver_eliminados)
    print("####################################")

    contexto = {
        "Platillos": platillos,
        "VerEliminados": "1" if ver_eliminados else "0"
    }

    return render(request, "inventario_platillos_filtrados.html", contexto)

#endregion Platillos

#region TipoPlatillo

def inventario_tipoplatillo(request):
    if request.user.is_authenticated:
        try:
            PlatilloType = TipoPlatillo.objects.all()
            return render(request, "inventario_tipoPlatillo.html", {'TypePlatillo': PlatilloType})
        except Exception as ex:
            print()
            print("#################### E X C E P C I O N ########################")
            print("-------------------'inventario_tipoplatillo'-------------------")
            print(traceback.format_exc())
            print("########################################################")
            return JsonResponse({'error': str(ex)}, status=500)
    else:
        # Si no lo ha hecho entonces deberá iniciar sesión
        return render(request, "login.html")
    
def filtrar_tipo_platillos(request):
    if not request.user.is_authenticated:
        return render(request, "login.html")

    ver_eliminados = request.GET.get("verEliminados") == "1"

    if ver_eliminados:
        tipoplatillos = TipoPlatillo.objects.order_by("Id")
    else:
        tipoplatillos = TipoPlatillo.objects.filter(EsActivo="1").order_by("Id")
        
    print("############### TIPO PLATILLOS #####################")
    print(ver_eliminados)
    print("####################################################")

    contexto = {
        "TypePlatillo": tipoplatillos,
        "VerEliminados": "1" if ver_eliminados else "0"
    }

    return render(request, "inventario_tipo_platillos_filtrados.html", contexto)
    
#endregion TipoPlatillo

#endregion Inventario
