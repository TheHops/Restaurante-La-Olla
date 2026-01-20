# Se importa la funcion para las respuestas del sitio web
from django.db.models import Case, When, Count
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from Application.models  import Orden, Platillo, Usuario, DetalleOrden, MesasPorOrden
from django.contrib import messages
from django.http import JsonResponse
from datetime import datetime, timedelta
from django.db.models import Q, Prefetch
import traceback
from django.core.mail import send_mail
from django.utils import timezone

User = get_user_model()

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

        entrada = request.POST.get("txtUsername")
        pass_word = request.POST.get("txtPassword")

        # Primero detectamos si escribieron un correo
        es_correo = "@" in entrada and "." in entrada

        user_obj = None

        if es_correo:
            try:
                user_obj = User.objects.get(email=entrada)
                username_real = user_obj.username
            except User.DoesNotExist:
                messages.error(request, "El correo ingresado no está asociado a ninguna cuenta.")
                return redirect("loginUser")
        else:
            username_real = entrada

        user = authenticate(request, username=username_real, password=pass_word)

        if user is None:
            messages.error(request, "Credenciales incorrectas.")
            return redirect("loginUser")

        if user.EsActivo != "1":
            messages.error(request, "Tu cuenta está inactiva.")
            return redirect("loginUser")

        login(request, user)
        return redirect("/")

    return render(request, "login.html")

def logoutUser(request):
    logout(request)
    return redirect("/")

#region GraficasOrdenes

dias_semana_es = {
    0: "Lunes",
    1: "Martes",
    2: "Miércoles",
    3: "Jueves",
    4: "Viernes",
    5: "Sábado",
    6: "Domingo",
}

