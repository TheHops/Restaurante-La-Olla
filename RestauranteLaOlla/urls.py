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
from RestauranteLaOlla.views import *
from RestauranteLaOlla.Modulos.Inventario import Menu
from RestauranteLaOlla.Modulos.Personal import Personal
from RestauranteLaOlla.Modulos.Personal import MiPerfil
from RestauranteLaOlla.Modulos.Reportes import Reportes
from RestauranteLaOlla.Modulos.Platillos import Platillos
from RestauranteLaOlla.Modulos.TipoPlatillos import TipoPlatillos
from RestauranteLaOlla.Modulos.Ventas import Ventas
# from . import views
 
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name="index"),
    path('login/', loginUser, name="loginUser"),
    path('logout/', logoutUser, name="logoutUser"),
    path('inventario/', Menu.inventario_platillos, name="inventario"),
    path('platillos/', Menu.inventario_platillos, name="inventario_platillos"),
    path('tipoplatillo/', Menu.inventario_tipoplatillo, name="inventario_tipoplatillo"),
    path('personal/', Personal.personal, name="personal"),
    path('cargo/', Personal.cargo, name="cargo"),
    path('venta/', Ventas.venta, name="venta"),
    path('ActualizarPlatillos/', Platillos.Actualizar_Platillos, name="ActualizarPlatillos"),
    path('DarBajaPlatillo/', Platillos.DarBaja_Platillo, name="DarBajaPlatillo"),
    path('AgregarPlatillo/', Platillos.Agregar_Platillo, name="AgregarPlatillo"),
    path('ActualizarTipoPlatillo/', TipoPlatillos.Actualizar_TipoPlatillo, name="ActualizarTipoPlatillo"),
    path('DarBajaTipoPlatillo/', TipoPlatillos.DarBaja_TipoPlatillo, name="DarBajaTipoPlatillo"),
    path('AgregarTIpoPlatillo/', TipoPlatillos.Agregar_TipoPlatillo, name="AgregarTIpoPlatillo"),
    path('ExportarPlatillo/', Reportes.ExportarPlatillo, name="ExportarPlatillo"),
    path('ExportarTipoPlatillo/', Reportes.ExportarTipoPlatillo, name="ExportarTipoPlatillo"),
    path('ExportarPersonal/', Reportes.ExportarPersonal, name="ExportarPersonal"),
    path('AgregarPersonal/', Personal.AgregarPersonal, name="AgregarPersonal"),
    path('ModificarPersonal/',Personal. ModificarPersonal, name = "ModificarPersonal"),
    path('DarBajaPersonal/', Personal.DarBajaPersonal,name="DarBajaPersonal"),
    path('BuscarPlatillo/', Ventas.BuscarPlatillo, name="BuscarPlatillo"),
    path('FiltrarMesas/', Ventas.FiltrarMesas, name="FiltrarMesas"),
    path('OrdenesPendientes/', Ventas.OrdenesPendientes, name="OrdenesPendientes"),
    path('CrearOrden/', Ventas.CrearOrden, name="CrearOrden"),
    path('FacturarOrden/', Ventas.FacturarOrden, name="FacturarOrden"),
    path('CreacionPlatillos_PDF/', Reportes.CreacionPlatillos_PDF, name="CreacionPlatillos_PDF"),
    path('CreacionTipoPlatillos_PDF/',Reportes.CreacionTipoPlatillos_PDF,name="CreacionTipoPlatillos_PDF"),
    path('CancelarOrden/', Ventas.CancelarOrden, name="CancelarOrden"),
    path('GraficaOrdenes/', GraficarOrdenes, name="GraficaOrdenes"),    
    path('FiltrarOrdenes/', FiltrarOrdenes, name="FiltrarOrdenes"),
    path("CambiarAEnPreparacion/", Ventas.CambiarAEnPreparacion, name="CambiarAEnPreparacion"),
    path("CambiarAPreparado/", Ventas.CambiarAPreparado, name="CambiarAPreparado"),
    path("cargo/consultar/", consultar_cargo, name="ConsultaCargo"),
    path("FiltrarPlatillos/", Menu.filtrar_platillos, name="FiltrarPlatillos"),
    path("FiltrarTipoPlatillos/", Menu.filtrar_tipo_platillos, name="FiltrarTipoPlatillos"),
    path("FiltrarPersonal/", Personal.filtrar_personal, name="FiltrarPersonal"),
    path("RestablecerPass/", Personal.RestablecerPass, name="RestablecerPass"),
    path("EnviarCorreo/", EnviarCorreo, name="EnviarCorreo"),
    path("InicioEditar/", Ventas.InicioEditar, name="InicioEditar"),
    path('EditarOrden/', Ventas.EditarOrden, name="EditarOrden"),
    path("InicioIncluir/", Ventas.InicioIncluir, name="InicioIncluir"),
    path("MiPerfil/", MiPerfil.MiPerfil, name="MiPerfil"),
    path("EditarMiPerfil/", MiPerfil.EditarDatosPerfil, name="EditarMiPerfil"),
    path("CambiarPass/", MiPerfil.CambiarPass, name="CambiarPass"),
    path("Reportes/", Reportes.Reportes, name="reportes"),
    path("InicioMostrar/", Reportes.InicioMostrar, name="InicioMostrar"),
    path("ReportesOrdenesFiltradas/", Reportes.ReportesOrdenesFiltradas, name="ReportesOrdenesFiltradas"),
    path("ExportarOrdenes/", Reportes.ExportarOrdenes, name="ExportarOrdenes"),
    path("InicioEditarMesas/", Ventas.InicioEditarMesas, name="InicioEditarMesas"),
    path("DebeCambiarPass/", DebeCambiarPass, name="DebeCambiarPass"),
    path("ForgotPassword/", ForgotPassword, name="ForgotPassword"),
    path("ValidateEmailForgotPass/", ValidateEmailForgotPass, name="ValidateEmailForgotPass"),
    path("ReenviarOTPForgotPass/", ReenviarOTPForgotPass, name="ReenviarOTPForgotPass"),

]

urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)