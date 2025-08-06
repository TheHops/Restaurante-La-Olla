import datetime
import os
import traceback
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from jinja2 import Environment, FileSystemLoader
import pdfkit, xlwt

from Application.models import Platillo, TipoPlatillo
from RestauranteLaOlla import settings

#region EXPORTACIONES
def Exportar_ExcelPlatillo(request):
    if request.user.is_authenticated:
        try:
            response = HttpResponse(content_type='application/ms-excel')
            response['Content-Disposition'] = 'attachment; filename=Platillos_' +\
                str(datetime.datetime.now())+'.xls'
            wb = xlwt.Workbook(encoding='utf-8')
            ws = wb.add_sheet('Platillo')
            row_num = 0
            font_style = xlwt.XFStyle()
            font_style.font.bold = True

            Columns = ['Nombre Platillo', 'Precio',
                    'TipoPlatillo', 'Descripcion', 'Estado']

            for col_num in range(len(Columns)):
                ws.write(row_num, col_num, Columns[col_num], font_style)

            font_style = xlwt.XFStyle()
            rows = Platillo.objects.all().values_list('Nombre', 'Precio',
                                                    'IdTipoPlatillo', 'Descripcion', 'EsActivo')

            for row in rows:
                row_num += 1

                for column_num in range(len(row)):
                    ws.write(row_num, column_num, str(row[column_num]), font_style)

            wb.save(response)
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

def ExportarTipoPlatillos(request):
    if request.user.is_authenticated:
        try:
            response = HttpResponse(content_type='application/ms-excel')
            response['Content-Disposition'] = 'attachment; filename=TipoPlatillos_' +\
                str(datetime.datetime.now())+'.xls'
            wb = xlwt.Workbook(encoding='utf-8')
            ws = wb.add_sheet('TipoPlatillos')
            row_num = 0
            font_style = xlwt.XFStyle()
            font_style.font.bold = True

            Columns = ['Tipo de Platillos', 'Estado']

            for col_num in range(len(Columns)):
                ws.write(row_num, col_num, Columns[col_num], font_style)

            font_style = xlwt.XFStyle()
            rows = TipoPlatillo.objects.all().values_list('Nombre', 'EsActivo')

            for row in rows:
                row_num += 1

                for column_num in range(len(row)):
                    ws.write(row_num, column_num, str(row[column_num]), font_style)

            wb.save(response)
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
