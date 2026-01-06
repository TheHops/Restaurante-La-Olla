import datetime
from django.utils import timezone
from decimal import Decimal
import os
import traceback
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from jinja2 import Environment, FileSystemLoader
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill, Border, Side
import pdfkit
from openpyxl.utils import get_column_letter
from django.db.models import Prefetch

from Application.models import Platillo, TipoPlatillo, Orden, DetalleOrden
from RestauranteLaOlla import settings

def Reportes (request):
    if not request.user.is_authenticated:
        return render(request, "login.html")
    
    return render(request, "reportes.html")

def ReportesOrdenesFiltradas (request):
    return render(request, "reportes_ordenes_filtradas.html")

def InicioMostrar(request):
    if not request.user.is_authenticated:
        return render(request, "login.html")
    
    idOrden = request.GET.get("IdOrden")
    
    if not idOrden:
        return JsonResponse({"message": "Orden no válida"})

    orden = Orden.objects.prefetch_related(Prefetch('Detalles', queryset=DetalleOrden.objects.filter(EsActivo="1"))).get(Id=idOrden)
    
    contexto = {
        "Orden": orden,
        "Modo": "Mostrar"
    }

    return render(request, "detalle_orden_editar.html", contexto)

#region EXPORTACIONES
def Exportar_ExcelPlatillo(request):
    if not request.user.is_authenticated:
        return render(request, "login.html")

    try:
        columnas = ['Nombre consumo', 'Precio', 'Tipo de consumo', 'Descripcion', 'Estado']
        datos = []

        for nombre, precio, tipo, desc, es_activo in Platillo.objects.values_list(
            'Nombre', 'Precio', 'IdTipoPlatillo__Nombre', 'Descripcion', 'EsActivo'
        ):
            estado_symbol = '✅' if es_activo in (1, '1', True) else '⛔'
            datos.append([
                nombre,
                precio,
                tipo,
                desc,
                estado_symbol
            ])

        wb = exportar_excel_datos("PLATILLOS", columnas, datos)

        # Preparar respuesta
        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        
        filename = 'Platillos_' + timezone.localtime().strftime('%d-%m-%Y') + '.xlsx'
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        
        wb.save(response)
        
        return response
    except Exception:
        import traceback
        print()
        print("#################### E X C E P C I O N ########################")
        print("-------------------- 'exportar platillo' --------------------")
        print(traceback.format_exc())
        print("#############################################################")
        print()

def ExportarTipoPlatillos(request):
    if not request.user.is_authenticated:
        return render(request, "login.html")

    try:
        columnas = ['Tipo de Platillos', 'Estado']
        datos = []

        for nombre, es_activo in TipoPlatillo.objects.values_list('Nombre', 'EsActivo'):
            estado_symbol = '✅' if es_activo in (1, '1', True) else '⛔'
            datos.append([
                nombre,
                estado_symbol
            ])

        wb = exportar_excel_datos("TIPO DE PLATILLO", columnas, datos)

        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        filename = 'TipoPlatillos_' + timezone.localtime().strftime('%d-%m-%Y') + '.xlsx'
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        wb.save(response)
        return response

    except Exception:
        import traceback
        print()
        print("#################### E X C E P C I O N ########################")
        print("---------------- 'exportar tipo platillo' ----------------")
        print(traceback.format_exc())
        print("#############################################################")
#endregion

#region  DOCUMENTOS PDF
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
#endregion

#region PublicFunctions

def exportar_excel_datos(titulo, columnas, datos):
    # ==== CREAR LIBRO ====
    wb = Workbook()
    ws = wb.active
    ws.title = "Datos"

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
    for i, header in enumerate(columnas, start=1):
        ws.column_dimensions[get_column_letter(i)].width = max(len(header) + 5, 15)

    return wb

#endregion PublicFunctions