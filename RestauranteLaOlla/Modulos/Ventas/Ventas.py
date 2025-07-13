import json
from django.http import HttpResponse
from django.shortcuts import render

from Application.models import Areamesa, Detallefactura, Factura, Mesa, Metodopago, Personal, Platillo, Proveedor
from django.db.models import Q

# region VENTAS
def venta(request):
    if request.user.is_authenticated:
        try:
            platillo = Platillo.objects.filter(
                activo="activo").order_by('nombreplatillo').values()

            areaMesa = Areamesa.objects.filter(activo="1").values()

            areamesaSeleccionada = Areamesa.objects.get(id=1)

            mesa = Mesa.objects.filter(
                Q(idareamesa=areamesaSeleccionada) & Q(activo="1")).values()

            ordenesPendientes = Factura.objects.filter(
                Q(estado="1") & Q(activo="1")).count()

            # print("-----------------> URL Platillos <-----------------")
            # for p in platillo:
            #     print(p)
            #     print("-------------------------------------------------------------------------------------------------------------")

            contexto = {
                'Platillos': platillo,
                'Mesas': mesa,
                'AreaMesa': areaMesa,
                'ordenesPendientes': ordenesPendientes
            }

            return render(request, "venta.html", contexto)
        except Exception as ex:
            print()
            print("#################### E X C E P C I O N ########################")
            print(ex)
            print("########################################################")
            print()
    else:
        # Si no lo ha hecho entonces deberá iniciar sesión
        return render(request, "login.html")

def Detalle_Proveedor(request):
    if request.user.is_authenticated:
        try:
            if request.method == "POST":
                Nombre = request.POST.get("Nombre")
                Direccion = request.POST.get("Direction")
                Telefono = request.POST.get("Telefono")
                Correo = request.POST.get("Correo")
                Estado = request.POST.get("estado")
                id = request.POST.get("id")
                print("xdxdxd  "+id)
                proveedor = Proveedor.objects.get(id=id)
                print("proveedor ------------------------------> " + str(proveedor))
                proveedor.nombreprov = Nombre
                proveedor.direccionprov = Direccion
                proveedor.telefonoprov = Telefono
                proveedor.correoprov = Correo
                proveedor.activo = Estado
                proveedor.save()
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

def Agregar_Proveedor(request):
    if request.user.is_authenticated:
        try:
            if request.method == "POST":
                Nombre = request.POST.get("Nombre")
                Direccion = request.POST.get("Direction")
                Telefono = request.POST.get("Telefono")
                Correo = request.POST.get("Correo")
                proveedor = Proveedor()
                proveedor.nombreprov = Nombre
                proveedor.direccionprov = Direccion
                proveedor.telefonoprov = Telefono
                proveedor.correoprov = Correo
                proveedor.activo = "Inactivo"
                proveedor.save()
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

def DarBaja_Proveedor(request):
    if request.user.is_authenticated:
        try:
            if request.method == "POST":
                id = request.POST.get("id")
                print("xdxdxd  "+id)
                proveedor = Proveedor.objects.get(id=id)
                print("proveedor ------------------------------> " + str(proveedor))
                proveedor.activo = "Inactivo"
                proveedor.save()
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

#region VENTAS
def BuscarPlatillo(request):
    if request.user.is_authenticated:
        try:
            if request.method == "GET":
                Texto = request.GET.get("InputBuscarPlatillo")

                if Texto != "":
                    PlatillosObtenidos = Platillo.objects.filter(
                        nombreplatillo__icontains=Texto).order_by('nombreplatillo').values()
                    # No será sensible a las mayusculas con la i antes de contains
                else:
                    PlatillosObtenidos = Platillo.objects.filter(
                        activo="activo").order_by('nombreplatillo').values()

                contexto = {
                    "Platillos": PlatillosObtenidos
                }

                return render(request, "platillos.html", contexto)
        except Exception as ex:
            print()
            print("#################### E X C E P C I O N ########################")
            print(ex)
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

                areamesaSeleccionada = Areamesa.objects.get(id=idAM)

                MesasObtenidas = Mesa.objects.filter(
                    Q(idareamesa=areamesaSeleccionada) & Q(activo="1")).values()
                # No será sensible a las mayusculas con la i antes de contains

                contexto = {
                    "Mesas": MesasObtenidas
                }

                return render(request, "mesas.html", contexto)
        except Exception as ex:
            print()
            print("#################### E X C E P C I O N ########################")
            print(ex)
            print("########################################################")
            print()
    else:
        # Si no lo ha hecho entonces deberá iniciar sesión
        return render(request, "login.html")

def OrdenesPendientes(request):
    if request.user.is_authenticated:
        try:
            # El signo negativo para ordenarlos de manera descendiente
            ordenes =  Factura.objects.filter(Q(estado="1") & Q(activo="1")).order_by('-id').values()
            # ordenes = Factura.objects.filter(activo="1").order_by(
            #     F('id').desc(), F('estado').asc()).values()

            # print("----------------------- ORDENES --------------------------")
            # for orden in ordenes:
            #     print(orden["idmesa_id"])
            #     mesa = Mesa.objects.filter(id=orden["idmesa_id"])
            #     print(mesa)
            #     print("**************")

            mesas = Mesa.objects.filter(activo="1")
            metodoPago = Metodopago.objects.filter(activo="1").values()
            detalleOrden = Detallefactura.objects.all().values()
            platillos = Platillo.objects.all().values()

            print(detalleOrden)

            # print(ordenes)
            contexto = {
                "Ordenes": ordenes,
                "MetodoPago": metodoPago,
                "Mesas": mesas,
                "DetalleOrden": detalleOrden,
                "Platillos": platillos
            }

            return render(request, "ordenes.html", contexto)
        except Exception as ex:
            print()
            print("#################### E X C E P C I O N ########################")
            print(ex)
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
                print("Numero mesa: ", mesaseleccionada.numeromesa)
                print("Area de mesa: ", mesaseleccionada.idareamesa.nombream)
                print("Total: ", totalval)
                print(datos)

                for dato in datos:
                    print(dato['id'], dato['subtotal'], dato['cantidad'])

                print("--------------------------------------------------------------------")

                print("User ID: ", request.user.id)

                #################################################
                # SE CREA LA ORDEN

                # Se obtiene el usuario en sesión
                personalensesion = Personal.objects.get(id=request.user.id)

                Orden = Factura.objects.create(
                    idpersonal=personalensesion,
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

                    OrdenDetalle = Detallefactura.objects.create(
                        idfactura=Orden,
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
                OrdenACancelar = Factura.objects.get(id=idOrden)

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

                # Se obtiene la orden que se va a facturar
                OrdenAFacturar = Factura.objects.get(id=idOrden)
                print(OrdenAFacturar)

                OrdenAFacturar.monto = monto
                OrdenAFacturar.cambio = cambio
                OrdenAFacturar.estado = "0"
                OrdenAFacturar.propina = propina

                # Se guardan los cambios
                OrdenAFacturar.save()

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
