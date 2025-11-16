from Application.models import Platillo, TipoPlatillo 
from django.shortcuts import render
import traceback
from django.http import JsonResponse

#region INVENTARIO

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
#endregion
