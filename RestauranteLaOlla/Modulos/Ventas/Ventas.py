import json
import traceback
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.utils import timezone

from Application.models import AreaMesa, DetalleOrden, Orden, Mesa, Usuario, Platillo, MesasPorOrden, TipoPlatillo
from django.db.models import Q, Prefetch, Count

# region VENTAS
def venta(request):
    if request.user.is_authenticated:
        try:
            platillo = Platillo.objects.filter(
                EsActivo="1").order_by('Nombre')

            AreaM = AreaMesa.objects.filter(EsActivo="1").values()
            
            tipos = (
                TipoPlatillo.objects
                .filter(EsActivo="1")
                .annotate(cantidad_platillos=Count('Platillos', filter=Q(Platillos__EsActivo="1")))
                .filter(cantidad_platillos__gt=0)
                .prefetch_related(
                    Prefetch(
                        'Platillos',
                        queryset=Platillo.objects.filter(EsActivo="1").order_by('Nombre')
                    )
                )
            )

            AreaMesaSeleccionada = AreaMesa.objects.filter(Id = 1).first()

            if AreaMesaSeleccionada:
                mesa = Mesa.objects.filter(
                    Q(IdAreaMesa=AreaMesaSeleccionada) & Q(EsActivo="1")).values()
            else:
                mesa = []

            ordenesPendientes = Orden.objects.filter(
                Q(Estado="1") & Q(EsActivo="1")).count()

            contexto = {
                'Tipos': tipos,
                'Platillos': platillo,
                'Mesas': mesa,
                'AreaMesa': AreaM,
                'ordenesPendientes': ordenesPendientes
            }

            return render(request, "venta.html", contexto)
        except Exception as ex:
            print()
            print("#################### E X C E P C I O N ########################")
            print("--------------------------'venta'--------------------------")
            print(traceback.format_exc())
            print("########################################################")
            print()
    else:
        # Si no lo ha hecho entonces deberá iniciar sesión
        return render(request, "login.html")
#endregion

#region FiltrarPlatillo
def BuscarPlatillo(request):
    if request.user.is_authenticated:
        try:
            if request.method == "GET":
                Texto = request.GET.get("InputBuscarPlatillo")
                TiposParam = request.GET.get("TiposSeleccionados", "")

                # Convertir "1,2,3" → [1,2,3]
                tipos_ids = []
                if TiposParam:
                    tipos_ids = [int(x) for x in TiposParam.split(",") if x.isdigit()]

                # --- Construir filtros dinámicos ---
                filtros = Q(EsActivo="1")

                # Filtrar por texto si existe
                if Texto:
                    filtros &= Q(Nombre__icontains=Texto)

                # Filtrar por tipos (solo si hay tipos seleccionados)
                if tipos_ids:
                    filtros &= Q(IdTipoPlatillo_id__in=tipos_ids)

                # Obtener los platillos filtrados
                PlatillosFiltrados = (
                    Platillo.objects.filter(filtros)
                    .order_by("Nombre")
                )

                # --- Obtener tipos que tengan esos platillos ---
                TiposFiltrados = TipoPlatillo.objects.filter(
                    EsActivo="1",
                    Platillos__in=PlatillosFiltrados
                ).distinct()
                
                print("PLATILLOS FILTRADOS")
                print(PlatillosFiltrados)

                # --- Prefetch solo los platillos filtrados ---
                TiposFiltrados = TiposFiltrados.prefetch_related(
                    Prefetch(
                        'Platillos',
                        queryset=PlatillosFiltrados,
                        to_attr='PlatillosFiltrados'
                    )
                )
                
                print("TIPOS FILTRADOS 2")
                print(TiposFiltrados)

                contexto = {
                    "Tipos": TiposFiltrados
                }

                return render(request, "platillos.html", contexto)
        except Exception as ex:
            print()
            print("#################### E X C E P C I O N ########################")
            print("----------------------'BuscarPlatillo'---------------------")
            print(traceback.format_exc())
            print("########################################################")
            print()
    else:
        # Si no lo ha hecho entonces deberá iniciar sesión
        return render(request, "login.html")
#endregion FiltrarPlatillo

#region FiltrarMesas
def FiltrarMesas(request):
    if request.user.is_authenticated:
        try:
            if request.method == "GET":
                idAM = request.GET.get("listaAreasDeMesa")

                print("-----------------------vvvvvv---------------------------")
                print(idAM)

                AreaMesaSeleccionada = AreaMesa.objects.get(Id=idAM)
                
                print(AreaMesaSeleccionada)

                MesasObtenidas = Mesa.objects.filter(
                    Q(IdAreaMesa=AreaMesaSeleccionada) & Q(EsActivo="1")).values()
                # No será sensible a las mayusculas con la i antes de contains

                print(MesasObtenidas)

                contexto = {
                    "Mesas": MesasObtenidas
                }

                return render(request, "mesas.html", contexto)
        except Exception as ex:
            print()
            print("#################### E X C E P C I O N ########################")
            print("--------------------'FiltrarMesas'--------------------")
            print(traceback.format_exc())
            print("########################################################")
            print()
    else:
        # Si no lo ha hecho entonces deberá iniciar sesión
        return render(request, "login.html")
