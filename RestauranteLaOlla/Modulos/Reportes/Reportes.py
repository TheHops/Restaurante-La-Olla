import os
import traceback
import pdfkit
import json

from datetime import datetime, time
from decimal import Decimal

from jinja2 import Environment, FileSystemLoader

from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.formats import date_format
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.db.models import Prefetch, Q

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill, Border, Side
from openpyxl.utils import get_column_letter

from Application.models import Platillo, TipoPlatillo, Orden, DetalleOrden, AreaMesa, Usuario, MesasPorOrden
from RestauranteLaOlla import settings

from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
import io

#region Inicio

def Reportes (request):
    if not request.user.is_authenticated:
        return render(request, "login.html")
    
    if request.user.IdCargo.Nombre == "Armador" or request.user.IdCargo.Nombre == "Mesero":
            return redirect("/")
    
    areas = AreaMesa.objects.filter(EsActivo = "1")
    
    return render(request, "reportes.html", {"Areas": areas})

#endregion Inicio

#region Ordenes filtradas

def ReportesOrdenesFiltradas (request):
    if not request.user.is_authenticated:
        return render(request, "login.html")
    
    if request.user.IdCargo.Nombre == "Armador" or request.user.IdCargo.Nombre == "Mesero":
        return redirect("/")

    if request.method != "GET":
        return JsonResponse(
            {"status": "error", "message": "Método no permitido"},
            status=405
        )

    try:
        fecha_inicio_str = request.GET.get("FechaInicio")
        fecha_fin_str = request.GET.get("FechaFin")
        estado = request.GET.get("Estado")
        
        areasSeleccionadas = request.GET.get("AreasSeleccionadas", "")
        
        print("ESTADO")
        print(estado)
        
        areas_ids = []
        if areasSeleccionadas:
            areas_ids = [int(x) for x in areasSeleccionadas.split(",") if x.isdigit()]

        try:
            ordenes = filtrar_ordenes_fechas_areas(fecha_inicio_str, fecha_fin_str, areas_ids, estado)
        except ValidationError as e:
            return JsonResponse({"status": "error", "message": str(e)})

        contexto = {
            "Ordenes": ordenes,
        }

        return render(
            request,
            "reportes_ordenes_filtradas.html",
            contexto
        )

    except Exception as ex:
        print("\n############### EXCEPCIÓN ###############")
        print(traceback.format_exc())
        print("#########################################\n")
        return JsonResponse(
            {"status": "error", "message": str(ex)},
            status=500
        )

#endregion Ordenes filtradas

#region Mostrar orden

def InicioMostrar(request):
    if not request.user.is_authenticated:
        return render(request, "login.html")
    
    if request.user.IdCargo.Nombre == "Armador" or request.user.IdCargo.Nombre == "Mesero":
        return redirect("/")
    
    idOrden = request.GET.get("IdOrden")
    
    if not idOrden:
        return JsonResponse({"message": "Orden no válida"})

    orden = Orden.objects.prefetch_related(Prefetch('Detalles', queryset=DetalleOrden.objects.filter(EsActivo="1")), Prefetch('Mesas', queryset=MesasPorOrden.objects.filter(EsActivo="1").select_related('IdMesa'))).get(Id=idOrden)
    
    usuario = Usuario.objects.select_related("IdCargo").get(Id=orden.IdUsuario.Id)
    
    contexto = {
        "Orden": orden,
        "Modo": "Mostrar",
        "NombreCreador": usuario.Nombres + " " + usuario.Apellidos,
        "CargoCreador": usuario.IdCargo.Nombre
    }

    return render(request, "detalle_orden_editar.html", contexto)

#endregion Mostrar orden

#region Exportaciones

#region Ordenes

