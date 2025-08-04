# Se importa la funcion para las respuestas del sitio web
from django.db.models import Case, When, Count
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from Application.models  import DetalleOrden, Orden, Mesa, Platillo 
from django.http import JsonResponse
from datetime import datetime, timedelta
from django.db.models import Q
import traceback

def index(request):
    # Direccion que me llevará al login por defecto
    if request.user.is_authenticated:
        print("SI ENTRO")
        # Si el usuario ya inició sesión entonces entrará directamente al sistema sin necesidad de volver a iniciar sesión
        return render(request, "inicio.html")
    else:
        # Si no lo ha hecho entonces deberá iniciar sesión
        return render(request, "login.html")

def loginUser(request):

    # Se verifica si el método fué de tipo POST
    if request.method == "GET":

        # Se obtienen los valores de los campos
        user_name = request.GET.get("txtUsername")
        pass_word = request.GET.get("txtPassword")

        print("USER -----> " + str(user_name))
        print("PASSWORD --> " + str(pass_word))

        # Se verifica si el usuario existe
        user = authenticate(request, username=user_name, password=pass_word)
        # Si no existe devolcerá un None
        
        print(user)

        # Si el usuario existe se inIcia sesión
        if user is not None and (user.EsActivo == '1' or user.EsActivo.lower() == 'inactivo'):
            login(request, user=user)
            return redirect("/")

    return render(request, 'login.html')

def logoutUser(request):
    logout(request)
    return redirect("/")

#region GraficasOrdenes
def GraficarOrdenes(request):
    if request.user.is_authenticated:
        try:
            # Filtrar órdenes facturadas
            facturas_por_dia = Orden.objects.filter(Estado='0')

            # Fecha actual y semana actual
            fecha_actual = datetime.today().date()
            num_semana_actual = fecha_actual.isocalendar()[1]
            inicio_semana_actual = fecha_actual - timedelta(days=fecha_actual.weekday())
            fin_semana_actual = inicio_semana_actual + timedelta(days=6)

            # Filtrar facturas dentro de la semana actual
            facturas_semana_actual = facturas_por_dia.filter(Fecha__date__range=[inicio_semana_actual, fin_semana_actual])

            # Contar facturas por día de la semana (0 = lunes, 6 = domingo)
            facturas_dict = {}
            for factura in facturas_semana_actual:
                if factura.Fecha:
                    dia_semana = factura.Fecha.weekday()
                    facturas_dict[dia_semana] = facturas_dict.get(dia_semana, 0) + 1

            # Construir listas de datos
            dias_semana = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
            num_facturas = [facturas_dict.get(dia, 0) for dia in range(7)]

            # Reordenar según el día actual
            dia_actual = fecha_actual.weekday()
            dias_semana = dias_semana[dia_actual:] + dias_semana[:dia_actual]
            num_facturas = num_facturas[dia_actual:] + num_facturas[:dia_actual]

            # Llevar el último al inicio (rotación visual)
            ultimo_valor = num_facturas.pop()
            num_facturas.insert(0, ultimo_valor)

            # Obtener los 5 platillos más vendidos
            platillos_mas_vendidos = Platillo.objects.annotate(num_ventas=Count('detalleorden')).order_by('-num_ventas')[:5]
            platillos_nombres = [platillo.Nombre for platillo in platillos_mas_vendidos]
            num_ventas_platillos = [platillo.num_ventas for platillo in platillos_mas_vendidos]

            # Retornar datos JSON
            data = {
                'dias_semana': dias_semana,
                'num_facturas': num_facturas,
                'platillos_nombres': platillos_nombres,
                'num_ventas_platillos': num_ventas_platillos
            }

            return JsonResponse(data)

        except Exception as ex:
            print("\n############### EXCEPCIÓN ###############")
            print(traceback.format_exc())
            print("#########################################\n")
            return JsonResponse({'error': str(ex)}, status=500)
    else:
        return render(request, "login.html")
#endregion GraficarOrdenes

#region FiltrarOrdenes
def FiltrarOrdenes(request):
    if request.user.is_authenticated:
        try:
            if request.method == "GET":
                EstadoOrden = request.GET.get("SelectFiltrarOrdenes")

                if EstadoOrden == "3":
                    OrdenesFiltradas = Orden.objects.select_related('IdMesa__IdAreaMesa', 'IdUsuario').filter(EsActivo="1").order_by(Case(When(Estado='1', then=0), When(Estado='0', then=1), When(Estado='2', then=2)), '-Id')
                else:
                    OrdenesFiltradas = Orden.objects.select_related('IdMesa__IdAreaMesa', 'IdUsuario').filter(Q(Estado=EstadoOrden) & Q(EsActivo="1")).order_by('-Id')

                mesas = Mesa.objects.filter(EsActivo="1")
                
                # metodoPago = ''
                # asignar el metodo de pago desde el request
                
                detalleOrden = DetalleOrden.objects.filter(IdOrden__in=OrdenesFiltradas).select_related('IdPlatillo')
                platillos = Platillo.objects.all().values()

                # print(ordenes)
                contexto = {
                    "Ordenes": OrdenesFiltradas,
                    # "MetodoPago": metodoPago,
                    "Mesas": mesas,
                    "DetalleOrden": detalleOrden,
                    "Platillos": platillos
                }

                # ordenes = Orden.objects.filter(activo="1").order_by(Case(When(estado='1', then=0), When(estado='0', then=1), When(estado='2', then=2)), '-id').values()

                # MesasObtenidas = Mesa.objects.filter(
                #     Q(idareamesa=areamesaSeleccionada) & Q(activo="1")).values()
                # No será sensible a las mayusculas con la i antes de contains

                return render(request, "ordenesFiltradas.html", contexto)
        except Exception as ex:
            print("\n############### EXCEPCIÓN ###############")
            print(traceback.format_exc())
            print("#########################################\n")
            return JsonResponse({'error': str(ex)}, status=500)
    else:
        # Si no lo ha hecho entonces deberá iniciar sesión
        return render(request, "login.html")
#endregion FiltrarOrdenes