#endregion FiltrarMesas

#region OrdenesPendientes
def OrdenesPendientes(request):
    if request.user.is_authenticated:
        try:
            # El signo negativo para ordenarlos de manera descendiente
            ordenes =  Orden.objects.select_related('IdUsuario').filter(Q(Estado="1") & Q(EsActivo="1")).order_by('-Id')
            
            platillos = Platillo.objects.all().values()
            
            # Obtener cargo del usuario en sesión
            cargo_usuario = request.user.IdCargo.Nombre if request.user.IdCargo else None

            # print(ordenes)
            contexto = {
                "Ordenes": ordenes,
                "Platillos": platillos,
                "CargoUsuario": cargo_usuario
            }

            return render(request, "ordenes.html", contexto)
        except Exception as ex:
            print()
            print("#################### E X C E P C I O N ########################")
            print("--------------------'OrdenesPendientes'--------------------")
            print(traceback.format_exc())
            print("########################################################")
            return JsonResponse({'error': str(ex)}, status=500)
    else:
        # Si no lo ha hecho entonces deberá iniciar sesión
        return render(request, "login.html")
#endregion OrdenesPendientes

#region CrearOrden
def CrearOrden(request):
    if not request.user.is_authenticated:
        return render(request, "login.html")
    
    if request.method != "POST":
        return JsonResponse({"status": "error", "message": "Método no permitido."}, status=405)
    
    try:
        # Datos recibidos del frontend
        datos_json = request.POST.get('OrdenPlatillos')
        mesas_json = request.POST.get('mesas')
        descripcion = request.POST.get('descripcion')
        totalval = request.POST.get('total')

        datos = json.loads(datos_json)
        mesas = json.loads(mesas_json)

        print("---------------------------- ORDEN CREADA -----------------------")
        print("Mesas:", mesas)
        print("Total:", totalval)
        print("Descripción:", descripcion)
        print("User ID:", request.user.Id)
        print("--------------------------------------------------------------------")

        # Obtener usuario en sesión
        usuario_en_sesion = Usuario.objects.get(Id=request.user.Id)

        # Crear la orden
        orden = Orden.objects.create(
            IdUsuario=usuario_en_sesion,
            Total=totalval,
            Descripcion=descripcion  # si tu modelo tiene este campo
        )

        # Asignar mesas a la orden
        mesas_objetos = Mesa.objects.filter(Id__in=mesas)
        for mesa in mesas_objetos:
            MesasPorOrden.objects.create(IdOrden=orden, IdMesa=mesa)

        # Establecer el área según la primera mesa seleccionada
        if mesas_objetos.exists():
            orden.AreaDeMesa = mesas_objetos[0].IdAreaMesa.Nombre
            orden.save()

        # Crear los detalles de la orden
        for dato in datos:
            platillo = Platillo.objects.get(Id=dato["id"])
            DetalleOrden.objects.create(
                IdOrden=orden,
                IdPlatillo=platillo,
                Cantidad=dato['cantidad'],
                PrecioVenta=platillo.Precio,
                SubTotal=dato['subtotal']
            )

        print("-----------------------------------------------------")
        print("Orden creada correctamente:", orden)
        print("-----------------------------------------------------")

        # Respuesta final esperada por el frontend
        return JsonResponse({
            "status": "ok",
            "message": "Orden creada exitosamente",
            "orden_id": orden.Id
        })
    except Exception as ex:
        print("\n############### EXCEPCIÓN ###############")
        print(traceback.format_exc())
        print("#########################################\n")
        return JsonResponse({"status": "error", "message": str(ex)}, status=500)
#endregion CrearOrden

#region AnularOrden
def CancelarOrden(request):
    if not request.user.is_authenticated:
        return render(request, "login.html")

    if request.method != "POST":
        return JsonResponse({"status": "error", "message": "Método no permitido."}, status=405)

    try:
        idOrden = request.POST.get('idOrden')
        motivo = request.POST.get('motivo')

        # Buscar la orden
        orden = Orden.objects.get(Id=idOrden)

        # Actualizar estado y motivo
        orden.Estado = "2"  # Cancelada / Anulada
        orden.Motivo = motivo
        orden.UltimaModificacion = timezone.now()
        
        orden.save()

        print("====== ORDEN ANULADA ======")
        print(f"Orden: {orden.Id} - Motivo: {motivo}")
        print("============================")

        return JsonResponse({
            "status": "ok",
            "message": f"La orden #{orden.Id} fue anulada correctamente."
        })

    except Orden.DoesNotExist:
        return JsonResponse({"status": "error", "message": "La orden no existe."}, status=404)

    except Exception as ex:
        print("\n############### EXCEPCIÓN ###############")
        print(traceback.format_exc())
        print("#########################################\n")
        return JsonResponse({"status": "error", "message": str(ex)}, status=500)