def ExportarOrdenes(request):
    if not request.user.is_authenticated:
        return render(request, "login.html")
    
    if request.method != "POST":
        return JsonResponse({"status": "error", "message": "Método no permitido"}, status=405)
    
    if request.user.IdCargo.Nombre == "Armador" or request.user.IdCargo.Nombre == "Mesero":
        return redirect("/")
    
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"status": "error", "message": "JSON inválido"}, status=400)
    
    try:
        fecha_inicio_str = data["FechaInicio"]
        fecha_fin_str = data["FechaFin"]
        areas_ids = data["AreasSeleccionadas"]
        tipo_exportacion = data["TipoExportacion"]
        incluir_detalles = data["IncluirDetalles"]
        estado = data["Estado"]
    except KeyError as e:
        return JsonResponse({"status": "error", "message": f"Falta el campo {str(e)}"}, status=400)
    
    print(data)
    print(tipo_exportacion)
    
    try:
        ordenes = filtrar_ordenes_fechas_areas(fecha_inicio_str, fecha_fin_str, areas_ids, estado)
    except ValidationError as e:
        return JsonResponse({"status": "error", "message": str(e)})
    
    if tipo_exportacion == "1":
        wb = exportar_excel_ordenes(ordenes, incluir_detalles)
        return descargar_excel(wb, f"ordenes_{fecha_inicio_str}_{fecha_fin_str}.xlsx")
    
    return JsonResponse({
            "status": "error",
            "message": "Exportación no implementada"
        }, status=400)

def exportar_excel_ordenes(ordenes, incluir_detalles = False):
    titulo = "REPORTE DE ÓRDENES"
    columnas = ["N° Orden", "Estado", "Fecha", "Área", "Mesas", "Subtotal", "Propina", "Descuento", "Total a pagar", "Método de pago", "Monto", "Cambio", "Segundo monto"]

    datos = []
    for orden in ordenes:
        mesas = " - ".join(f"#{m.IdMesa.Numero}" for m in orden.Mesas.all())

        datos.append([
            orden.Id,
            orden.get_Estado_display(),
            date_format(
                timezone.localtime(orden.UltimaModificacion),
                "j \\d\\e F \\d\\e Y \\a \\l\\a\\s H:i"
            ),
            orden.IdAreaDeMesa.Nombre if orden.IdAreaDeMesa else "",
            mesas,
            "C$" + str(orden.Total),
            "C$" + str(orden.Propina),
            "C$" + str(orden.Descuento),
            "C$" + str(orden.TotalPagar),
            orden.get_MetodoPago_display(),
            "C$" + str(orden.Monto),
            "C$" + str(orden.Cambio),
            "C$" + str(orden.SegundoMonto)
        ])

    wb = exportar_excel_datos(titulo, columnas, datos, "Ordenes")
    
    # HOJA 2: DETALLES (OPCIONAL)
    if incluir_detalles:
        ws_detalles = wb.create_sheet(title="Detalles")

        columnas_detalles = [
            "N° Orden", "Consumo", "Cantidad", "Precio", "Subtotal"
        ]

        datos_detalles = []

        for orden in ordenes:
            for detalle in orden.Detalles.filter(EsActivo="1"):
                datos_detalles.append([
                    orden.Id,
                    detalle.IdPlatillo.Nombre,
                    detalle.Cantidad,
                    detalle.PrecioVenta,
                    detalle.Cantidad * detalle.PrecioVenta
                ])

        # Ponemos estilo a la nueva hoja
        poblar_hoja_existente(
            ws_detalles,
            "DETALLES DE ÓRDENES",
            columnas_detalles,
            datos_detalles
        )

    return wb

#endregion Ordenes

#region Platillos

