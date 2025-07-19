import json
import traceback
from django.http import HttpResponse
from django.shortcuts import render

from Application.models import AreaMesa, DetalleOrden, Orden, Mesa, Usuario, Platillo
from django.db.models import Q

# region VENTAS
def venta(request):
    if request.user.is_authenticated:
        try:
            platillo = Platillo.objects.filter(
                EsActivo="Activo").order_by('Nombre').values()

            AreaM = AreaMesa.objects.filter(EsActivo="1").values()

            AreaMesaSeleccionada = AreaMesa.objects.filter(Id = 1).first()

            if AreaMesaSeleccionada:
                mesa = Mesa.objects.filter(
                    Q(IdAreaMesa=AreaMesaSeleccionada) & Q(EsActivo="1")).values()
            else:
                mesa = []

            ordenesPendientes = Orden.objects.filter(
                Q(Estado="1") & Q(EsActivo="1")).count()

            print("-----------------> URL Platillos <-----------------")
            for p in platillo:
                print(p)
                print("-------------------------------------------------------------------------------------------------------------")

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

                if Texto != "":
                    PlatillosObtenidos = Platillo.objects.filter(
                        nombreplatillo__icontains=Texto).order_by('Nombre').values()
                    # No será sensible a las mayusculas con la i antes de contains
                else:
                    PlatillosObtenidos = Platillo.objects.filter(
                        EsActivo="Activo").order_by('Nombre').values()

                contexto = {
                    "Platillos": PlatillosObtenidos
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

def FiltrarMesas(request):
    if request.user.is_authenticated:
        try:
            if request.method == "GET":
                idAM = request.GET.get("listaAreasDeMesa")

                print("-----------------------vvvvvv---------------------------")
                print(idAM)

                AreaMesaSeleccionada = AreaMesa.objects.get(Id=idAM)

                MesasObtenidas = Mesa.objects.filter(
                    Q(IdAreaMesa=AreaMesaSeleccionada) & Q(EsActivo="1")).values()
                # No será sensible a las mayusculas con la i antes de contains

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

def OrdenesPendientes(request):
    if request.user.is_authenticated:
        try:
            # El signo negativo para ordenarlos de manera descendiente
            ordenes =  Orden.objects.filter(Q(Estado="1") & Q(EsActivo="1")).order_by('-Id').values()
            # ordenes = Orden.objects.filter(activo="1").order_by(
            #     F('id').desc(), F('estado').asc()).values()

            # print("----------------------- ORDENES --------------------------")
            # for orden in ordenes:
            #     print(orden["idmesa_id"])
            #     mesa = Mesa.objects.filter(id=orden["idmesa_id"])
            #     print(mesa)
            #     print("**************")

            mesas = Mesa.objects.filter(EsActivo="1")
            detalleOrden = DetalleOrden.objects.all().values()
            platillos = Platillo.objects.all().values()

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
            print()
    else:
        # Si no lo ha hecho entonces deberá iniciar sesión
        return render(request, "login.html")

def CrearOrden(request):
    if request.user.is_authenticated:
        try:
            if request.method == "POST":
                datos_json = request.POST.get('OrdenPlatillos')
                mesa = request.POST.get('mesa')
                totalval = request.POST.get('total')

                mesaseleccionada = Mesa.objects.get(id=mesa)

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

                print("User ID: ", request.user.id)

                #################################################
                # SE CREA LA ORDEN

                # Se obtiene el usuario en sesión
                Usuarioensesion = Usuario.objects.get(id=request.user.id)

                Orden = Orden.objects.create(
                    idUsuario=Usuarioensesion,
                    idmesa=mesaseleccionada,
                    total=totalval
                )

                Orden.save()

                #################################################
                # SE CREAN LOS DETALLEN DE LA ORDEN

                for dato in datos:
                    print(dato['id'], dato['subtotal'], dato['cantidad'])
                    print("Precio: ", dato['subtotal']/dato['cantidad'])

                    platillodeldetalle = Platillo.objects.get(id=dato["id"])

                    OrdenDetalle = DetalleOrden.objects.create(
                        idOrden=Orden,
                        idplatillo=platillodeldetalle,
                        cantidad=dato['cantidad'],
                        precioventa=platillodeldetalle.precioplatillo
                    )

                    OrdenDetalle.save()

                #################################################

                print("-----------------------------------------------------")
                print("Orden: ", Orden)
                print("-----------------------------------------------------")

                return HttpResponse(request, "Hola")
        except Exception as ex:
            print()
            print("#################### E X C E P C I O N ########################")
            print(ex)
            print("########################################################")
            print()
    else:
        # Si no lo ha hecho entonces deberá iniciar sesión
        return render(request, "login.html")

def CancelarOrden (request):
    if request.user.is_authenticated:
        try:
            if request.method == "POST":
                # Se obtiene el valor del id de la orden
                idOrden = request.POST.get('idOrden')

                # Se obtiene la orden con esa id
                OrdenACancelar = Orden.objects.get(id=idOrden)

                # Se modifica el estado a "Cancelado"
                OrdenACancelar.estado = "2"

                print(OrdenACancelar)

                # Se guardan los cambios
                OrdenACancelar.save()

                return HttpResponse(request, "Hola")
        except Exception as ex:
            print()
            print("#################### E X C E P C I O N ########################")
            print(ex)
            print("########################################################")
            print()
    else:
        # Si no lo ha hecho entonces deberá iniciar sesión
        return render(request, "login.html")

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
                orden = Orden.objects.get(id=idOrden)
                print(orden)

                orden.monto = monto
                orden.cambio = cambio
                orden.estado = "0"
                orden.propina = propina

                # Se guardan los cambios
                orden.save()

                return HttpResponse(request, "Hola")
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
