import json
import traceback

from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.db import transaction
from django.db.models import Q, Prefetch, Count

from django.core.exceptions import ValidationError

from decimal import Decimal, ROUND_HALF_UP

from Application.models import AreaMesa, DetalleOrden, Orden, Mesa, Usuario, Platillo, MesasPorOrden, TipoPlatillo

# region VENTAS
def venta(request):
    if request.user.is_authenticated:
        if request.user.IdCargo.Nombre == "Armador" or request.user.IdCargo.Nombre == "Cajero":
            return redirect("/")
        
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
                .order_by('Nombre')
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

            # Si es mesero, solo contar sus órdenes
            if cargo_usuario == "Mesero":
                ordenes_query = ordenes_query.filter(IdUsuario=request.user)

            ordenesPendientes = ordenes_query.count()

            contexto = {
                'Tipos': tipos,
                'Platillos': platillo,
                'Mesas': mesa,
                'AreaMesa': AreaM,
                'ordenesPendientes': ordenesPendientes,
                'User': request.user
            }

            return render(request, "venta.html", contexto)
        except Exception as ex:
            print()
            print("#################### E X C E P C I O N ########################")
            print("--------------------------'venta'--------------------------")
            print(traceback.format_exc(ex))
            print("########################################################")
            print()
    else:
        # Si no lo ha hecho entonces deberá iniciar sesión
        return render(request, "login.html")
#endregion

#region FiltrarPlatillo
def BuscarPlatillo(request):
    if request.user.is_authenticated:
        if request.user.IdCargo.Nombre == "Armador" or request.user.IdCargo.Nombre == "Cajero":
            return redirect("/")
        
        try:
            if request.method == "GET":
                Texto = request.GET.get("InputBuscarPlatillo")
                TiposParam = request.GET.get("TiposSeleccionados", "")
                
                print("BUSQUEDA")
                print(Texto)
                print(TiposParam)

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
                ).order_by('Nombre')
                
                print("TIPOS FILTRADOS")
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
        if request.user.IdCargo.Nombre == "Armador" or request.user.IdCargo.Nombre == "Cajero":
            return redirect("/")
        
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
                "CargoUsuario": cargo_usuario,
                "User": request.user
            }
            
            print(request.user)
            print(contexto)

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
    
    if request.user.IdCargo.Nombre == "Armador" or request.user.IdCargo.Nombre == "Cajero":
        return redirect("/")
    
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
    
    if request.user.IdCargo.Nombre == "Armador":
        return redirect("/")

    if request.method != "POST":
        return JsonResponse({"status": "error", "message": "Método no permitido"}, status=405)

    try:
        idOrden = request.POST.get('idOrden')
        motivo = request.POST.get('motivo')

        # Buscar la orden
        orden = Orden.objects.get(Id=idOrden)

        # Actualizar estado y motivo
        orden.Estado = "2"  # Cancelada / Anulada
        orden.Motivo = motivo
        orden.MetodoPago = "5" # N/A
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
        return JsonResponse({"status": "error", "message": "La orden no existe"}, status=404)

    except Exception as ex:
        print("\n############### EXCEPCIÓN ###############")
        print(traceback.format_exc())
        print("#########################################\n")
        return JsonResponse({"status": "error", "message": str(ex)}, status=500)
#endregion AnularOrden

#region FacturarOrden

def redondear(valor): return Decimal(valor).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