def ExportarPlatillo(request):
    if not request.user.is_authenticated:
        return render(request, "login.html")
    
    if request.user.IdCargo.Nombre == "Armador" or request.user.IdCargo.Nombre == "Mesero":
        return redirect("/")
    
    try:
        tipoExportacion = request.GET.get("Tipo")
        
        print(tipoExportacion)
        
        if tipoExportacion not in ("1","2"):
            return JsonResponse({
                "status": "error",
                "message": "Tipo de exportación inválido"
            }, status=400)
        
        if tipoExportacion == "1":
            return exportar_excel_platillos()
        
        if tipoExportacion == "2":
            return exportar_pdf_platillo()
        
        return JsonResponse({
            "status": "error",
            "message": "Exportación no implementada"
        }, status=400)
    except Exception:
        import traceback
        print()
        print("#################### E X C E P C I O N ########################")
        print("-------------------- 'exportar platillo' --------------------")
        print(traceback.format_exc())
        print("#############################################################")
        print()
        return JsonResponse({
            "status": "error",
            "message": "Error interno al exportar consumos"
        }, status=500)
        
def exportar_excel_platillos():
    columnas = ['Nombre consumo', 'Precio', 'Tipo de consumo', 'Descripcion', 'Estado']
    datos = []

    for nombre, precio, tipo, desc, es_activo in Platillo.objects.values_list(
        'Nombre', 'Precio', 'IdTipoPlatillo__Nombre', 'Descripcion', 'EsActivo'
    ):
        estado_symbol = '✅ Activo' if es_activo in (1, '1', True) else '⛔ Inactivo'
        datos.append([
            nombre,
            precio,
            tipo,
            desc,
            estado_symbol
        ])

    wb = exportar_excel_datos("CONSUMOS", columnas, datos, "Consumos")

    # Preparar respuesta
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    
    filename = 'Consumos_' + timezone.localtime().strftime('%d-%m-%Y') + '.xlsx'
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    wb.save(response)
    
    return response

def exportar_pdf_platillo():
    columnas = ['Nombre consumo', 'Precio', 'Tipo de consumo', 'Descripcion', 'Estado']
    filas = []

    for nombre, precio, tipo, desc, es_activo in Platillo.objects.values_list('Nombre', 'Precio', 'IdTipoPlatillo__Nombre', 'Descripcion', 'EsActivo'):
        estado_symbol = '✅ Activo' if es_activo in (1, '1', True) else '⛔ Inactivo'
        filas.append([
            nombre,
            precio,
            tipo,
            desc,
            estado_symbol
        ])

    return generar_pdf_tabla(
        titulo="CONSUMOS",
        columnas=columnas,
        filas=filas,
        nombre_archivo="Consumos",
        ancho_columnas=[100, 50, 100, 200, 50],
        wrap_columns=[0, 2, 3]
    )
        
#endregion Platillos

#region TipoPlatillos

def ExportarTipoPlatillo(request):
    if not request.user.is_authenticated:
        return render(request, "login.html")
    
    if request.user.IdCargo.Nombre == "Armador" or request.user.IdCargo.Nombre == "Mesero":
        return redirect("/")

    try:
        tipoExportacion = request.GET.get("Tipo")
        
        print(tipoExportacion)
        
        if tipoExportacion not in ("1","2"):
            return JsonResponse({
                "status": "error",
                "message": "Tipo de exportación inválido"
            }, status=400)
        
        if tipoExportacion == "1":
            return exportar_excel_tipo_platillo()
        
        if tipoExportacion == "2":
            return exportar_pdf_tipo_platillo()
        
        return JsonResponse({
            "status": "error",
            "message": "Exportación no implementada"
        }, status=400)
    except Exception:
        import traceback
        print()
        print("#################### E X C E P C I O N ########################")
        print("---------------- 'exportar tipo platillo' ----------------")
        print(traceback.format_exc())
        print("#############################################################")
        
        return JsonResponse({
            "status": "error",
            "message": "Error interno al exportar consumos"
        }, status=500)
        
def exportar_excel_tipo_platillo():
    columnas = ['Nombre', 'Estado']
    datos = []

    for nombre, es_activo in TipoPlatillo.objects.values_list('Nombre', 'EsActivo'):
        estado_symbol = '✅ Activo' if es_activo in (1, '1', True) else '⛔ Inactivo'
        datos.append([
            nombre,
            estado_symbol
        ])

    wb = exportar_excel_datos("TIPO DE CONSUMO", columnas, datos, "Tipos de consumo")

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    filename = 'TipoConsumo_' + timezone.localtime().strftime('%d-%m-%Y') + '.xlsx'
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    wb.save(response)
    return response

