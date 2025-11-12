import json
import traceback
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

from Application.models import AreaMesa, DetalleOrden, Orden, Mesa, Usuario, Platillo, MesasPorOrden
from django.db.models import Q

# region VENTAS
def venta(request):
    if request.user.is_authenticated:
        try:
            platillo = Platillo.objects.filter(
                EsActivo="1").order_by('Nombre').values()

            AreaM = AreaMesa.objects.filter(EsActivo="1").values()

            AreaMesaSeleccionada = AreaMesa.objects.filter(Id = 1).first()

            if AreaMesaSeleccionada:
                mesa = Mesa.objects.filter(
                    Q(IdAreaMesa=AreaMesaSeleccionada) & Q(EsActivo="1")).values()
            else:
                mesa = []

            ordenesPendientes = Orden.objects.filter(
                Q(Estado="1") & Q(EsActivo="1")).count()

            contexto = {
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

#region VENTAS
def BuscarPlatillo(request):
    if request.user.is_authenticated:
        try:
            if request.method == "GET":
                Texto = request.GET.get("InputBuscarPlatillo")
                
                print("TEXTO: " + Texto)

                if Texto != "":
                    PlatillosObtenidos = Platillo.objects.filter(
                        Q(Nombre__icontains=Texto) & Q(EsActivo="1")).order_by('Nombre').values()
                    # No será sensible a las mayusculas con la i antes de contains
                else:
                    PlatillosObtenidos = Platillo.objects.filter(
                        EsActivo="1").order_by('Nombre').values()

                contexto = {
                    "Platillos": PlatillosObtenidos
                }
                
                print(PlatillosObtenidos)

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

            print("ORDENES PENDIENTES ==> ")
            print(ordenes)

            # print(ordenes)
            contexto = {
                "Ordenes": ordenes,
                "Platillos": platillos
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
def FacturarOrden(request):
    if request.user.is_authenticated:
        try:
            if request.method == "POST":
                idOrden = request.POST.get('idOrden')
                monto = request.POST.get('monto')
                cambio = request.POST.get('cambio')
                propina = request.POST.get('propinaOrden')

                print("""
                ID Orden: {},
                Monto: {},
                Cambio: {},
                Propina {}
                """.format(idOrden, monto, cambio, propina))

                # Se obtiene la orden que se va a Ordenr
                orden = Orden.objects.get(Id=idOrden)
                print(orden)

                orden.Monto = monto
                orden.Cambio = cambio
                orden.Estado = "0"
                orden.Propina = propina

                # Se guardan los cambios
                orden.save()

                return HttpResponse(request, "Hola")
        except Exception as ex:
            print("\n############### EXCEPCIÓN ###############")
            print(traceback.format_exc())
            print("#########################################\n")
            return JsonResponse({'error': str(ex)}, status=500)
    else:
        # Si no lo ha hecho entonces deberá iniciar sesión
        return render(request, "login.html")
#endregion FacturarOrden