def GraficarOrdenes(request):
    if not request.user.is_authenticated:
        return render(request, "login.html")

    try:
        hoy_local = timezone.localdate()  # 18/12/2025
        hace_7_dias_local = hoy_local - timedelta(days=6)

        # Convertir a datetime al inicio y fin del día
        inicio_rango = timezone.make_aware(
            datetime.combine(hace_7_dias_local, datetime.min.time()), timezone.get_current_timezone()
        )
        fin_rango = timezone.make_aware(
            datetime.combine(hoy_local, datetime.max.time()), timezone.get_current_timezone()
        )
        
        print() 
        print("Hace 7 días - Hoy") 
        print(hace_7_dias_local)
        print(hoy_local)

        # Órdenes facturadas en los últimos 7 días
        facturas_7_dias = Orden.objects.filter(
            Estado="0",
            UltimaModificacion__range=(inicio_rango, fin_rango)
        )
        
        print() 
        print("Facturas 7 días") 
        print(facturas_7_dias)

        # Inicializar diccionario con los últimos 7 días
        dias = [(hoy_local - timedelta(days=i)) for i in range(6, -1, -1)]
        
        print() 
        print("Días") 
        print(dias)
        
        conteo_por_dia = {dia: 0 for dia in dias}

        for factura in facturas_7_dias:
            fecha = factura.UltimaModificacion.astimezone(
                timezone.get_current_timezone()
            ).date()
            if fecha in conteo_por_dia:
                conteo_por_dia[fecha] += 1

        dias_labels = [dias_semana_es[dia.weekday()] for dia in dias]
        num_facturas = list(conteo_por_dia.values())

        # Top 5 platillos
        platillos_mas_vendidos = (
            Platillo.objects
            .annotate(num_ventas=Count('detalleorden'))
            .order_by('-num_ventas')[:5]
        )

        data = {
            "dias_semana": dias_labels,
            "num_facturas": num_facturas,
            "platillos_nombres": [p.Nombre for p in platillos_mas_vendidos],
            "num_ventas_platillos": [p.num_ventas for p in platillos_mas_vendidos],
        }

        return JsonResponse(data)

    except Exception as ex:
        print(traceback.format_exc())
        return JsonResponse({"error": str(ex)}, status=500)

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
    if not request.user.is_authenticated:
        return render(request, "login.html")

    if request.method != "GET":
        return JsonResponse({"status": "error", "message": "Método no permitido"}, status=405)

    try:
        EstadoOrden = request.GET.get("SelectFiltrarOrdenes")
        cargo_usuario = request.user.IdCargo.Nombre

        validar_cargo(request, cargo_usuario)

        # Validación segura del filtro
        EstadoOrden = validar_filtro_por_cargo(cargo_usuario, EstadoOrden)

        # Query base
        ordenes = Orden.objects.select_related(
            'IdUsuario'
        ).prefetch_related(
            Prefetch('Detalles', queryset=DetalleOrden.objects.order_by('-EsActivo')),
            Prefetch('Mesas', queryset=MesasPorOrden.objects.filter(EsActivo="1").select_related('IdMesa')
    )
        ).filter(EsActivo="1")

        # FILTRO ADICIONAL PARA MESERO
        if cargo_usuario == "Mesero":
            ordenes = ordenes.filter(IdUsuario=request.user)

        # FILTROS POR ESTADO
        if EstadoOrden == "5":
            ordenes = ordenes.order_by(
                Case(
                    When(Estado='1', then=0),
                    When(Estado='4', then=1),
                    When(Estado='3', then=2),
                    When(Estado='0', then=3),
                    When(Estado='2', then=4),
                ),
                '-UltimaModificacion'
            )

        elif EstadoOrden == "6":
            ordenes = ordenes.filter(
                Estado__in=["1", "4"]
            ).order_by(
                Case(
                    When(Estado='1', then=0),
                    When(Estado='4', then=1),
                ),
                '-UltimaModificacion'
            )

        else:
            ordenes = ordenes.filter(
                Estado=EstadoOrden
            ).order_by('-UltimaModificacion')

        platillos = Platillo.objects.all().values()

        contexto = {
            "Ordenes": ordenes,
            "Platillos": platillos,
            "CargoUsuario": cargo_usuario
        }

        return render(request, "ordenesFiltradas.html", contexto)

    except Exception as ex:
        print("\n############### EXCEPCIÓN ###############")
        print(traceback.format_exc())
        print("#########################################\n")
        return JsonResponse({'error': str(ex)}, status=500)

#endregion FiltrarOrdenes

#region Cargo

def consultar_cargo(request):
    usuario = request.user

    if not usuario.is_authenticated:
        return render(request, "login.html")

    if usuario.IdCargo is None:
        return render(request, "login.html")

    return JsonResponse({"status": "ok", "CargoUsuario": usuario.IdCargo.Nombre})

def validar_cargo(request, cargo_recibido):

    # Verificar autenticación
    if not request.user.is_authenticated:
        return render(request, "login.html")

    cargo_usuario = request.user.IdCargo.Nombre if request.user.IdCargo else ""

    # Comparación estricta
    if cargo_usuario != cargo_recibido:
        return JsonResponse({
            "status": "error",
            "message": "Cargo inválido o manipulado desde el cliente."
        }, status=403)

    # Si coincide → todo bien
    return None

#endregion Cargo

#region Correo

def EnviarCorreo(request):
    if not request.user.is_authenticated:
        return render(request, "login.html")
    
    if request.method == "POST":
        id_personal = request.POST.get("idPersonal")
        titulo = request.POST.get("tituloCorreo")
        mensaje = request.POST.get("mensajeCorreo")

        usuario = Usuario.objects.get(Id=id_personal)

        enviado = send_mail(
            subject=titulo,
            message=mensaje,
            from_email='jasson2852@gmail.com',
            recipient_list=[usuario.email],
            fail_silently=False,
        )
        
        if enviado > 0:
            return JsonResponse({'status': 'ok', 'message': '¡Correo enviado con éxito!'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Error al enviar correo'})

#endregion Correo






