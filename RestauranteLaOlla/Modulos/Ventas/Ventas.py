import json
import traceback

from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.db import transaction
from django.db.models import Q, Prefetch, Count

from decimal import Decimal, ROUND_HALF_UP

from Application.models import AreaMesa, DetalleOrden, Orden, Mesa, Usuario, Platillo, MesasPorOrden, TipoPlatillo


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

            cargo_usuario = request.user.IdCargo.Nombre

            ordenes_query = Orden.objects.filter(
                Estado="1",
                EsActivo="1"
            )

            # 🔒 Si es mesero, solo contar sus órdenes
            if cargo_usuario == "Mesero":
                ordenes_query = ordenes_query.filter(IdUsuario=request.user)

            ordenesPendientes = ordenes_query.count()

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
        
        if descripcion is not None and descripcion.strip() == "":
            descripcion = None

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
            orden.IdAreaDeMesa = mesas_objetos[0].IdAreaMesa
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
            "message": f"¡Orden #{orden.Id} creada exitosamente!",
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
            "message": f"¡La orden #{orden.Id} fue anulada exitosamente!"
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

def redondear(valor): return Decimal(valor).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

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
        
        if not idOrden:
            return JsonResponse({
                "status": "error",
                "message": "Id de orden no proporcionado."
            })
            
        if not idOrden.isdigit():
            return JsonResponse({
                "status": "error",
                "message": "Id de orden inválido."
            })
            
        metodoPago_raw = request.POST.get('metodoPago')
        
        if not metodoPago_raw or not metodoPago_raw.isdigit():
            return JsonResponse({
                "status": "error",
                "message": "Método de pago inválido."
            })
            
        monto       = to_float(request.POST.get('monto', 0))
        cambio      = to_float(request.POST.get('cambio', 0))
        propina     = to_float(request.POST.get('propinaOrden', 0))
        descuento   = to_float(request.POST.get('descuentoOrden', 0))
        total       = to_float(request.POST.get('totalOrden', 0))
        metodoPago  = int(metodoPago_raw)
        banco  = request.POST.get('banco')
        numRef      = request.POST.get('numRef')
        segundoMonto = 0.0
        
        for nombre, valor in {
            "monto": monto,
            "propina": propina,
            "total": total,
            "cambio": cambio
        }.items():
            if valor < 0:
                return JsonResponse({
                    "status": "error",
                    "message": f"El valor '{nombre}' no puede ser negativo."
                })
                
        if total <= 0:
            return JsonResponse({
                "status": "error",
                "message": "El total de la orden es inválido."
            })

        # ===============================
        # Obtener orden
        # ===============================
        orden = Orden.objects.get(Id=idOrden)
        
        if orden.Estado == "0":
            return JsonResponse({
                "status": "error",
                "message": "La orden ya fue facturada."
            })
        
        orden.UltimaModificacion = timezone.now()
        
        if banco is not None and banco.strip() == "":
            banco = None
            
        print("Total base: " + str(total))
        print("Propina: " + str(propina))
        print("Descuento: " + str(descuento))
        print("Monto: " + str(monto))
        print("Cambio: " + str(cambio))

        totalPagar = calcularTotalPagar(total, propina, descuento)
        
        # ===============================
        # Validaciones por método de pago
        # ===============================
        if metodoPago == 1:  # EFECTIVO
            if monto < total:
                return JsonResponse({
                    "status": "error",
                    "message": "El monto en efectivo no puede ser menor al total."
                })
                

            cambio_calculado = monto - totalPagar

            if redondear(cambio) != redondear(cambio_calculado):
                return JsonResponse({
                    "status": "error",
                    "message": "El cambio no coincide con el monto entregado."
                })

            orden.TotalPagar = totalPagar
            orden.NumRef = None

        elif metodoPago in (2, 3):  # TARJETA o TRANSFERENCIA
            monto = totalPagar

            cambio = 0

            if metodoPago == 3:
                orden.NumRef = numRef
            else:
                orden.NumRef = None
                
            orden.TotalPagar = totalPagar

        elif metodoPago == 4:
            # Si el cliente va a pagar en efectivo pero quiere cambio
            montoReal = monto - cambio
            
            if montoReal < 0:
                return JsonResponse({
                    "status": "error",
                    "message": "El cambio no debe ser mayor al monto."
                })
            
            # El monto de la tarjeta es la diferencia entre el total a pagar y el monto real en efectivo
            segundoMonto = totalPagar - montoReal
            
            if segundoMonto < 0:
                cambio = monto - totalPagar
                segundoMonto = 0

            orden.TotalPagar = totalPagar
            orden.NumRef = None
        else:
            return JsonResponse({
                "status": "error",
                "message": "Método de pago inválido."
            })

        # ===============================
        # Guardar datos
        # ===============================
        orden.Monto         = monto
        orden.Cambio        = cambio
        orden.Propina       = propina
        orden.Descuento     = descuento
        orden.Total         = total
        orden.MetodoPago    = metodoPago
        orden.Banco         = banco
        #orden.NumRef        = numRef
        orden.SegundoMonto  = segundoMonto
        orden.Estado        = "0"  # Facturada

        orden.save()

        return JsonResponse({
            "status": "ok",
            "message": f"¡La orden #{orden.Id} fue registrada exitosamente!"
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
        
def calcularTotalPagar (totalBase, propina, descuento):
    if descuento > 0:
        descuento *= -1
    
    return float(totalBase) + float(propina) + float(descuento)

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
            return JsonResponse({
                "status": "error",
                "message": "Ocurrió un error cambiar el estado la orden."
            })

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
            return JsonResponse({
                "status": "error",
                "message": "Ocurrió un error cambiar el estado la orden."
            })

#endregion CambiarAPreparado

#region EditarOrden

def InicioEditar(request):
    if not request.user.is_authenticated:
        return render(request, "login.html")
    
    idOrden = request.GET.get("IdOrden")
    
    if not idOrden:
        return JsonResponse({"message": "Orden no válida"})

    orden = Orden.objects.prefetch_related(Prefetch('Detalles', queryset=DetalleOrden.objects.filter(EsActivo="1"))).get(Id=idOrden)
    
    contexto = {
        "Orden": orden,
        "Modo": "Editar"
    }

    return render(request, "detalle_orden_editar.html", contexto)

def InicioIncluir(request):
    if not request.user.is_authenticated:
        return render(request, "login.html")

    idOrden = request.GET.get("IdOrden")

    if not idOrden:
        return JsonResponse({"message": "Orden no válida"}, status=400)

    # Obtener la orden
    orden = get_object_or_404(Orden, Id=idOrden)

    # IDs de platillos ya incluidos en la orden
    platillos_en_orden = (
        DetalleOrden.objects
        .filter(IdOrden=orden, EsActivo="1")
        .values_list("IdPlatillo_id", flat=True)
    )

    # Platillos activos que NO estén en la orden
    platillos_disponibles = (
        Platillo.objects
        .filter(EsActivo="1")
        .exclude(Id__in=platillos_en_orden)
        .order_by("Nombre")
    )

    contexto = {
        "Platillos": platillos_disponibles
    }

    return render(request, "incluir_platillos_editar.html", contexto)

def EditarOrden (request):
    descripcionFueEditada = False
    detalleNuevo = False
    detalleEditado = False
    detalleEliminado = False
    cantidadEliminados = 0
    cantidadEditados = 0
    cantidadNuevos = 0
    
    if not request.user.is_authenticated:
        return render(request, "login.html")
    
    if request.method != "POST":
        return JsonResponse({"status": "error", "message": "Método no permitido"}, status=405)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"status": "error", "message": "JSON inválido"}, status=400)
    
    # Se hace todo mediante una transacción para evitar inconsistencias
    with transaction.atomic():
        # Se obtiene la orden
        orden = get_object_or_404(Orden, Id=data["idOrden"], EsActivo="1")

        # Se actualiza la información de la orden
        descripcionOrden = data.get("descripcion", orden.Descripcion)
        
        if descripcionOrden is not None and descripcionOrden.strip() == "":
            descripcionOrden = None
            
        if orden.Descripcion != descripcionOrden:
            descripcionFueEditada = True
        
        orden.Descripcion = descripcionOrden
        orden.FueEditada = True
        orden.UltimaModificacion = timezone.now()
        orden.Detalles.update(DesdeEdicion=False)
        orden.Detalles.update(EsNuevo=False)
        orden.Detalles.update(EsEliminado=False)
        orden.DescripcionEdicion = None
        orden.save()

        total_orden = Decimal("0.00")

        # 3️⃣ Procesar detalles
        for item in data["detalles"]:
            
            # Se guarda lo primero que ya tenemos a mano
            cantidad = int(item["cantidad"])
            es_activo = item["esActivo"]
            is_new = item["isNew"]

            # Obtener platillo
            platillo = get_object_or_404(Platillo, Id=item["idPlatillo"], EsActivo="1")
            
            # Se guarda el precio y subtotal para el detalle
            precio = platillo.Precio
            subtotal = precio * cantidad
            
            print("Cantidad: " + str(cantidad))
            print("Precio: " + str(precio))
            print("Subtotal: " + str(subtotal))
            print("Es activo: " + es_activo)

            if is_new:
                # Si es nuevo, se crea
                detalle = DetalleOrden.objects.create(
                    IdOrden=orden,
                    IdPlatillo=platillo,
                    Cantidad=cantidad,
                    PrecioVenta=precio,
                    SubTotal=subtotal,
                    EsActivo=es_activo,
                    DesdeEdicion=True,
                    EsNuevo=True
                )
                
                detalleNuevo = True
                cantidadNuevos += 1
            else:
                # Si no es nuevo, es porque ya existe y solo se modifica
                detalle = get_object_or_404(
                    DetalleOrden,
                    Id=item["idDetalle"],
                    IdOrden=orden
                )
                
                fue_editado = (
                    detalle.Cantidad != cantidad or
                    detalle.PrecioVenta != precio or
                    detalle.SubTotal != subtotal or
                    detalle.EsActivo != es_activo
                )
                
                if fue_editado:
                    if es_activo == "0":
                        detalleEliminado = True
                        cantidadEliminados += 1
                        detalle.EsEliminado = True
                    else:
                        detalleEditado = True
                        cantidadEditados += 1

                detalle.Cantidad = cantidad
                detalle.PrecioVenta = precio
                detalle.SubTotal = subtotal
                detalle.EsActivo = es_activo
                detalle.DesdeEdicion = fue_editado
                detalle.save()

            # Se acumula el total para luego guardarlo en la orden
            if es_activo == "1":
                total_orden += subtotal

        # Se actualiza el total de la orden
        orden.Total = total_orden
        orden.DescripcionEdicion = obtenerMensajeEdicion(descripcionFueEditada, detalleNuevo, detalleEditado, detalleEliminado, cantidadEliminados, cantidadEditados, cantidadNuevos)
        orden.save()
        
        orden.recalcular_estado()

    return JsonResponse({
        "status": "ok",
        "message": f"¡Orden #{orden.Id} editada con éxito!",
        "total": str(total_orden)
    })

