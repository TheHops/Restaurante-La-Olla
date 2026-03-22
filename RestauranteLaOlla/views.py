# Se importa la funcion para las respuestas del sitio web
from django.db.models import Case, When, Count, Sum
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.views.decorators.http import require_POST
from Application.models  import Orden, Platillo, Usuario, DetalleOrden, MesasPorOrden, OTP
from django.contrib import messages
from django.http import JsonResponse
from datetime import datetime, timedelta, time
from django.db.models import Q, Prefetch
from django.db.models.functions import TruncDate
import traceback
from django.core.mail import send_mail
from django.utils import timezone
import secrets
import string
import re
import json

from django.conf import settings

from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

User = get_user_model()

def index(request):
    # Direccion que me llevará al login por defecto
    if request.user.is_authenticated:
        if request.user.IdCargo.Nombre == "Armador":
            return redirect("OrdenesPendientes/")
        elif request.user.IdCargo.Nombre == "Mesero":
            return redirect("venta/")
        
        # Si el usuario ya inició sesión entonces entrará directamente al sistema sin necesidad de volver a iniciar sesión
        return render(request, "inicio.html", {"Cargo": request.user.IdCargo.Nombre, "User": request.user})
    else:
        # Si no lo ha hecho entonces deberá iniciar sesión
        return render(request, "login.html")
    
def DebeCambiarPass(request):
    if not request.user.is_authenticated:
        return redirect("/")
    
    if request.method != "GET":
        return JsonResponse({"status": "error", "message": "Método no permitido"}, status=405)
    
    print(request.user.DebeCambiarPass)
    
    return JsonResponse({"status": "ok", "DebeCambiarPass": request.user.DebeCambiarPass})

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
                return render(request, "login.html", {"is_for_incorrect_login":True, "message": "El correo ingresado no está asociado a ninguna cuenta", "icon": "error"})
        else:
            username_real = entrada

        user = authenticate(request, username=username_real, password=pass_word)

        if user is None:
            messages.error(request, "Credenciales incorrectas.")
            return render(request, "login.html", {"is_for_incorrect_login":True, "message": "Credenciales incorrectas", "icon": "error"})

        if user.EsActivo != "1":
            messages.error(request, "Tu cuenta está inactiva.")
            return render(request, "login.html", {"is_for_incorrect_login":True, "message": "La cuenta está inactiva", "icon": "error"})

        login(request, user)
        return redirect("/")

    return render(request, "login.html", {"is_for_incorrect_login":False, "message": "", "icon": ""})

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
    
    if request.user.IdCargo.Nombre == "Armador" or request.user.IdCargo.Nombre == "Mesero":
            return redirect("/")

    try:
        cargo_usuario = request.user.IdCargo.Nombre
        data = {}

        # 1. Datos para el Administrador (7 días)
        if cargo_usuario == "Administrador":
            hoy_local = timezone.localdate()
            dias = [(hoy_local - timedelta(days=i)) for i in range(6, -1, -1)]
            inicio_rango = timezone.make_aware(datetime.combine(dias[0], time.min))
            fin_rango = timezone.make_aware(datetime.combine(dias[-1], time.max))
            
            ventas_7_dias = Orden.objects.filter(
                Estado="0", EsActivo="1", 
                UltimaModificacion__range=(inicio_rango, fin_rango)
            )
            
            mapeo_ventas = {}
            for factura in ventas_7_dias:
                fecha = factura.UltimaModificacion.astimezone(timezone.get_current_timezone()).date()
                mapeo_ventas[fecha] = mapeo_ventas.get(fecha, 0) + float(factura.TotalPagar)
                
            print(dias)
            
            data["ingresos_v"] = [mapeo_ventas.get(dia, 0) for dia in dias]
            data["labels_x"] = [dias_semana_es[dia.weekday()] for dia in dias]
            data["resumen"] = obtener_metricas_resumen()

        # 2. Datos para el Cajero (Hoy por horas)
        elif cargo_usuario == "Cajero":
            labels_h, valores_h = obtener_ventas_por_horas()
            data["labels_x"] = labels_h
            data["ingresos_v"] = valores_h
            data["cajero_stats"] = obtener_metricas_cajero()

        # 3. Métodos de Pago (Común para ambos, pero podrías filtrar 
        # que el cajero solo vea lo de HOY y el admin 30 días)
        dias_metodos = 1 if cargo_usuario == "Cajero" else 30
        data["metodos_labels"], data["metodos_valores"] = obtener_stats_metodos_pago(dias_metodos)

        return JsonResponse(data)
    except Exception as ex:
        print(traceback.format_exc())
        return JsonResponse({"error": str(ex)}, status=500)
    