def exportar_pdf_tipo_platillo():
    columnas = ["Nombre", "Estado"]
    filas = []

    for nombre, es_activo in TipoPlatillo.objects.values_list("Nombre", "EsActivo"):
        estado = "Activo" if es_activo == "1" else "Inactivo"
        filas.append([nombre, estado])

    return generar_pdf_tabla(
        titulo="TIPOS DE CONSUMO",
        columnas=columnas,
        filas=filas,
        nombre_archivo="TipoConsumo",
        ancho_columnas=[300, 150]
    )
        
#endregion TipoPlatillos

#region Personal
        
def ExportarPersonal(request):
    if not request.user.is_authenticated:
        return render(request, "login.html")
    
    if request.user.IdCargo.Nombre == "Armador" or request.user.IdCargo.Nombre == "Mesero":
        return redirect("/")

    try:
        tipoExportacion = request.GET.get("Tipo")
        
        if tipoExportacion not in ("1","2"):
            return JsonResponse({
                "status": "error",
                "message": "Tipo de exportación inválido"
            }, status=400)
        
        # Para exportar en excel
        if tipoExportacion == "1":
            response = exportar_excel_personal()
            return response
        
        return JsonResponse({
            "status": "error",
            "message": "Exportación no implementada"
        }, status=400)

    except Exception:
        import traceback
        print()
        print("#################### E X C E P C I O N ########################")
        print("---------------- 'exportar tipo platillo' ----------------")
        print(traceback.format_exc())
        print("#############################################################")
        
def exportar_excel_personal():
    columnas = ['Id', 'Nombres y apellidos', 'Usuario', 'Cargo', 'Telefono', 'Correo', 'Estado']
    datos = []

    for id, nombre, apellido, nombre_user, nombre_cargo, telefono, correo, es_activo in Usuario.objects.values_list('Id', 'Nombres', 'Apellidos', 'username', 'IdCargo__Nombre', 'Telefono', 'email', 'EsActivo'):
        estadoData = '✅ Activo' if es_activo in (1, '1', True) else '⛔ Dado de baja'
        datos.append([
            id,
            nombre + " " + apellido,
            nombre_user,
            nombre_cargo,
            telefono,
            correo,
            estadoData
        ])

    wb = exportar_excel_datos("PERSONAL", columnas, datos, "Personal")

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    
    filename = 'Personal_' + timezone.localtime().strftime('%d-%m-%Y') + '.xlsx'
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    wb.save(response)
    return response
        
#endregion Personal

#endregion Exportaciones

#region PDF

def CreacionPlatillos_PDF(request):
    if request.user.is_authenticated:
        try:
            directorio = os.getcwd()
            
            print("\n########## DIRECTORIO ###########")
            print(directorio)

            ruta_template = os.path.normpath(directorio + '/RestauranteLaOlla/Templates/Platillos_PDF.html')
            
            print("\n########## RUTA TEMPLATE ###########")
            print(ruta_template)
            
            segmentos = ruta_template.split('\\')
            
            print("\n########## SEGMENTOS ###########")
            print(segmentos)           

            ruta = '/'.join(segmentos)
            
            print("\n########## RUTA ###########")
            print(ruta)

            if not os.path.isfile(ruta_template):
                return HttpResponse("Error: El archivo HTML del template no existe.")

            ruta = os.path.dirname(ruta_template)
            nombre_template = os.path.basename(ruta_template)

            env = Environment(loader=FileSystemLoader(ruta))
            template = env.get_template(nombre_template)
            platillos = Platillo.objects.filter(EsActivo="1").order_by('Nombre').values()

            # filtro de tipo platillo
            tp = TipoPlatillo.objects.filter(EsActivo="1").values()
    
            # nuevo elemento a contexto
            html = template.render({'platillos': platillos, 'tipoplatillos' : tp})
        
            config = pdfkit.configuration(wkhtmltopdf=settings.WKHTMLTOPDF_CMD)
            pdf = pdfkit.from_string(html, False, configuration=config)

            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="platillos.pdf"'
            response.write(pdf)

            return response
        except Exception as ex:
            print("\n############### EXCEPCIÓN ###############")
            print(traceback.format_exc())
            print("#########################################\n")
            return JsonResponse({'error': str(ex)}, status=500)
    else:
        # Si no lo ha hecho entonces deberá iniciar sesión
        return render(request, "login.html")

