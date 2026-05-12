from django.utils import timezone
from django.http import JsonResponse
import traceback

from django.shortcuts import redirect, render
from django.contrib.auth import get_user_model

from Application.models import Arqueo

User = get_user_model()

#region Caja

def Caja(request):
    if request.user.is_authenticated:
        try:
            # 1. Validación de seguridad (Cargos)
            if request.user.IdCargo.Nombre in ["Armador", "Mesero"]:
                return redirect("/")
            
            # 2. Obtener la fecha de hoy
            hoy = timezone.localdate()
            
            print("HOY")
            print(hoy)
            
            # 3. Buscar si ya existe un arqueo para hoy
            arqueo_actual = Arqueo.objects.filter(Fecha=hoy).first()
            
            if not arqueo_actual:
                # Si no existe registro para hoy, lo creamos
                arqueo_actual = Arqueo.objects.create(
                    Estado="0",
                    MontoInicial=0
                    # No asignamos IdUsuarioApertura aún porque no ha dado clic en "Iniciar"
                )

            # 4. Preparar el contexto
            contexto = {
                "User": request.user,
                "Arqueo": arqueo_actual, # Enviamos el objeto completo
            }
            
            return render(request, "caja.html", contexto)
        except Exception as ex:
            print("\n\n############### E X C E P C I Ó N ###############")
            print(traceback.format_exc())
            print("#####################################################\n\n")
    else:
        # Si no lo ha hecho entonces deberá iniciar sesión
        return render(request, "login.html")

#endregion Caja

#region InicioArqueo
    
def InicioArqueo(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            try:
                # 1. Validación de seguridad
                if request.user.IdCargo.Nombre in ["Armador", "Mesero"]:
                    return JsonResponse({"status": "error", "message": "No tiene permisos para esta acción."})

                # 2. Recibir datos del frontend
                monto_inicial = request.POST.get("MontoInicial", 0)
                
                # 3. Obtener el arqueo del día actual
                hoy = timezone.localdate()
                arqueo = Arqueo.objects.filter(Fecha=hoy).first()
                
                print("HOY")
                print(hoy)
                
                print("ARQUEO")
                print(arqueo)

                if arqueo:
                    # Si el arqueo ya estaba iniciado o cerrado, evitamos duplicar
                    if arqueo.Estado != "0":
                         return JsonResponse({"status": "error", "message": "El arqueo de hoy ya ha sido iniciado o cerrado."})
                    
                    # 4. Actualizar el registro
                    arqueo.MontoInicial = monto_inicial
                    arqueo.IdUsuarioApertura = request.user # Definimos quién aperturó
                    arqueo.Estado = "1" # Cambiamos a "Iniciado"
                    arqueo.save()

                    return JsonResponse({
                        "status": "ok", 
                        "message": "Arqueo iniciado correctamente. ¡Buen turno!"
                    })
                else:
                    return JsonResponse({"status": "error", "message": "No se encontró un registro de arqueo para hoy."})

            except Exception as ex:
                print("\n\n############### E X C E P C I Ó N ###############")
                print(traceback.format_exc())
                print("#####################################################\n\n")
                return JsonResponse({"status": "error", "message": "Ocurrió un error al procesar la solicitud."})
        
        return JsonResponse({"status": "error", "message": "Método no permitido."})
    else:
        return render(request, "login.html")

#endregion InicioArqueo

#endregion InicioArqueo