def obtener_stats_metodos_pago(dias_atras=30):
    """
    Retorna labels y valores de métodos de pago en un rango de días.
    """
    hoy_local = timezone.localdate()
    fecha_inicio = hoy_local - timedelta(days=dias_atras)
    
    # Límites con zona horaria
    inicio_dt = timezone.make_aware(datetime.combine(fecha_inicio, datetime.min.time()))
    fin_dt = timezone.make_aware(datetime.combine(hoy_local, datetime.max.time()))
    

    # Consulta agrupada
    stats = (
        Orden.objects.filter(
            Estado="0", 
            EsActivo="1",
            UltimaModificacion__range=(inicio_dt, fin_dt)
        )
        .values('MetodoPago')
        .annotate(total=Count('Id'))
        .order_by('-total')
    )

    # Diccionario de traducción según tus modelos
    nombres_map = {
        "1": "Efectivo",
        "2": "Tarjeta",
        "3": "Transferencia",
        "4": "Efectivo y tarjeta",
        "5": "N/A"
    }

    labels = []
    valores = []

    for item in stats:
        nombre = nombres_map.get(item['MetodoPago'], "Otro")
        labels.append(nombre)
        valores.append(item['total'])

    return labels, valores

def obtener_ventas_por_horas():
    hoy = timezone.localdate()
    inicio_hoy = timezone.make_aware(datetime.combine(hoy, time.min))
    fin_hoy = timezone.make_aware(datetime.combine(hoy, time.max))

    bloques = [6, 8, 10, 12, 14, 16, 18, 20, 22]
    labels_horas = ["6AM", "8AM", "10AM", "12MD", "2PM", "4PM", "6PM", "8PM", "10PM"]
    
    # Inicializamos un diccionario para acumular: {6: 0, 8: 0, ...}
    acumulador = {hora: 0.0 for hora in bloques}

    ordenes_hoy = Orden.objects.filter(
        Estado="0", 
        EsActivo="1", 
        UltimaModificacion__range=(inicio_hoy, fin_hoy)
    )

    tz_local = timezone.get_current_timezone()

    for orden in ordenes_hoy:
        # 1. Convertimos la hora de la orden a la zona horaria de Nicaragua
        hora_local = orden.UltimaModificacion.astimezone(tz_local).hour
        
        # 2. Buscamos en qué bloque cae (si es 7:45, entra en el bloque del 6 porque 6 <= 7 < 8)
        # O en tu caso, si usas bloques de 2 horas:
        for hora_bloque in bloques:
            if hora_bloque <= hora_local < (hora_bloque + 2):
                acumulador[hora_bloque] += float(orden.TotalPagar)
                break

    # Convertimos el diccionario a la lista que espera la gráfica
    ventas_por_hora = [acumulador[h] for h in bloques]
    
    print("Ventas procesadas por hora local:", ventas_por_hora)
    return labels_horas, ventas_por_hora