def CreacionTipoPlatillos_PDF(request):
    if request.user.is_authenticated:
        try:
            directorio = os.getcwd()
            
            ruta_template = os.path.normpath(directorio + '/RestauranteLaOlla/RestauranteLaOlla/Templates/TipoPlatillos_PDF.html')
            segmentos = ruta_template.split('\\')
            ruta = '/'.join(segmentos)
            ruta_template = ruta.replace('/RestauranteLaOlla/', '/')

            if not os.path.isfile(ruta_template):
                return HttpResponse("Error: El archivo HTML del template no existe.")

            ruta = os.path.dirname(ruta_template)
            nombre_template = os.path.basename(ruta_template)

            env = Environment(loader=FileSystemLoader(ruta))
            template = env.get_template(nombre_template)
            tipoPlatillo =  TipoPlatillo.objects.all()
        
            html = template.render({'tipoPlatillo': tipoPlatillo})
        
            config = pdfkit.configuration(wkhtmltopdf=settings.WKHTMLTOPDF_CMD)
            pdf = pdfkit.from_string(html, False, configuration=config)

            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="Tipo_platillos.pdf"'
            response.write(pdf)
            return response
        except Exception as ex:
            print()
            print("#################### E X C E P C I O N ########################")
            print(ex)
            print("########################################################")
            print()
    else:
        # Si no lo ha hecho entonces deberá iniciar sesión
        return render(request, "login.html")
    
#endregion PDF

#region PublicFunctions

def filtrar_ordenes_fechas_areas(fecha_inicio_str, fecha_fin_str, areas_ids, estado = "0"):
    print(fecha_inicio_str)
    print(fecha_fin_str)
    print(areas_ids)
    
    listaEstado = estado.split(",")
    
    if not fecha_inicio_str or not fecha_fin_str:
        raise ValidationError("Fechas incompletas")

    # Convertir string → date
    fecha_inicio_date = datetime.strptime(fecha_inicio_str, "%Y-%m-%d").date()
    fecha_fin_date = datetime.strptime(fecha_fin_str, "%Y-%m-%d").date()

    # Validación lógica
    if fecha_inicio_date > fecha_fin_date:
        raise ValidationError("La fecha inicio no puede ser mayor a la fecha fin")

    # Ajustar horas
    fecha_inicio = timezone.make_aware(datetime.combine(fecha_inicio_date, time.min), timezone.get_current_timezone())   # 00:00:00
    fecha_fin = timezone.make_aware(datetime.combine(fecha_fin_date, time.max), timezone.get_current_timezone())         # 23:59:59.999999
    
    filtros = Q(
        EsActivo="1",
        UltimaModificacion__range=(fecha_inicio, fecha_fin),
        Estado__in=listaEstado
    )

    # Filtrar por áreas de mesa (opcional)
    if areas_ids:
        filtros &= Q(IdAreaDeMesa__in=areas_ids)

    # ------------------------
    # Query final
    # ------------------------
    ordenes = (
        Orden.objects
        .select_related('IdUsuario', 'IdAreaDeMesa')
        .prefetch_related(Prefetch('Detalles'), Prefetch('Mesas', queryset=MesasPorOrden.objects.filter(EsActivo="1").select_related('IdMesa')))
        .filter(filtros)
        .order_by("-Id")
    )
    
    return ordenes

