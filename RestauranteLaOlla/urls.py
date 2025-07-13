"""
URL configuration for RestauranteLaOlla project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from RestauranteLaOlla.settings import MEDIA_URL, MEDIA_ROOT
# from RestauranteLaOlla.views import *
# from RestauranteLaOlla.Modulos.Inventario import Inventario
# from RestauranteLaOlla.Modulos.Personal import Personal
# from RestauranteLaOlla.Modulos.Insumos import Insumos
# from RestauranteLaOlla.Modulos.Reportes import Reportes
# from RestauranteLaOlla.Modulos.Platillos import Platillos
# from RestauranteLaOlla.Modulos.TipoPlatillos import TipoPlatillos
# from RestauranteLaOlla.Modulos.Ventas import Ventas
# from . import views
# from django.conf.urls import url
 
urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', index, name="index"),
    # path('login/', loginUser, name="loginUser"),
    # path('logout/', logoutUser, name="logoutUser"),
    # path('inventario/', Inventario.inventario_platillos, name="inventario"),
    # path('platillos/', Inventario.inventario_platillos, name="inventario_platillos"),
    # path('tipoplatillo/', Inventario.inventario_tipoplatillo, name="inventario_tipoplatillo"),
    # path('proveedores/', Inventario.inventario_proveedores, name="inventario_proveedores"),
    # path('personal/', Personal.personal, name="personal"),
    # path('cargo/', Personal.cargo, name="cargo"),
    # path('venta/', Ventas.venta, name="venta"),
    # path('detalle/', Ventas.Detalle_Proveedor, name="detalle"),
    # path('ActualizarPlatillos/', Platillos.Actualizar_Platillos, name="ActualizarPlatillos"),
    # path('DarBajaPlatillo/', Platillos.DarBajar_Platillo, name="DarBajaPlatillo"),
    # path('AgregarPlatillo/', Platillos.Agregar_Platillo, name="AgregarPlatillo"),
    # path('ActualizarTipoPlatillo/', TipoPlatillos.Actualizar_TipoPlatillo, name="ActualizarTipoPlatillo"),
    # path('DarBajaTipoPlatillo/', TipoPlatillos.DarBaja_TipoPlatillo, name="DarBajaTipoPlatillo"),
    # path('AgregarTIpoPlatillo/', TipoPlatillos.Agregar_TipoPlatillo, name="AgregarTIpoPlatillo"),
    # path('ExportarPlatillo/', Reportes.Exportar_ExcelPlatillo, name="ExportarPlatillo"),
    # path('ExportarInsumos/', Reportes.ExportarInsumos, name="ExportarInsumos"),
    # path('ExportarProveedor/', Reportes.ExportarProveedores, name="ExportarProveedor"),
    # path('ExportarTipoPlatillo/', Reportes.ExportarTipoPlatillos, name="ExportarTipoPlatillo"),
    # path('AgregarPersonal/', Personal.AgregarPersonal, name="AgregarPersonal"),
    # path ('ModificarPersonal/',Personal. ModificarPersonal, name = "ModificarPersonal"),
    # path('DarBajaPersonal/', Personal.DarBajaPersonal,name="DarBajaPersonal"),
    # path('BuscarPlatillo/', Ventas.BuscarPlatillo, name="BuscarPlatillo"),
    # path('FiltrarMesas/', Ventas.FiltrarMesas, name="FiltrarMesas"),
    # path('OrdenesPendientes/', Ventas.OrdenesPendientes, name="OrdenesPendientes"),
    # path('CrearOrden', Ventas.CrearOrden, name="CrearOrden"),
    # path('FacturarOrden', Ventas.FacturarOrden, name="FacturarOrden"),
    # path('CreacionPlatillos_PDF/', Reportes.CreacionPlatillos_PDF, name="CreacionPlatillos_PDF"),
    # path('CreacionTipoPlatillos_PDF',Reportes.CreacionTipoPlatillos_PDF,name="CreacionTipoPlatillos_PDF"),
    # path('CreacionProveedores_PDF', Reportes.CreacionProveedores_PDF,name="CreacionProveedores_PDF"),
    # path('CancelarOrden', Ventas.CancelarOrden, name="CancelarOrden"),
    # path('GraficaFacturas', GraficaFacturas, name="GraficaFacturas"),    
    # path('FiltrarOrdenes/', FiltrarOrdenes, name="FiltrarOrdenes")

]

urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)