def obtener_metricas_resumen():
    hoy = timezone.localdate()
    hace_30_dias = hoy - timedelta(days=30)
    
    # Límites para los filtros
    inicio_hoy = timezone.make_aware(datetime.combine(hoy, datetime.min.time()))
    fin_hoy = timezone.make_aware(datetime.combine(hoy, datetime.max.time()))
    inicio_30 = timezone.make_aware(datetime.combine(hace_30_dias, datetime.min.time()))
    # inicio_hoy = datetime.combine(hoy, datetime.min.time())
    # fin_hoy = datetime.combine(hoy, datetime.max.time())
    # inicio_30 = datetime.combine(hace_30_dias, datetime.min.time())

    # 1. Total del día (Ventas + Propinas)
    stats_hoy = Orden.objects.filter(
        Estado="0", EsActivo="1",
        UltimaModificacion__range=(inicio_hoy, fin_hoy)
    ).aggregate(
        total_ventas=Sum('Total') + Sum('Descuento'),
        total_propinas=Sum('Propina')
    )
    
    print("#################################")
    print("FILTRO DE FECHAS 30D en DASHBOARD")
    print("INICIO")
    print(inicio_30)
    print("FIN")
    print(fin_hoy)

    # 2. Total últimos 30 días
    stats_30 = Orden.objects.filter(
        Estado="0", EsActivo="1",
        UltimaModificacion__range=(inicio_30, fin_hoy)
    ).aggregate(
        total_periodo=Sum('Total') + Sum('Descuento'),
        total_propinas_periodo=Sum('Propina'),
        total_gran_total=Sum('TotalPagar'),
        total_cantidad_ordenes=Count('Id')
    )

    return {
        "hoy_total": float(stats_hoy['total_ventas'] or 0),
        "hoy_propinas": float(stats_hoy['total_propinas'] or 0),
        "mes_total": float(stats_30['total_periodo'] or 0),
        "mes_propinas": float(stats_30['total_propinas_periodo'] or 0),
        "mes_gran_total": float(stats_30['total_gran_total'] or 0),
        "mes_cantidad_ordenes": float(stats_30['total_cantidad_ordenes'] or 0),
    }
    
def obtener_metricas_cajero():
    hoy = timezone.localdate()
    inicio_hoy = timezone.make_aware(datetime.combine(hoy, time.min))
    fin_hoy = timezone.make_aware(datetime.combine(hoy, time.max))

    # Filtramos órdenes de hoy
    ordenes_hoy = Orden.objects.filter(Estado="0", EsActivo="1", UltimaModificacion__range=(inicio_hoy, fin_hoy))

    # Métricas específicas (Efectivo es ID "1", Tarjeta es ID "2")
    efectivo = ordenes_hoy.filter(MetodoPago="1").aggregate(v=Sum('TotalPagar'), p=Sum('Propina'))
    tarjeta = ordenes_hoy.filter(MetodoPago="2").aggregate(v=Sum('TotalPagar'), p=Sum('Propina'))

    return {
        "hoy_efectivo_total": float(efectivo['v'] or 0),
        "hoy_efectivo_propina": float(efectivo['p'] or 0),
        "hoy_tarjeta_total": float(tarjeta['v'] or 0),
        "hoy_tarjeta_propina": float(tarjeta['p'] or 0),
    }

#endregion GraficarOrdenes

#region FiltrarOrdenes

OPCIONES_DISPONIBLES = {
    "Administrador": ["0", "1", "2", "3", "4", "5"],
    "Mesero": ["1", "4", "3", "7"],
    "Armador": ["1", "4", "6"],
    "Cajero": ["0", "2", "3"]
}

VALORES_POR_DEFECTO = {
    "Administrador": "5",
    "Mesero": "7",
    "Armador": "6",
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
            
        elif EstadoOrden == "7":
            ordenes = ordenes.filter(
                Estado__in=["1", "4", "3"]
            ).order_by(
                Case(
                    When(Estado='1', then=0),
                    When(Estado='4', then=1),
                    When(Estado='3', then=2),
                ),
                '-UltimaModificacion'
            )

        else:
            ordenes = ordenes.filter(
                Estado=EstadoOrden
            ).order_by('-UltimaModificacion')
            
        print("ESTADO ORDEN")
        print(EstadoOrden)

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
            "message": "Cargo inválido o manipulado desde el cliente"
        }, status=403)

    # Si coincide → todo bien
    return None

#endregion Cargo

#region Correo