def FacturarOrden(request):
    if not request.user.is_authenticated:
        return render(request, "login.html")
    
    if request.user.IdCargo.Nombre == "Armador" or request.user.IdCargo.Nombre == "Mesero":
        return redirect("/")

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
                "message": "Id de orden no proporcionado"
            })
            
        if not idOrden.isdigit():
            return JsonResponse({
                "status": "error",
                "message": "Id de orden inválido"
            })
            
        metodoPago_raw = request.POST.get('metodoPago')
        
        if not metodoPago_raw or not metodoPago_raw.isdigit():
            return JsonResponse({
                "status": "error",
                "message": "Método de pago inválido"
            })
            
        monto       = Decimal(request.POST.get('monto', 0))
        cambio      = Decimal(request.POST.get('cambio', 0))
        
        propina     = Decimal(request.POST.get('propinaOrden', 0))
        porcentajePropina   = Decimal(request.POST.get('porcentajePropinaOrden', 0))
        
        descuento   = Decimal(request.POST.get('descuentoOrden', 0))
        porcentajeDescuento   = Decimal(request.POST.get('porcentajeDescuentoOrden', 0))
        
        metodoPago  = int(metodoPago_raw)
        banco  = request.POST.get('banco')
        numRef      = request.POST.get('numRef')
        segundoMonto = 0.0
        
        for nombre, valor in {
            "monto": monto,
            "propina": propina,
            "cambio": cambio
        }.items():
            if valor < 0:
                return JsonResponse({
                    "status": "error",
                    "message": f"El valor '{nombre}' no puede ser negativo"
                })
                
        if porcentajeDescuento != 0 and (porcentajeDescuento < 10 or porcentajeDescuento > 30):
            return JsonResponse({
                "status": "error",
                "message": "Porcentaje de descuento inválido"
            })
            
        if porcentajePropina < 0 or porcentajePropina > 10:
            return JsonResponse({
                "status": "error",
                "message": "Porcentaje de propina inválido"
            })

        # ===============================
        # Obtener orden
        # ===============================
        orden = Orden.objects.get(Id=idOrden)
        
        if orden.Estado == "0":
            return JsonResponse({
                "status": "error",
                "message": "El pago de la orden ya fue registrado"
            })
            
        if orden.Estado == "2":
            return JsonResponse({
                "status": "error",
                "message": "La orden fue anulada"
            })
            
        total       = orden.Total
        
        if total <= 0:
            return JsonResponse({
                "status": "error",
                "message": "El total de la orden es inválido"
            })
            
        descuento_calculado = redondear(
            ((total * Decimal(porcentajeDescuento)) / Decimal(100)) * -1
        )
            
        propina_calculada = redondear(
            ((total + descuento_calculado) * Decimal(porcentajePropina)) / Decimal(100)
        )
        
        orden.UltimaModificacion = timezone.now()
        
        if banco is not None and banco.strip() == "":
            banco = None
            
        print("Total base: " + str(total))
        print("Descuento (Front): " + str(descuento))
        print("Propina (Front): " + str(propina))
        print("Monto (Front): " + str(monto))
        
        print("Porcentaje descuento: " + str(porcentajeDescuento))
        print("Descuento calculado (Back): " + str(descuento_calculado))
        
        print("Porcentaje propina: " + str(porcentajePropina))
        print("Propina calculada (Back): " + str(propina_calculada))
        
        print("Cambio: " + str(cambio))
        
        if redondear(propina) != propina_calculada:
            return JsonResponse({
                "status": "error",
                "message": "La propina no coincide con el porcentaje enviado"
            })

        if redondear(descuento) != descuento_calculado:
            return JsonResponse({
                "status": "error",
                "message": "El descuento no coincide con el porcentaje enviado"
            })

        totalPagar = calcularTotalPagar(total, propina, descuento)
        
        # ===============================
        # Validaciones por método de pago
        # ===============================
        if metodoPago == 1:  # EFECTIVO
            if monto < total:
                return JsonResponse({
                    "status": "error",
                    "message": "El monto en efectivo no puede ser menor al total"
                })
                

            cambio_calculado = monto - totalPagar

            if redondear(cambio) != redondear(cambio_calculado):
                return JsonResponse({
                    "status": "error",
                    "message": "El cambio no coincide con el monto entregado"
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
                    "message": "El cambio no debe ser mayor al monto"
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
                "message": "Método de pago inválido"
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
            "message": f"¡El pago de la orden #{orden.Id} fue registrado exitosamente!"
        })

    except Orden.DoesNotExist:
        return JsonResponse({
            "status": "error",
            "message": "La orden no existe"
        })

    except Exception as ex:
        print("\n############### EXCEPCIÓN ###############")
        print(traceback.format_exc())
        print("#########################################\n")

        return JsonResponse({
            "status": "error",
            "message": "Ocurrió un error al facturar la orden"
        })
        
def calcularTotalPagar (totalBase, propina, descuento):
    if descuento > 0:
        descuento *= -1
    
    return redondear(Decimal(totalBase) + Decimal(propina) + Decimal(descuento))

#endregion FacturarOrden

#region CambiarAEnPreparacion