def exportar_excel_datos(titulo, columnas, datos, sheetName):
    # ==== CREAR LIBRO ====
    wb = Workbook()
    ws = wb.active
    ws.title = sheetName

    # ==== ESTILOS ====
    vino_oscuro = "800000"
    blanco = "FFFFFF"
    font_blanca_sans = Font(bold=True, color=blanco, name="Arial")

    borde_resaltado = Border(
        left=Side(border_style="thin", color="000000"),
        right=Side(border_style="thin", color="000000"),
        top=Side(border_style="thin", color="000000"),
        bottom=Side(border_style="thin", color="000000")
    )

    # ==== TÍTULO ====
    ultima_columna = get_column_letter(len(columnas))
    ws.merge_cells(f"A1:{ultima_columna}1")
    celda_titulo = ws["A1"]
    celda_titulo.value = titulo
    celda_titulo.font = font_blanca_sans
    celda_titulo.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    celda_titulo.fill = PatternFill("solid", fgColor=vino_oscuro)
    celda_titulo.border = borde_resaltado
    ws.row_dimensions[1].height = 25

    # ==== ENCABEZADOS ====
    for col_idx, header in enumerate(columnas, start=1):
        c = ws.cell(row=2, column=col_idx, value=header)
        c.font = font_blanca_sans
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        c.fill = PatternFill("solid", fgColor=vino_oscuro)
        c.border = borde_resaltado
    ws.row_dimensions[2].height = 20

    # ==== DATOS ====
    start_row = 3
    for idx, fila in enumerate(datos, start=0):
        row_index = start_row + idx

        # Color alterno
        fill_color = "FFF5F5" if idx % 2 == 0 else "FFF0E6"

        for col_idx, valor in enumerate(fila, start=1):
            cell = ws.cell(row=row_index, column=col_idx, value=valor)

            # Formato moneda si la columna es "Precio"
            if columnas[col_idx - 1].lower() == "precio" and isinstance(valor, (int, float, Decimal)):
                cell.number_format = u'"C$"#,##0.00'

            cell.fill = PatternFill("solid", fgColor=fill_color)
            cell.border = borde_resaltado

    # ==== AJUSTES VISUALES ====
    ws.freeze_panes = "A3"
    
    for col_idx, header in enumerate(columnas, start=1):
        column_letter = get_column_letter(col_idx)
        max_length = len(str(header))

        for row in ws.iter_rows(
            min_row=2,
            max_row=ws.max_row,
            min_col=col_idx,
            max_col=col_idx
        ):
            cell_value = row[0].value
            if cell_value:
                max_length = max(max_length, len(str(cell_value)))

        ws.column_dimensions[column_letter].width = min(max_length + 4, 50)

    return wb

def poblar_hoja_existente(ws, titulo, columnas, datos):
    vino_oscuro = "800000"
    blanco = "FFFFFF"
    font_blanca_sans = Font(bold=True, color=blanco, name="Arial")

    borde_resaltado = Border(
        left=Side(border_style="thin", color="000000"),
        right=Side(border_style="thin", color="000000"),
        top=Side(border_style="thin", color="000000"),
        bottom=Side(border_style="thin", color="000000")
    )

    ultima_columna = get_column_letter(len(columnas))
    ws.merge_cells(f"A1:{ultima_columna}1")

    ws["A1"].value = titulo
    ws["A1"].font = font_blanca_sans
    ws["A1"].alignment = Alignment(horizontal="center", vertical="center")
    ws["A1"].fill = PatternFill("solid", fgColor=vino_oscuro)
    ws["A1"].border = borde_resaltado
    ws.row_dimensions[1].height = 25

    for col_idx, header in enumerate(columnas, start=1):
        c = ws.cell(row=2, column=col_idx, value=header)
        c.font = font_blanca_sans
        c.alignment = Alignment(horizontal="center", vertical="center")
        c.fill = PatternFill("solid", fgColor=vino_oscuro)
        c.border = borde_resaltado

    start_row = 3
    for idx, fila in enumerate(datos):
        fill_color = "FFF5F5" if idx % 2 == 0 else "FFF0E6"
        for col_idx, valor in enumerate(fila, start=1):
            cell = ws.cell(row=start_row + idx, column=col_idx, value=valor)
            cell.fill = PatternFill("solid", fgColor=fill_color)
            cell.border = borde_resaltado

    ws.freeze_panes = "A3"
    for i, header in enumerate(columnas, start=1):
        ws.column_dimensions[get_column_letter(i)].width = max(len(header) + 5, 15)