def EnviarCorreo(request):
    if not request.user.is_authenticated:
        return render(request, "login.html")
    
    if request.user.IdCargo.Nombre == "Armador" or request.user.IdCargo.Nombre == "Mesero" or request.user.IdCargo.Nombre == "Cajero":
            return redirect("/")
    
    if request.method == "POST":
        try:
            id_personal = request.POST.get("idPersonal")
            titulo = request.POST.get("tituloCorreo")
            mensaje = request.POST.get("mensajeCorreo")
            
            usuario = Usuario.objects.get(Id=id_personal)
            mensaje = f"Hola {usuario.Nombres},\n\n" + f"{mensaje}"

            enviado = send_mail(
                subject=titulo,
                message=mensaje,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[usuario.email],
                fail_silently=False,
            )
            
            if enviado > 0:
                return JsonResponse({'status': 'ok', 'message': '¡Correo enviado con éxito!'})
            else:
                return JsonResponse({'status': 'error', 'message': 'Error al enviar correo'})
        except Exception as e:
            return JsonResponse({"ok": False, "message": f"Error al enviar el correo: {str(e)}"})

#endregion Correo

#region ForgotPassword

def generar_otp(longitud=6):
    caracteres = string.digits
    otp = ''.join(secrets.choice(caracteres) for _ in range(longitud))
    return otp

def generar_crear_otp(usuario):
    # Invalidar OTP anteriores no usados
    OTP.objects.filter(
        Usuario=usuario,
        Usado=False
    ).update(Usado=True)
    
    codigo = generar_otp()
    expiracion = timezone.now() + timedelta(minutes=2)

    OTP.objects.create(
        Usuario=usuario,
        Codigo=codigo,
        FechaExpiracion=expiracion
    )

    return codigo, expiracion

def enviar_otp_correo(usuario, otp):
    try:
        asunto = "Código OTP para restablecer contraseña"
        mensaje = f"Hola {usuario.Nombres},\n\nTu código OTP para restablecer tu contraseña es:\n\n{otp}\n\nEste código expirará en 2 minutos. Si no solicitaste este OTP, ignora este mensaje."
        
        enviado = send_mail(
            subject=asunto,
            message=mensaje,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[usuario.email],
            fail_silently=False,
        )

        if enviado <= 0:
            return {"ok": False, "message": "Error al enviar el OTP"}
        
        return {"ok": True, "message": "OTP enviado correctamente al correo"}
    except Exception as e:
        return {"ok": False, "message": f"Error al enviar el OTP: {str(e)}"}

# Método que sirve para renderizar los elementos necesarios para cambiar contraseña desde login
def ForgotPassword(request):
    if request.method == "GET":
        return render(request, "inicio_forgot_password.html")

@require_POST
def ValidateEmailForgotPass(request):

    correo = request.POST.get("txtCorreoForgotPass")

    if not correo:
        return JsonResponse({
            "ok": False,
            "message": "Debes ingresar un correo electrónico"
        }, status=400)

    try:
        usuario = Usuario.objects.select_related("IdCargo").get(email=correo)
    except Usuario.DoesNotExist:
        return JsonResponse({
            "ok": False,
            "message": "No existe ningún usuario asociado a este correo"
        }, status=400)

    try:
        if usuario.EsActivo != "1":
            return JsonResponse({
                "ok": False,
                "message": "El usuario asociado a este correo está inactivo"
            }, status=400)

        if not usuario.IdCargo or usuario.IdCargo.Nombre != "Administrador":
            return JsonResponse({
                "ok": False,
                "message": "Esta función solo está disponible para administradores"
            }, status=400)

        # Caso correcto
        print("ESTE USUARIO ES ADMIN")
        
        otp, expiracion = generar_crear_otp(usuario)
        print("OTP generado:", otp)
        
        segundos_restantes = int((expiracion - timezone.now()).total_seconds())
        
        resultado_envio = enviar_otp_correo(usuario, otp)

        if not resultado_envio["ok"]:
            return JsonResponse({
                "ok": False,
                "message": resultado_envio["message"]
            }, status=400)
        
        contexto = {
            "Usuario": usuario,
            "segundos_restantes": segundos_restantes
        }

        return render(request, "ingresar_otp_forgot_password.html", contexto)
    except Exception as ex:
        print()
        print("#################### E X C E P C I O N ########################")
        print("-----------------------'ForgotPass'--------------------------")
        print(traceback.format_exc(ex))
        print("########################################################")
        print()
        
        return JsonResponse({
            "ok": False,
            "message": "Ocurrió un error al generar el OTP"
        }, status=500)
        
