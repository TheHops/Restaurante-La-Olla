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
        if request.user.IdCargo.Nombre == "Cocinero":
            return redirect("OrdenesPendientes/")
        elif request.user.IdCargo.Nombre == "Mesero":
            return redirect("venta/")
        
        # Si el usuario ya inició sesión entonces entrará directamente al sistema sin necesidad de volver a iniciar sesión
        return render(request, "inicio.html")
    else:
        # Si no lo ha hecho entonces deberá iniciar sesión
        return render(request, "login.html")

def loginUser(request):

    if request.method == "POST":

        user_name = request.POST.get("txtUsername")
        pass_word = request.POST.get("txtPassword")

        user = authenticate(request, username=user_name, password=pass_word)

        if user is not None and (user.EsActivo == '1' or user.EsActivo.lower() == 'inactivo'):
            login(request, user=user)
            return redirect("/")

        return redirect("loginUser")

    return render(request, "login.html")

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

OPCIONES_DISPONIBLES = {
    "Administrador": ["0", "1", "2", "3", "4", "5"],
    "Mesero": ["1", "4", "6"],
    "Cocinero": ["1", "4", "6"],
    "Cajero": ["0", "2", "3"]
}

VALORES_POR_DEFECTO = {
    "Administrador": "5",
    "Mesero": "6",
    "Cocinero": "6",
    "Cajero": "3"
}

def validar_filtro_por_cargo(cargo, valor_filtro):
    opciones = OPCIONES_DISPONIBLES.get(cargo, [])
    default = VALORES_POR_DEFECTO.get(cargo, None)

    if valor_filtro in opciones:
        return valor_filtro

    return default

def FiltrarOrdenes(request):
    if request.user.is_authenticated:
        try:
            if request.method == "GET":
                EstadoOrden = request.GET.get("SelectFiltrarOrdenes")
                
                cargo_usuario = request.user.IdCargo.Nombre

                # Validación segura del filtro
                EstadoOrden = validar_filtro_por_cargo(cargo_usuario, EstadoOrden)

                if EstadoOrden == "5":
                    OrdenesFiltradas = Orden.objects.select_related('IdUsuario').filter(EsActivo="1").order_by(Case(When(Estado='1', then=0), When(Estado='4', then=1), When(Estado='3', then=2), When(Estado='0', then=3), When(Estado='2', then=4)), '-Id')
                elif EstadoOrden == "6":
                    OrdenesFiltradas = Orden.objects.select_related('IdUsuario').filter(EsActivo="1", Estado__in=["1", "4"]).order_by(Case(When(Estado='1', then=0), When(Estado='4', then=1)), '-Id')
                else:
                    OrdenesFiltradas = Orden.objects.select_related('IdUsuario').filter(Q(Estado=EstadoOrden) & Q(EsActivo="1")).order_by('-Id')
                
                # metodoPago = ''
                # asignar el metodo de pago desde el request
                
                platillos = Platillo.objects.all().values()

                # print(ordenes)
                contexto = {
                    "Ordenes": OrdenesFiltradas,
                    # "MetodoPago": metodoPago,
                    "Platillos": platillos,
                    "CargoUsuario": cargo_usuario
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