def CambiarAEnPreparacion(request):
    if not request.user.is_authenticated:
        return render(request, "login.html")
    
    if request.user.IdCargo.Nombre == "Mesero" or request.user.IdCargo.Nombre == "Cajero":
        return redirect("/")
    
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
                "message": f"¡La orden #{orden.Id} ahora está en preparación!",
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
    
    if request.user.IdCargo.Nombre == "Mesero" or request.user.IdCargo.Nombre == "Cajero":
        return redirect("/")
    
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
                "message": f"¡La orden #{orden.Id} está preparada!",
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
    
    if request.user.IdCargo.Nombre == "Armador":
            return redirect("/")
    
    idOrden = request.GET.get("IdOrden")
    
    if not idOrden:
        return JsonResponse({"message": "Orden no válida"})

    orden = Orden.objects.prefetch_related(Prefetch('Detalles', queryset=DetalleOrden.objects.filter(EsActivo="1")), Prefetch('Mesas', queryset=MesasPorOrden.objects.filter(EsActivo="1").select_related('IdMesa'))).get(Id=idOrden)
    
    contexto = {
        "Orden": orden,
        "Modo": "Editar"
    }

    return render(request, "detalle_orden_editar.html", contexto)

def InicioIncluir(request):
    if not request.user.is_authenticated:
        return render(request, "login.html")
    
    if request.user.IdCargo.Nombre == "Armador":
            return redirect("/")

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
        .filter(
            EsActivo="1",
            IdTipoPlatillo__EsActivo="1"
        )
        .exclude(Id__in=platillos_en_orden)
        .order_by("Nombre")
    )

    contexto = {
        "Platillos": platillos_disponibles
    }

    return render(request, "incluir_platillos_editar.html", contexto)

def InicioEditarMesas(request):
    if not request.user.is_authenticated:
        return render(request, "login.html")
    
    if request.user.IdCargo.Nombre == "Armador":
            return redirect("/")
    
    print("SI ENTRO")

    idOrden = request.GET.get("IdOrden")
    if not idOrden:
        return JsonResponse({"message": "Orden no válida"}, status=400)

    orden = get_object_or_404(Orden, Id=idOrden)

    mesas_orden = (
        MesasPorOrden.objects
        .filter(IdOrden=orden, EsActivo="1")
        .values_list("IdMesa_id", flat=True)
    )

    areas = (
        AreaMesa.objects
        .filter(EsActivo="1")
        .prefetch_related(
            Prefetch(
                "Mesas",
                queryset=Mesa.objects.filter(EsActivo="1"),
                to_attr="mesas_activas"
            )
        )
    )

    contexto = {
        "Orden": orden,
        "Areas": areas,
        "MesasOrden": list(mesas_orden),
    }
    
    print(contexto)

    return render(request, "editar_mesas.html", contexto)

def Editar_area_y_mesas(orden, id_area_mesa_nueva, mesas_nuevas_ids):
    hayCambioAreaMesa = False
    hayCambiosMesas = False

    # ---------- ÁREA DE MESA ----------
    id_area_actual = orden.IdAreaDeMesa_id

    if str(id_area_actual) != str(id_area_mesa_nueva):
        area = get_object_or_404(AreaMesa, Id=id_area_mesa_nueva, EsActivo="1")
        orden.IdAreaDeMesa = area
        orden.AreaDeMesa = area.Nombre
        hayCambioAreaMesa = True
    else:
        area = orden.IdAreaDeMesa  # reutilizamos

    # ---------- VALIDACIÓN DE MESAS ----------
    mesas_invalidas = Mesa.objects.filter(
        Id__in=mesas_nuevas_ids
    ).exclude(
        IdAreaMesa=area,
        EsActivo="1"
    )

    if mesas_invalidas.exists():
        numeros = ", ".join(
            str(m.Numero) for m in mesas_invalidas
        )
        raise ValidationError(
            f"Las siguientes mesas no pertenecen al área '{area.Nombre}': {numeros}"
        )

    # ---------- MESAS ----------
    mesas_actuales_qs = MesasPorOrden.objects.filter(
        IdOrden=orden,
        EsActivo="1"
    )

    mesas_actuales_ids = set(
        mesas_actuales_qs.values_list("IdMesa_id", flat=True)
    )
    mesas_nuevas_ids = set(map(int, mesas_nuevas_ids))

    # Mesas eliminadas
    mesas_a_eliminar = mesas_actuales_ids - mesas_nuevas_ids
    if mesas_a_eliminar:
        MesasPorOrden.objects.filter(
            IdOrden=orden,
            IdMesa_id__in=mesas_a_eliminar
        ).update(EsActivo="0")
        hayCambiosMesas = True

    # Mesas nuevas
    mesas_a_agregar = mesas_nuevas_ids - mesas_actuales_ids
    if mesas_a_agregar:
        for id_mesa in mesas_a_agregar:
            mesa = get_object_or_404(Mesa, Id=id_mesa, EsActivo="1")
            MesasPorOrden.objects.create(
                IdOrden=orden,
                IdMesa=mesa,
                EsActivo="1"
            )
        hayCambiosMesas = True

    return hayCambioAreaMesa, hayCambiosMesas