@require_POST
def ReenviarOTPForgotPass(request):
    user_id = request.POST.get("idUsuario")

    try:
        usuario = Usuario.objects.get(Id=user_id)

        otp, expiracion = generar_crear_otp(usuario)
        envio = enviar_otp_correo(usuario, otp)

        if not envio["ok"]:
            return JsonResponse({"ok": False, "message": envio["message"]}, status=400)

        segundos = int((expiracion - timezone.now()).total_seconds())

        return JsonResponse({
            "ok": True,
            "segundos": segundos
        })

    except Exception:
        return JsonResponse({
            "ok": False,
            "message": "Error al reenviar OTP"
        }, status=500)
        
@require_POST
def ValidarOTPForgotPass(request):
    otp_ingresado = request.POST.get("otp")
    id_usuario = request.POST.get("id_usuario")

    # Validar que se envíen los datos
    if not otp_ingresado or not id_usuario:
        return JsonResponse({
            "ok": False,
            "message": "Datos incompletos."
        }, status=400)

    # Validar formato del OTP (6 dígitos numéricos)
    if not re.fullmatch(r"\d{6}", otp_ingresado):
        return JsonResponse({
            "ok": False,
            "message": "El OTP ingresado no es válido."
        }, status=400)

    try:
        # Obtener OTP activo del usuario
        otp_obj = OTP.objects.get(
            Usuario__Id=id_usuario,
            Codigo=otp_ingresado,
            Usado=False
        )
    except OTP.DoesNotExist:
        return JsonResponse({
            "ok": False,
            "message": "El OTP es incorrecto o ya fue utilizado."
        }, status=400)

    # Validar expiración
    if timezone.now() > otp_obj.FechaExpiracion:
        return JsonResponse({
            "ok": False,
            "message": "El OTP ha expirado."
        }, status=400)

    # TODO CORRECTO
    print("OTP CORRECTO")
    
    otp_obj.Usado = True
    otp_obj.save()

    return render(request, "cambiar_pass_forgot_pass.html", {"UserId": id_usuario})

def CambiarPassForgotPass (request):
    if request.method != "POST":
        return JsonResponse({
            "status": "error",
            "message": "Método no permitido"
        }, status=400)
    
    try:
        new_pass = request.POST.get("txtNuevaPassForgotPass")
        verify_pass = request.POST.get("txtVerificarPassForgotPass")
        id_usuario = request.POST.get("userIdValue")

        user = Usuario.objects.get(Id=id_usuario)
        
        print(user)
        
        print("PASS")
        print(new_pass)
        print(verify_pass)

        # 🔹 Verificar coincidencia
        if new_pass != verify_pass:
            return JsonResponse({
                "status": "error",
                "message": "Las contraseñas no coinciden"
            }, status=400)

        # 🔹 Validar contraseña con Django
        try:
            validate_password(new_pass, user=request.user)
        except ValidationError as e:
            return JsonResponse({
                "status": "error",
                "message": " ".join(e.messages)
            }, status=400)

        # 🔹 Cambiar contraseña
        user.set_password(new_pass)
        user.DebeCambiarPass = False
        user.save()

        # 🔹 Mantener sesión activa
        update_session_auth_hash(request, user)

        return render(request, "login.html", {"is_for_change_pass":True, "message": "¡La contraseña fue cambiada con éxito!", "icon": "success"})
    except Exception as ex:
        print()
        print("#################### E X C E P C I O N ########################")
        print(ex)
        print("########################################################")
        print()
        
        return JsonResponse({
            "status": "error",
            "message": "Ocurrió un error al intentar cambiar la contraseña"
        })

#endregion ForgotPassword



