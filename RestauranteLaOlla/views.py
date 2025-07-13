# Se importa la funcion para las respuestas del sitio web
from django.db.models import Case, When, Count
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from Application.models  import Detallefactura, Factura, Mesa, Metodopago, Platillo 
from django.http import JsonResponse
from datetime import datetime
import datetime
import datetime
from django.db.models import Q

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
        username = request.GET.get("txtUsername")
        password = request.GET.get("txtPassword")

        print("USER -----> " + str(username))
        print("PASSWORD --> " + str(password))

        # Se verifica si el usuario existe
        user = authenticate(request, username=username, password=password)
        # Si no existe devolcerá un None
        
        print("\n\n====================")
        print("usuario inactivo ",user.activo)
        # Si el usuario existe se incia sesión
        if user is not None and (user.activo == '1' or user.activo.lower() == 'inactivo'):
            login(request, user=user)
            return redirect("/")

    return render(request, 'login.html')

def logoutUser(request):
    logout(request)
    return redirect("/")

#region GRAFICAS DASHBOARD
def GraficaFacturas(request):
    if request.user.is_authenticated:
        try:
            facturas_por_dia = Factura.objects.filter(estado='0')
            # Crea un diccionario, donde se cuenta las facturas por día de la semana xdxdxd

            # Obtiene la fecha actual y la semana actual
            fecha_actual = datetime.datetime.today().date()
            num_semana_actual = fecha_actual.isocalendar()[1]
            
            print("Número de la semana actual:", num_semana_actual)
            
            dia_inicio_semana = datetime.date.today().weekday()

            print("Día de inicio de la semana:", dia_inicio_semana + 1)

            # Calcula la fecha de inicio y fin de la semana actual
            inicio_semana_actual = fecha_actual - datetime.timedelta(days=fecha_actual.weekday())
            fin_semana_actual = inicio_semana_actual + datetime.timedelta(days=6)

            print("\n=====================================")
            print("=====================================")
            print("inicio semana actual ",inicio_semana_actual)
            print("fin semana actual ",fin_semana_actual)

            # Filtra las facturas por la semana actual
            facturas_semana_actual = facturas_por_dia.filter(fechaventa__range=[inicio_semana_actual, fin_semana_actual])
            
            print("\n=====================================")
            print("=====================================")
            print("facturas semana actual ",facturas_semana_actual)
            
            # Crea un diccionario para contar las facturas por día de la semana
            facturas_dict = {}
            for factura in facturas_por_dia:
                dia_semana = factura.fechaventa.weekday() 
            for factura in facturas_semana_actual:
                dia_semana = factura.fechaventa.weekday()
                facturas_dict[dia_semana] = facturas_dict.get(dia_semana, 0) + 1
                
                print("\n=====================================")
                print("=====================================")
                print("dia de semana ",dia_semana)
                print("facturas dict  ",facturas_dict[dia_semana])


            # Creamos listas separadas para las etiquetas de los ejes X e Y
            dias_semana = ["Domingo","Lunes", "Martes","Miercoles","Jueves","Viernes","Sabado"]
            num_facturas = [facturas_dict.get(dia, 0) for dia in range(7)]
            print(num_facturas)
            dias_semana = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
            num_facturas = [0] * 7

            # Asigna las facturas al día correspondiente
            for dia_semana, cantidad_facturas in facturas_dict.items():
                num_facturas[dia_semana] = cantidad_facturas

            # Desplaza los valores en las listas según el día actual
            dias_semana = dias_semana[fecha_actual.weekday():] + dias_semana[:fecha_actual.weekday()]
            num_facturas = num_facturas[fecha_actual.weekday():] + num_facturas[:fecha_actual.weekday()]
            
            ultimo_valor = num_facturas.pop()  # Elimina y devuelve el último elemento de la lista
            num_facturas.insert(0, ultimo_valor)
            print("\n=====================================")
            print("=====================================")
            print("numero de facturas ",num_facturas)
            print("dias de semana ",dias_semana)

            # Si la semana actual ha terminado, reinicia la información de las facturas
            print("\n================================")
            print(num_semana_actual)
            if num_semana_actual != inicio_semana_actual.isocalendar()[1]:
                facturas_dict = {}
                num_facturas = [0] * 7

            # Obtiene los 5 platillos más vendidos
            platillos_mas_vendidos = Platillo.objects.annotate(num_ventas=Count('detallefactura')).order_by('-num_ventas')[:5]
            platillos_nombres = [platillo.nombreplatillo for platillo in platillos_mas_vendidos]
            num_ventas_platillos = [platillo.num_ventas for platillo in platillos_mas_vendidos]
            print("\n=====================================")
            print("=====================================")
            print("platillos mas vendidos ",platillos_nombres)
            print("platillos cantidades vendidas ",num_ventas_platillos)


            # Pasa los datos a la respuesta JSON
            data = {
                'dias_semana': dias_semana,
                'num_facturas': num_facturas,
                'platillos_nombres': platillos_nombres,
                'num_ventas_platillos': num_ventas_platillos
            }

            # el mero quiebractre69
            return JsonResponse(data)
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

def FiltrarOrdenes(request):
    if request.user.is_authenticated:
        try:
            if request.method == "GET":
                EstadoOrden = request.GET.get("SelectFiltrarOrdenes")

                if EstadoOrden == "3":
                    OrdenesFiltradas = Factura.objects.filter(activo="1").order_by(Case(When(estado='1', then=0), When(estado='0', then=1), When(estado='2', then=2)), '-id').values()
                else:
                    OrdenesFiltradas = Factura.objects.filter(Q(estado=EstadoOrden) & Q(activo="1")).order_by('-id').values()

                mesas = Mesa.objects.filter(activo="1")
                metodoPago = Metodopago.objects.filter(activo="1").values()
                detalleOrden = Detallefactura.objects.all().values()
                platillos = Platillo.objects.all().values()

                # print(ordenes)
                contexto = {
                    "Ordenes": OrdenesFiltradas,
                    "MetodoPago": metodoPago,
                    "Mesas": mesas,
                    "DetalleOrden": detalleOrden,
                    "Platillos": platillos
                }


                # ordenes = Factura.objects.filter(activo="1").order_by(Case(When(estado='1', then=0), When(estado='0', then=1), When(estado='2', then=2)), '-id').values()

                # MesasObtenidas = Mesa.objects.filter(
                #     Q(idareamesa=areamesaSeleccionada) & Q(activo="1")).values()
                # No será sensible a las mayusculas con la i antes de contains

                return render(request, "ordenesFiltradas.html", contexto)
        except Exception as ex:
            print()
            print("#################### E X C E P C I O N ########################")
            print(ex)
            print("########################################################")
            print()
    else:
        # Si no lo ha hecho entonces deberá iniciar sesión
        return render(request, "login.html")



       # print("==========dia semana====================")
        #print("==============================")
        #print(dia_semana)


