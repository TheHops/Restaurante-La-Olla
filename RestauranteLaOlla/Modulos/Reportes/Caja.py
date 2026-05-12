from django.utils import timezone
from datetime import datetime, time
from django.http import JsonResponse
import traceback

from django.shortcuts import redirect, render
from django.contrib.auth import get_user_model

from django.db.models import Sum, Count, Q

from Application.models import Arqueo, Orden

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
            
            # 3. Buscar si ya existe un arqueo para hoy
            arqueo_actual = Arqueo.objects.filter(Fecha=hoy).first()
            
            if not arqueo_actual:
                # Si no existe registro para hoy, lo creamos
                arqueo_actual = Arqueo.objects.create(
                    Estado="0",
                    MontoInicial=0
                    # No asignamos IdUsuarioApertura aún porque no ha dado clic en "Iniciar"
                )
                
            print("HOY")
            print(hoy)

            # 3. Definir el inicio y fin del día en "aware datetime" (con zona horaria)
            # Esto crea un rango: 2026-05-11 00:00:00 hasta 23:59:59 en America/Managua
            inicio_dia = timezone.make_aware(datetime.combine(hoy, time.min))
            fin_dia = timezone.make_aware(datetime.combine(hoy, time.max))

            # 4. Consultas de Órdenes usando el rango (range)
            # Esto obliga a Django a convertir los UTC de la BD a Nicaragua antes de comparar
            ordenes_hoy = Orden.objects.filter(
                UltimaModificacion__range=(inicio_dia, fin_dia), 
                Estado="0", 
                EsActivo="1"
            )
            
            print("ORDENES")
            print(ordenes_hoy)

            # --- TOTAL EFECTIVO ---
            # Sumamos órdenes puras en efectivo (1) + la parte de efectivo de las mixtas (4)
            efectivo_puro = ordenes_hoy.filter(MetodoPago="1").aggregate(total=Sum('TotalPagar'))['total'] or 0
            efectivo_mixto = ordenes_hoy.filter(MetodoPago="4").aggregate(total=Sum('Monto') - Sum('Cambio'))['total'] or 0
            total_efectivo = efectivo_puro + efectivo_mixto
            
            print("Total efectivo puro")
            print(efectivo_puro)
            print("Total efectivo mixto")
            print(efectivo_mixto)
            print("Total efectivo")
            print(total_efectivo)

            # --- TOTAL TARJETA ---
            # Sumamos órdenes puras en tarjeta (2) + la parte de tarjeta de las mixtas (4)
            tarjeta_pura = ordenes_hoy.filter(MetodoPago="2").aggregate(total=Sum('TotalPagar'))['total'] or 0
            tarjeta_mixta = ordenes_hoy.filter(MetodoPago="4").aggregate(total=Sum('SegundoMonto'))['total'] or 0
            total_tarjeta = tarjeta_pura + tarjeta_mixta
            
            print("Total tarjeta")
            print(total_tarjeta)

            # --- TOTAL TRANSFERENCIA ---
            total_transferencia = ordenes_hoy.filter(MetodoPago="3").aggregate(total=Sum('TotalPagar'))['total'] or 0
            
            print("Total transferencia")
            print(total_transferencia)

            # --- CANTIDAD DE VOUCHERS (Órdenes con Tarjeta) ---
            # Contamos cuántas órdenes involucraron tarjeta (puro 2 o mixto 4)
            cantidad_tarjeta = ordenes_hoy.filter(Q(MetodoPago="2") | Q(MetodoPago="4")).count()

            # 5. Preparar el contexto
            contexto = {
                "User": request.user,
                "Arqueo": arqueo_actual,
                "TotalEfectivo": total_efectivo,
                "TotalTarjeta": total_tarjeta,
                "TotalTransferencia": total_transferencia,
                "CantidadTarjeta": cantidad_tarjeta,
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