def obtenerMensajeEdicion (edicionDescripcion, detalleNuevo, detalleEditado, detalleEliminado, cantidadEliminados, cantidadEditados, cantidadNuevos):
    if edicionDescripcion and detalleNuevo and detalleEditado and detalleEliminado:
        mensajeEliminados = "una eliminación" if cantidadEliminados == 1 else f"{cantidadEliminados} eliminaciones"
        
        mensajeEditados = "hubo una modificación" if cantidadEditados == 1 else f"hubieron {cantidadEditados} modificaciones"
        
        mensajeNuevos = "se agregó un nuevo consumo" if cantidadNuevos == 1 else f"se agregaron {cantidadNuevos} nuevos consumos"
        
        return f"Se editó la descripción de la orden, {mensajeNuevos} a la orden y {mensajeEditados} junto con {mensajeEliminados} de los detalles ya existentes"
    
    elif edicionDescripcion and detalleNuevo and detalleEliminado:
        mensajeEliminados = "hubo una eliminación" if cantidadEliminados == 1 else f"hubieron {cantidadEliminados} eliminaciones"
        
        mensajeNuevos = "se agregó un nuevo consumo" if cantidadNuevos == 1 else f"se agregaron {cantidadNuevos} nuevos consumos"
        
        return f"Se editó la descripción de la orden, {mensajeNuevos} a la orden y {mensajeEliminados} de los detalles ya existentes"
    
    elif edicionDescripcion and detalleNuevo and detalleEditado:
        mensajeEditados = "hubo una modificación" if cantidadEditados == 1 else f"hubieron {cantidadEditados} modificaciones"
        
        mensajeNuevos = "se agregó un nuevo consumo" if cantidadNuevos == 1 else f"se agregaron {cantidadNuevos} nuevos consumos"
        
        return f"Se editó la descripción de la orden, {mensajeNuevos} a la orden y {mensajeEditados} de los detalles ya existentes"
    
    elif edicionDescripcion and detalleEditado and detalleEliminado:
        mensajeEliminados = "una eliminación" if cantidadEliminados == 1 else f"{cantidadEliminados} eliminaciones"
        
        mensajeEditados = "hubo una modificación" if cantidadEditados == 1 else f"hubieron {cantidadEditados} modificaciones"
        
        return f"Se editó la descripción de la orden y {mensajeEditados} junto con {mensajeEliminados} de los detalles ya existentes"
    
    elif edicionDescripcion and detalleNuevo:
        mensajeNuevos = "se agregó un nuevo consumo" if cantidadNuevos == 1 else f"se agregaron {cantidadNuevos} nuevos consumos"
        
        return f"Se editó la descripción de la orden y {mensajeNuevos} a la orden"
    
    elif edicionDescripcion and detalleEliminado:
        mensajeEliminados = "hubo una eliminación" if cantidadEliminados == 1 else f"hubieron {cantidadEliminados} eliminaciones"
        
        return f"Se editó la descripción de la orden y {mensajeEliminados} en los detalles ya existentes"
    
    elif edicionDescripcion and detalleEditado:
        mensajeEditados = "hubo una modificación" if cantidadEditados == 1 else f"hubieron {cantidadEditados} modificaciones"
        
        return f"Se editó la descripción de la orden y {mensajeEditados} en los detalles ya existentes"
    
    elif edicionDescripcion:
        return "Se editó la descripción de la orden"
    
    elif detalleNuevo and detalleEditado and detalleEliminado:
        mensajeEliminados = "una eliminación" if cantidadEliminados == 1 else f"{cantidadEliminados} eliminaciones"
        
        mensajeEditados = "hubo una modificación" if cantidadEditados == 1 else f"hubieron {cantidadEditados} modificaciones"
        
        mensajeNuevos = "Se agregó un nuevo consumo" if cantidadNuevos == 1 else f"Se agregaron {cantidadNuevos} nuevos consumos"
        
        return f"{mensajeNuevos} a la orden y {mensajeEditados} junto con {mensajeEliminados} de los detalles ya existentes"
        
    elif detalleNuevo and detalleEliminado:
        mensajeEliminados = "hubo una eliminación" if cantidadEliminados == 1 else f"hubieron {cantidadEliminados} eliminaciones"
        
        mensajeNuevos = "Se agregó un nuevo consumo" if cantidadNuevos == 1 else f"Se agregaron {cantidadNuevos} nuevos consumos"
        
        return f"{mensajeNuevos} a la orden y {mensajeEliminados} de los detalles ya existentes"
    
    elif detalleNuevo and detalleEditado:
        mensajeEditados = "hubo una modificación" if cantidadEditados == 1 else f"hubieron {cantidadEditados} modificaciones"
        
        mensajeNuevos = "Se agregó un nuevo consumo" if cantidadNuevos == 1 else f"Se agregaron {cantidadNuevos} nuevos consumos"
        
        return f"{mensajeNuevos} a la orden y {mensajeEditados} de los detalles ya existentes"
    
    elif detalleEditado and detalleEliminado:
        mensajeEliminados = "una eliminación" if cantidadEliminados == 1 else f"{cantidadEliminados} eliminaciones"
        
        mensajeEditados = "Hubo una modificación" if cantidadEditados == 1 else f"Hubieron {cantidadEditados} modificaciones"
        
        return f"{mensajeEditados} junto con {mensajeEliminados} de los detalles ya existentes"
    
    elif detalleNuevo:
        mensajeNuevos = "Se agregó un nuevo consumo" if cantidadNuevos == 1 else f"Se agregaron {cantidadNuevos} nuevos consumos"
        
        return f"{mensajeNuevos} a la orden"
    
    elif detalleEliminado:
        mensajeEliminados = "Hubo una eliminación" if cantidadEliminados == 1 else f"Hubieron {cantidadEliminados} eliminaciones"
        
        return f"{mensajeEliminados} en los detalles ya existentes"
    
    elif detalleEditado:
        mensajeEditados = "Hubo una modificación" if cantidadEditados == 1 else f"Hubieron {cantidadEditados} modificaciones"
        
        return f"{mensajeEditados} en los detalles ya existentes"
    
    else:
        return None
#endregion EditarOrden