def EditarOrden (request):
    descripcionFueEditada = False
    detalleNuevo = False
    detalleEditado = False
    detalleEliminado = False
    areaCambiada = False
    mesasCambiadas = False
    cantidadEliminados = 0
    cantidadEditados = 0
    cantidadNuevos = 0
    
    if not request.user.is_authenticated:
        return render(request, "login.html")
    
    if request.method != "POST":
        return JsonResponse({"status": "error", "message": "Método no permitido"}, status=405)
    
    if request.user.IdCargo.Nombre == "Armador":
            return redirect("/")

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"status": "error", "message": "JSON inválido"}, status=400)
    
    # Se hace todo mediante una transacción para evitar inconsistencias
    with transaction.atomic():
        # Se obtiene la orden
        orden = get_object_or_404(Orden, Id=data["idOrden"], EsActivo="1")
        
        if orden.Estado == "0":
            return JsonResponse({
                "status": "error",
                "message": "El pago de la orden ya fue registrado"
            })
            
        if orden.Estado == "2":
            return JsonResponse({
                "status": "error",
                "message": "La orden fue anulada"
            })

        # Se actualiza la información de la orden
        descripcionOrden = data.get("descripcion", orden.Descripcion)
        
        if descripcionOrden is not None and descripcionOrden.strip() == "":
            descripcionOrden = None
            
        if orden.Descripcion != descripcionOrden:
            descripcionFueEditada = True
            
        idAreaMesa = data["idAreaMesa"]
        mesasIdList = data["mesas"]
        
        print("Id area de mesa:")
        print(idAreaMesa)
        print("Mesas:")
        print(mesasIdList)
        
        areaCambiada, mesasCambiadas = Editar_area_y_mesas(
            orden,
            idAreaMesa,
            mesasIdList
        )
        
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
        orden.DescripcionEdicion = obtenerMensajeEdicion(descripcionFueEditada, detalleNuevo, detalleEditado, detalleEliminado, cantidadEliminados, cantidadEditados, cantidadNuevos, areaCambiada, mesasCambiadas)
        orden.save()
        
        orden.recalcular_estado()

    return JsonResponse({
        "status": "ok",
        "message": f"¡Orden #{orden.Id} modificada con éxito!",
        "total": str(total_orden)
    })

