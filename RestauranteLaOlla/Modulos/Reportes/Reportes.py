import datetime
import os
from django.http import HttpResponse
from django.shortcuts import render
from jinja2 import Environment, FileSystemLoader
import pdfkit, xlwt

from Application.models import Insumosvarios, Platillo, Proveedor, Tipoplatillo
from Restaurante_La_Olla import settings

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
            rows = Platillo.objects.all().values_list('nombreplatillo', 'precioplatillo',
                                                    'idtipoplatillo', 'descripcionplatillo', 'activo')

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

def ExportarInsumos(request):
    if request.user.is_authenticated:
        try:
            response = HttpResponse(content_type='application/ms-excel')
            response['Content-Disposition'] = 'attachment; filename=Insumos_' +\
                str(datetime.datetime.now())+'.xls'
            wb = xlwt.Workbook(encoding='utf-8')
            ws = wb.add_sheet('Insumos')
            row_num = 0
            font_style = xlwt.XFStyle()
            font_style.font.bold = True

            Columns = ['Nombre Insumo', 'Stock',
                    'Presentacion', 'Unidad Medida ID', 'Estado']

            for col_num in range(len(Columns)):
                ws.write(row_num, col_num, Columns[col_num], font_style)

            font_style = xlwt.XFStyle()
            rows = Insumosvarios.objects.all().values_list(
                'nombreinsumo', 'stock', 'presentacion', 'idunidadmedida', 'activo')

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

def ExportarProveedores(request):
    if request.user.is_authenticated:
        try:
            response = HttpResponse(content_type='application/ms-excel')
            response['Content-Disposition'] = 'attachment; filename=Proveedores_' +\
                str(datetime.datetime.now())+'.xls'
            wb = xlwt.Workbook(encoding='utf-8')
            ws = wb.add_sheet('Proveedores')
            row_num = 0
            font_style = xlwt.XFStyle()
            font_style.font.bold = True

            Columns = ['Nombre Proveedor', 'Direccion', 'Telefono', 'Correo', 'Estado']

            for col_num in range(len(Columns)):
                ws.write(row_num, col_num, Columns[col_num], font_style)

            font_style = xlwt.XFStyle()
            rows = Proveedor.objects.all().values_list('nombreprov', 'direccionprov',
                                                    'telefonoprov', 'correoprov', 'activo')

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
            rows = Tipoplatillo.objects.all().values_list('nombretp', 'activo')

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
            # ruta_template = 'C:/Users/Hops/OneDrive/Escritorio/Universidad/Proyectos pa Monografia/Restaurante-La-Olla/Restaurante_La_Olla/Templates/Platillos_PDF.html'
            # ruta_template = 'C:/Users/samue/OneDrive/Escritorio/Universidad/Proyectos pa Monografia/Restaurante-La-Olla/Restaurante_La_Olla/Templates/Platillos_PDF.html'
        
            directorio = os.getcwd()

            ruta_template = os.path.normpath(directorio + '/Restaurante-La-Olla/Restaurante_La_Olla/Templates/Platillos_PDF.html')
            segmentos = ruta_template.split('\\')
            ruta = '/'.join(segmentos)
            ruta_template = ruta.replace('/Restaurante-La-Olla/', '/')

            print("********************** P D F *************************")
            print(directorio)
            print()
            print(ruta_template)
            print()
            print(segmentos)
            print()
            print(os.path.isfile(ruta_template))
            print()

            # C:\Users\ASUS\Documents\5T2\Tendencias tecnológicas\Proyecto\Restaurante-La-Olla\Restaurante_La_Olla\Templates\Platillos_PDF.html
        
            if not os.path.isfile(ruta_template):
                return HttpResponse("Error: El archivo HTML del template no existe.")

            ruta = os.path.dirname(ruta_template)
            nombre_template = os.path.basename(ruta_template)

            env = Environment(loader=FileSystemLoader(ruta))
            template = env.get_template(nombre_template)
            platillos = Platillo.objects.filter(activo="activo").order_by('nombreplatillo').values()
            # <<<<<<< HEAD

            # filtro de tipo platillo
            tp = Tipoplatillo.objects.filter(activo="activo").values()
    
            
            # nuevo elemento a contexto
            html = template.render({'platillos': platillos, 'tipoplatillos' : tp})
            # =======
            tp = Tipoplatillo.objects.filter(activo="activo").values()
        
            html = template.render({'platillos': platillos,'tipoplatillos': tp})
            # >>>>>>> 32d43393723fceb8ea28adf52f72683109f47250
        
            config = pdfkit.configuration(wkhtmltopdf=settings.WKHTMLTOPDF_CMD)
            pdf = pdfkit.from_string(html, False, configuration=config)

            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="platillos.pdf"'
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

def CreacionTipoPlatillos_PDF(request):
    if request.user.is_authenticated:
        try:
            #ruta_template = 'C:/Users/samue/OneDrive/Escritorio/Universidad/Proyectos pa Monografia/Restaurante-La-Olla/Restaurante_La_Olla/Templates/TipoPlatillos_PDF.html'
        
            directorio = os.getcwd()
            
            ruta_template = os.path.normpath(directorio + '/Restaurante-La-Olla/Restaurante_La_Olla/Templates/TipoPlatillos_PDF.html')
            segmentos = ruta_template.split('\\')
            ruta = '/'.join(segmentos)
            ruta_template = ruta.replace('/Restaurante-La-Olla/', '/')

            if not os.path.isfile(ruta_template):
                return HttpResponse("Error: El archivo HTML del template no existe.")

            ruta = os.path.dirname(ruta_template)
            nombre_template = os.path.basename(ruta_template)

            env = Environment(loader=FileSystemLoader(ruta))
            template = env.get_template(nombre_template)
            tipoPlatillo =  Tipoplatillo.objects.all()
        
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

def CreacionProveedores_PDF(request):
    if request.user.is_authenticated:
        try:
            ruta_template = 'C:/Users/samue/OneDrive/Escritorio/Universidad/Proyectos pa Monografia/Restaurante-La-Olla/Restaurante_La_Olla/Templates/Proveedores_PDF.html'
            if not os.path.isfile(ruta_template):
                return HttpResponse("Error: El archivo HTML del template no existe.")

            ruta = os.path.dirname(ruta_template)
            nombre_template = os.path.basename(ruta_template)

            env = Environment(loader=FileSystemLoader(ruta))
            template = env.get_template(nombre_template)
            Proveedores = Proveedor.objects.all()
            
            html = template.render({'Proveedores': Proveedores})
        
            config = pdfkit.configuration(wkhtmltopdf=settings.WKHTMLTOPDF_CMD)
            pdf = pdfkit.from_string(html, False, configuration=config)

            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="Proveedores.pdf"'
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