def descargar_excel(wb, nombre_archivo):
    print(nombre_archivo)
    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = f'attachment; filename="{nombre_archivo}"'
    wb.save(response)
    return response

def generar_pdf_tabla(
    *,
    titulo: str,
    columnas: list,
    filas: list,
    nombre_archivo: str,
    ancho_columnas=None,
    wrap_columns=None,   # 👈 columnas que deben hacer wrap (índices)
):
    if wrap_columns is None:
        wrap_columns = []

    buffer = io.BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    elementos = []

    # ======================================================
    # ESTILOS
    # ======================================================
    styles = getSampleStyleSheet()

    cell_style = ParagraphStyle(
        name="CellStyle",
        fontSize=9,
        leading=12,
        alignment=0,      
        wordWrap="CJK",   
    )

    # ======================================================
    # PROCESAR FILAS (WRAP DE TEXTO)
    # ======================================================
    filas_procesadas = []

    for fila in filas:
        fila_nueva = []
        for i, valor in enumerate(fila):
            if i in wrap_columns:
                fila_nueva.append(
                    Paragraph(str(valor) if valor is not None else "", cell_style)
                )
            else:
                fila_nueva.append(valor)
        filas_procesadas.append(fila_nueva)

    # ======================================================
    # CONSTRUCCIÓN DE TABLA
    # ======================================================
    total_columnas = len(columnas)

    data = [
        [titulo] + [""] * (total_columnas - 1),  # FILA TÍTULO (SPAN)
        columnas,                                # ENCABEZADOS
        *filas_procesadas                        # DATOS
    ]

    table = Table(data, colWidths=ancho_columnas, repeatRows=2)

    table.setStyle(TableStyle([
        # ======================
        # TÍTULO
        # ======================
        ("SPAN", (0, 0), (-1, 0)),
        ("BACKGROUND", (0, 0), (-1, 0), colors.darkred),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 14),
        ("ALIGN", (0, 0), (-1, 0), "CENTER"),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
        ("TOPPADDING", (0, 0), (-1, 0), 12),

        # ======================
        # ENCABEZADOS
        # ======================
        ("BACKGROUND", (0, 1), (-1, 1), colors.HexColor("#800000")),
        ("TEXTCOLOR", (0, 1), (-1, 1), colors.white),
        ("FONTNAME", (0, 1), (-1, 1), "Helvetica-Bold"),
        ("ALIGN", (0, 1), (-1, 1), "CENTER"),
        ("BOTTOMPADDING", (0, 1), (-1, 1), 8),
        ("TOPPADDING", (0, 1), (-1, 1), 8),

        # ======================
        # CUERPO
        # ======================
        ("ALIGN", (0, 2), (-1, -1), "LEFT"),
        ("VALIGN", (0, 2), (-1, -1), "TOP"),
        ("BACKGROUND", (0, 2), (-1, -1), colors.whitesmoke),

        # ======================
        # BORDES
        # ======================
        ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
    ]))

    elementos.append(table)

    # ======================================================
    # CONSTRUIR PDF
    # ======================================================
    doc.build(elementos)

    buffer.seek(0)

    response = HttpResponse(
        buffer,
        content_type="application/pdf"
    )

    fecha = timezone.localtime().strftime("%d-%m-%Y")
    response["Content-Disposition"] = (
        f'attachment; filename="{nombre_archivo}_{fecha}.pdf"'
    )

    return response

#endregion PublicFunctions