def obtenerMensajeEdicion (edicionDescripcion, detalleNuevo, detalleEditado, detalleEliminado, cantidadEliminados, cantidadEditados, cantidadNuevos, areaCambiada, mesasCambiadas):
    mensaje = ""
    
    if edicionDescripcion and detalleNuevo and detalleEditado and detalleEliminado:
        mensajeEliminados = "una eliminación" if cantidadEliminados == 1 else f"{cantidadEliminados} eliminaciones"
        
        mensajeEditados = "hubo una modificación" if cantidadEditados == 1 else f"hubieron {cantidadEditados} modificaciones"
        
        mensajeNuevos = "se agregó un nuevo consumible" if cantidadNuevos == 1 else f"se agregaron {cantidadNuevos} nuevos consumibles"
        
        mensaje = f"Se editó la descripción de la orden, {mensajeNuevos} a la orden y {mensajeEditados} junto con {mensajeEliminados} de los detalles ya existentes"
    
    elif edicionDescripcion and detalleNuevo and detalleEliminado:
        mensajeEliminados = "hubo una eliminación" if cantidadEliminados == 1 else f"hubieron {cantidadEliminados} eliminaciones"
        
        mensajeNuevos = "se agregó un nuevo consumible" if cantidadNuevos == 1 else f"se agregaron {cantidadNuevos} nuevos consumibles"
        
        mensaje = f"Se editó la descripción de la orden, {mensajeNuevos} a la orden y {mensajeEliminados} de los detalles ya existentes"
    
    elif edicionDescripcion and detalleNuevo and detalleEditado:
        mensajeEditados = "hubo una modificación" if cantidadEditados == 1 else f"hubieron {cantidadEditados} modificaciones"
        
        mensajeNuevos = "se agregó un nuevo consumible" if cantidadNuevos == 1 else f"se agregaron {cantidadNuevos} nuevos consumibles"
        
        mensaje = f"Se editó la descripción de la orden, {mensajeNuevos} a la orden y {mensajeEditados} de los detalles ya existentes"
    
    elif edicionDescripcion and detalleEditado and detalleEliminado:
        mensajeEliminados = "una eliminación" if cantidadEliminados == 1 else f"{cantidadEliminados} eliminaciones"
        
        mensajeEditados = "hubo una modificación" if cantidadEditados == 1 else f"hubieron {cantidadEditados} modificaciones"
        
        mensaje = f"Se editó la descripción de la orden y {mensajeEditados} junto con {mensajeEliminados} de los detalles ya existentes"
    
    elif edicionDescripcion and detalleNuevo:
        mensajeNuevos = "se agregó un nuevo consumible" if cantidadNuevos == 1 else f"se agregaron {cantidadNuevos} nuevos consumibles"
        
        mensaje = f"Se editó la descripción de la orden y {mensajeNuevos} a la orden"
    
    elif edicionDescripcion and detalleEliminado:
        mensajeEliminados = "hubo una eliminación" if cantidadEliminados == 1 else f"hubieron {cantidadEliminados} eliminaciones"
        
        mensaje = f"Se editó la descripción de la orden y {mensajeEliminados} en los detalles ya existentes"
    
    elif edicionDescripcion and detalleEditado:
        mensajeEditados = "hubo una modificación" if cantidadEditados == 1 else f"hubieron {cantidadEditados} modificaciones"
        
        mensaje = f"Se editó la descripción de la orden y {mensajeEditados} en los detalles ya existentes"
    
    elif edicionDescripcion:
        mensaje = "Se editó la descripción de la orden"
    
    elif detalleNuevo and detalleEditado and detalleEliminado:
        mensajeEliminados = "una eliminación" if cantidadEliminados == 1 else f"{cantidadEliminados} eliminaciones"
        
        mensajeEditados = "hubo una modificación" if cantidadEditados == 1 else f"hubieron {cantidadEditados} modificaciones"
        
        mensajeNuevos = "Se agregó un nuevo consumible" if cantidadNuevos == 1 else f"Se agregaron {cantidadNuevos} nuevos consumibles"
        
        mensaje = f"{mensajeNuevos} a la orden y {mensajeEditados} junto con {mensajeEliminados} de los detalles ya existentes"
        
    elif detalleNuevo and detalleEliminado:
        mensajeEliminados = "hubo una eliminación" if cantidadEliminados == 1 else f"hubieron {cantidadEliminados} eliminaciones"
        
        mensajeNuevos = "Se agregó un nuevo consumible" if cantidadNuevos == 1 else f"Se agregaron {cantidadNuevos} nuevos consumibles"
        
        mensaje = f"{mensajeNuevos} a la orden y {mensajeEliminados} de los detalles ya existentes"
    
    elif detalleNuevo and detalleEditado:
        mensajeEditados = "hubo una modificación" if cantidadEditados == 1 else f"hubieron {cantidadEditados} modificaciones"
        
        mensajeNuevos = "Se agregó un nuevo consumible" if cantidadNuevos == 1 else f"Se agregaron {cantidadNuevos} nuevos consumibles"
        
        mensaje = f"{mensajeNuevos} a la orden y {mensajeEditados} de los detalles ya existentes"
    
    elif detalleEditado and detalleEliminado:
        mensajeEliminados = "una eliminación" if cantidadEliminados == 1 else f"{cantidadEliminados} eliminaciones"
        
        mensajeEditados = "Hubo una modificación" if cantidadEditados == 1 else f"Hubieron {cantidadEditados} modificaciones"
        
        mensaje = f"{mensajeEditados} junto con {mensajeEliminados} de los detalles ya existentes"
    
    elif detalleNuevo:
        mensajeNuevos = "Se agregó un nuevo consumible" if cantidadNuevos == 1 else f"Se agregaron {cantidadNuevos} nuevos consumibles"
        
        mensaje = f"{mensajeNuevos} a la orden"
    
    elif detalleEliminado:
        mensajeEliminados = "Hubo una eliminación" if cantidadEliminados == 1 else f"Hubieron {cantidadEliminados} eliminaciones"
        
        mensaje = f"{mensajeEliminados} en los detalles ya existentes"
    
    elif detalleEditado:
        mensajeEditados = "Hubo una modificación" if cantidadEditados == 1 else f"Hubieron {cantidadEditados} modificaciones"
        
        mensaje = f"{mensajeEditados} en los detalles ya existentes"
    
    if areaCambiada and mesasCambiadas:
        if mensaje != "":
            mensaje += " - "
        
        mensaje += "Hubieron cambios en el área y en las mesas"
    
    elif mesasCambiadas:
        if mensaje != "":
            mensaje += " - "
        
        mensaje += "Hubieron cambios en las mesas"
        
    if mensaje == "":
        mensaje = None
        
    return mensaje
        
#endregion EditarOrden