#endregion AnularOrden

#region FacturarOrden
def to_float(valor):
    if valor is None:
        return 0.0
    return float(valor.replace(".", "").replace(",", "."))

def FacturarOrden(request):
    if not request.user.is_authenticated:
        return render(request, "login.html")

    try:
        if request.method != "POST":
            return JsonResponse({
                "status": "error",
                "message": "Método no permitido"
            }, status=405)

        # ===============================
        # Obtener datos
        # ===============================
        idOrden     = request.POST.get('idOrden')
        monto       = to_float(request.POST.get('monto', 0))
        cambio      = to_float(request.POST.get('cambio', 0))
        propina     = to_float(request.POST.get('propinaOrden', 0))
        descuento   = to_float(request.POST.get('descuentoOrden', 0))
        total       = to_float(request.POST.get('totalOrden', 0))
        metodoPago  = int(request.POST.get('metodoPago'))
        banco  = request.POST.get('banco')
        numRef      = request.POST.get('numRef')

        # ===============================
        # Obtener orden
        # ===============================
        orden = Orden.objects.get(Id=idOrden)
        orden.UltimaModificacion = timezone.now()
        
        if banco is not None and banco.strip() == "":
            banco = None

        # ===============================
        # Validaciones por método de pago
        # ===============================
        if metodoPago == 1:  # EFECTIVO
            if monto < total:
                return JsonResponse({
                    "status": "error",
                    "message": "El monto en efectivo no puede ser menor al total."
                })

            cambio_calculado = round(monto - total, 2)

            if round(cambio, 2) != cambio_calculado:
                return JsonResponse({
                    "status": "error",
                    "message": "El cambio no coincide con el monto entregado."
                })

            orden.NumReferencia = None

        elif metodoPago in (2, 3):  # TARJETA o TRANSFERENCIA
            monto = total

            cambio = 0

            if metodoPago == 3:
                orden.NumReferencia = numRef
            else:
                orden.NumReferencia = None

        else:
            return JsonResponse({
                "status": "error",
                "message": "Método de pago inválido."
            })

        # ===============================
        # Guardar datos
        # ===============================
        orden.Monto        = monto
        orden.Cambio       = cambio
        orden.Propina      = propina
        orden.Descuento    = descuento
        orden.Total        = total
        orden.MetodoPago   = metodoPago
        orden.Banco        = banco
        orden.Estado       = "0"  # Facturada

        orden.save()

        return JsonResponse({
            "status": "ok",
            "message": f"La orden #{orden.Id} fue registrada correctamente."
        })

    except Orden.DoesNotExist:
        return JsonResponse({
            "status": "error",
            "message": "La orden no existe."
        })

    except Exception as ex:
        print("\n############### EXCEPCIÓN ###############")
        print(traceback.format_exc())
        print("#########################################\n")

        return JsonResponse({
            "status": "error",
            "message": "Ocurrió un error al facturar la orden."
        })
#endregion FacturarOrden

#region CambiarAEnPreparacion

def CambiarAEnPreparacion(request):
    if not request.user.is_authenticated:
        return render(request, "login.html")
    
    if request.method == "POST":
        try:
            id = request.POST.get("ID")
            orden = Orden.objects.get(Id=id)

            if orden.Estado != "1":
                return JsonResponse({
                    "status": "error",
                    "message": "No es una orden pendiente"
                }, status=400)

            orden.Estado = "4"
            orden.UltimaModificacion = timezone.now()
            
            orden.save()

            return JsonResponse({
                "status": "ok",
                "message": f"La orden #{orden.Id} ahora está en preparación",
                "old_type": "1",
                "new_type": "4"
            }, status=200)
        except Exception as ex:
            print("ERROR:", ex)
            return HttpResponse(status=500)

#endregion CambiarAEnPreparacion

#region CambiarAPreparado

def CambiarAPreparado(request):
    if not request.user.is_authenticated:
        return render(request, "login.html")
    
    if request.method == "POST":
        try:
            id = request.POST.get("ID")
            orden = Orden.objects.get(Id=id)

            if orden.Estado != "4":
                return JsonResponse({
                    "status": "error",
                    "message": f"La orden #{orden.Id} no está en preparación"
                }, status=400)

            orden.Estado = "3"
            orden.UltimaModificacion = timezone.now()
            
            orden.save()

            return JsonResponse({
                "status": "ok",
                "message": f"La orden #{orden.Id} está preparada",
                "old_type": "4",
                "new_type": "3"
            }, status=200)
        except Exception as ex:
            print("ERROR:", ex)
            return HttpResponse(status=500)

#endregion CambiarAPreparado