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
            
            detalleOrden = DetalleOrden.objects.filter(IdOrden__in=ordenes).select_related('IdPlatillo')
            
            mesas = Mesa.objects.filter(EsActivo="1")
            platillos = Platillo.objects.all().values()

            print("ORDENES PENDIENTES ==> ")
            print(ordenes)
            
            
            print("\nDETALLES DE ORDEN ==> ")
            print(detalleOrden)

            # print(ordenes)
            contexto = {
                "Ordenes": ordenes,
                "Mesas": mesas,
                "DetalleOrden": detalleOrden,
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
    if request.user.is_authenticated:
        try:
            if request.method == "POST":
                datos_json = request.POST.get('OrdenPlatillos')
                mesa = request.POST.get('mesa')
                totalval = request.POST.get('total')

                mesaseleccionada = Mesa.objects.get(Id=mesa)

                print("---------------------------- ORDEN CREADA -----------------------")
                datos = json.loads(datos_json)

                print("id mesa: ", mesa)
                print("Numero mesa: ", mesaseleccionada.Numero)
                print("Area de mesa: ", mesaseleccionada.IdAreaMesa.Nombre)
                print("Total: ", totalval)
                print(datos)

                for dato in datos:
                    print(dato['id'], dato['subtotal'], dato['cantidad'])

                print("--------------------------------------------------------------------")

                print("User ID: ", request.user.Id)

                #################################################
                # SE CREA LA ORDEN

                # Se obtiene el usuario en sesión
                Usuarioensesion = Usuario.objects.get(Id=request.user.Id)

                orden = Orden.objects.create(
                    IdUsuario=Usuarioensesion,
                    Total=totalval
                )

                orden.save()
                
                # Se registran las mesas por orden creada
                mesas = MesasPorOrden.objects.create(
                    IdOrden = orden,
                    IdMesa = mesaseleccionada
                )
                
                mesas.save()

                #################################################
                # SE CREAN LOS DETALLEN DE LA ORDEN

                for dato in datos:
                    print(dato['id'], dato['subtotal'], dato['cantidad'])
                    print("Precio: ", dato['subtotal']/dato['cantidad'])

                    platillodeldetalle = Platillo.objects.get(Id=dato["id"])

                    OrdenDetalle = DetalleOrden.objects.create(
                        IdOrden = orden,
                        IdPlatillo = platillodeldetalle,
                        Cantidad = dato['cantidad'],
                        PrecioVenta = platillodeldetalle.Precio,
                        SubTotal = dato['subtotal']
                    )

                    OrdenDetalle.save()

                #################################################

                print("-----------------------------------------------------")
                print("Orden: ", orden)
                print("-----------------------------------------------------")

                return HttpResponse(request, "Hola")
        except Exception as ex:
            print("\n############### EXCEPCIÓN ###############")
            print(traceback.format_exc())
            print("#########################################\n")
            return JsonResponse({'error': str(ex)}, status=500)
    else:
        # Si no lo ha hecho entonces deberá iniciar sesión
        return render(request, "login.html")
#endregion CrearOrden

#region AnularOrden
def CancelarOrden (request):
    if request.user.is_authenticated:
        try:
            if request.method == "POST":
                # Se obtiene el valor del id de la orden
                idOrden = request.POST.get('idOrden')

                # Se obtiene la orden con esa id
                OrdenACancelar = Orden.objects.get(Id=idOrden)

                # Se modifica el estado a "Cancelado"
                OrdenACancelar.Estado = "2"

                print("====== ANULAR ======")
                print(OrdenACancelar)

                # Se guardan los cambios
                OrdenACancelar.save()

                return HttpResponse(request, "Hola")
        except Exception as ex:
            print("\n############### EXCEPCIÓN ###############")
            print(traceback.format_exc())
            print("#########################################\n")
            return JsonResponse({'error': str(ex)}, status=500)
    else:
        # Si no lo ha hecho entonces deberá iniciar sesión
        return render(request, "login.html")
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
