from decimal import Decimal

from django.test import Client, TestCase
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from .models import Cargo, Usuario, AreaMesa, Mesa, Orden, TipoPlatillo, Platillo, DetalleOrden, OTP

#region UnitTests

class RestauranteModelTest(TestCase):

    def setUp(self):
        """
        Configuración inicial para las pruebas. 
        Se ejecuta antes de cada test.
        """
        # 1. Crear un cargo y un usuario
        self.cargo_admin = Cargo.objects.create(Nombre="Administrador")
        self.usuario = Usuario.objects.create_user(
            username="testuser",
            password="password123",
            Nombres="Juan",
            Apellidos="Pérez",
            IdCargo=self.cargo_admin,
            email="test@laolla.com"
        )

        # 2. Crear infraestructura del restaurante
        self.area = AreaMesa.objects.create(Nombre="Terraza")
        self.mesa = Mesa.objects.create(IdAreaMesa=self.area, Numero=5, Capacidad=4, Estado="1")

        # 3. Crear menú
        self.tipo_comida = TipoPlatillo.objects.create(Nombre="Almuerzos")
        self.platillo = Platillo.objects.create(
            IdTipoPlatillo=self.tipo_comida,
            Nombre="Gallo Pinto con Carne",
            Precio=150.00
        )

    ## --- PRUEBAS DE USUARIO ---
    def test_creacion_usuario(self):
        """Verifica que el usuario se cree con los datos correctos y el cargo asignado."""
        self.assertEqual(self.usuario.username, "testuser")
        self.assertEqual(self.usuario.IdCargo.Nombre, "Administrador")
        self.assertTrue(self.usuario.check_password("password123"))

    ## --- PRUEBAS DE PLATILLOS ---
    def test_str_platillo(self):
        """Valida que el método __str__ del platillo devuelva el formato esperado."""
        esperado = f"ID = {self.platillo.Id} | Platillo = Gallo Pinto con Carne | Tipo de platillo = Almuerzos"
        self.assertEqual(str(self.platillo), esperado)

    ## --- PRUEBAS DE ÓRDENES Y DETALLES ---
    def test_recalcular_estado_orden(self):
        """
        Prueba la lógica personalizada de 'recalcular_estado'.
        Si no hay detalles activos, la orden debería marcarse como inactiva (EsActivo="0").
        """
        # Crear una orden
        orden = Orden.objects.create(IdUsuario=self.usuario, AreaDeMesa="Terraza")
        
        # Crear un detalle activo
        detalle = DetalleOrden.objects.create(
            IdOrden=orden,
            IdPlatillo=self.platillo,
            Cantidad=2,
            PrecioVenta=150.00,
            SubTotal=300.00,
            EsActivo="1"
        )
        
        # Ejecutar el método
        orden.recalcular_estado()
        self.assertEqual(orden.EsActivo, "1")

        # Ahora marcamos el detalle como eliminado y recalculamos
        detalle.EsActivo = "0"
        detalle.save()
        orden.recalcular_estado()
        
        self.assertEqual(orden.EsActivo, "0")

    def test_valores_por_defecto_orden(self):
        """Verifica que los campos DecimalField tengan el valor por defecto 0."""
        orden = Orden.objects.create(IdUsuario=self.usuario)
        self.assertEqual(orden.Total, 0)
        self.assertEqual(orden.Propina, 0)
        self.assertEqual(orden.Estado, "1")  # Pendiente por defecto

    ## --- PRUEBAS DE OTP (SEGURIDAD) ---
    def test_creacion_otp(self):
        """Valida que se pueda generar un código OTP asociado al usuario."""
        expiracion = timezone.now() + timedelta(minutes=10)
        otp = OTP.objects.create(
            Usuario=self.usuario,
            Codigo="123456",
            FechaExpiracion=expiracion
        )
        self.assertEqual(otp.Codigo, "123456")
        self.assertFalse(otp.Usado)
        
    def test_integridad_financiera_manual(self):
        """
        Valida que los campos decimales de la Orden acepten y mantengan 
        la precisión necesaria para el sistema de facturación.
        """
        # 1. Definimos valores de prueba
        subtotal_esperado = Decimal("450.50")
        propina_esperada = Decimal("45.05") # 10%
        descuento = Decimal("20.00")
        total_pagar_esperado = (subtotal_esperado + propina_esperada) - descuento

        # 2. Creamos la orden asignando los valores manualmente (como lo harías en tu View)
        orden = Orden.objects.create(
            IdUsuario=self.usuario,
            Total=subtotal_esperado,
            Propina=propina_esperada,
            Descuento=descuento,
            TotalPagar=total_pagar_esperado,
            MetodoPago="1", # Efectivo
            Estado="0"      # Pago registrado
        )

        # 3. Recuperamos la orden de la base de datos para asegurar que se guardó bien
        orden_guardada = Orden.objects.get(Id=orden.Id)

        # 4. Verificaciones de precisión decimal
        self.assertEqual(orden_guardada.Total, subtotal_esperado)
        self.assertEqual(orden_guardada.TotalPagar, Decimal("475.55"))
        self.assertEqual(orden_guardada.MetodoPago, "1")
        self.assertEqual(orden_guardada.Estado, "0")
        
#endregion UnitTests

#region IntegrationTests

class IntegrationTest(TestCase):

    def setUp(self):
        # 1. Configuramos el cliente (nuestro navegador fantasma)
        self.client = Client()
        
        # 2. Creamos cargos necesarios
        self.cargo_admin = Cargo.objects.create(Nombre="Administrador")
        self.cargo_mesero = Cargo.objects.create(Nombre="Mesero")

        # 3. Creamos un usuario de prueba activo
        self.user_pass = "pass_olla_123"
        self.usuario = Usuario.objects.create_user(
            username="admin_test",
            email="admin@laolla.com",
            password=self.user_pass,
            IdCargo=self.cargo_admin,
            EsActivo="1"
        )
    
    #region Authentication

    def test_acceso_login_pagina(self):
        """Verifica que la página de login cargue correctamente (Status 200)."""
        response = self.client.get(reverse('loginUser'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "login.html")

    def test_login_exitoso_con_username(self):
        """Simula un inicio de sesión exitoso usando el nombre de usuario."""
        data = {
            'txtUsername': 'admin_test',
            'txtPassword': self.user_pass
        }
        # Enviamos el POST al nombre de la URL 'loginUser'
        response = self.client.post(reverse('loginUser'), data)
        
        # Al ser exitoso, tu vista hace: return redirect("/")
        # El código 302 es redirección en HTTP
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('index'))

    def test_login_exitoso_con_email(self):
        """Prueba la lógica especial de tu vista que detecta el '@' para login por correo."""
        data = {
            'txtUsername': 'admin@laolla.com',
            'txtPassword': self.user_pass
        }
        response = self.client.post(reverse('loginUser'), data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('index'))

    def test_login_fallido_credenciales_incorrectas(self):
        """Verifica que el sistema no deje entrar con claves malas y muestre el mensaje."""
        data = {
            'txtUsername': 'admin_test',
            'txtPassword': 'clave_erronea'
        }
        response = self.client.post(reverse('loginUser'), data)
        
        # No debería redirigir (sigue en la misma página)
        self.assertEqual(response.status_code, 200)
        # Verificamos que el contexto indique error (como lo tienes en tu View)
        self.assertTrue(response.context['is_for_incorrect_login'])
        self.assertEqual(response.context['message'], "Credenciales incorrectas")

    def test_redireccion_por_cargo_mesero(self):
        """
        Prueba la lógica de tu vista 'index'. 
        Si un Mesero hace login, debe ir directo a 'venta/'.
        """
        # Creamos y logueamos un mesero
        mesero = Usuario.objects.create_user(
            username="mesero_test",
            password="password",
            IdCargo=self.cargo_mesero
        )
        self.client.login(username="mesero_test", password="password")
        
        response = self.client.get(reverse('index'))
        
        # Según tu código: elif request.user.IdCargo.Nombre == "Mesero": return redirect("venta/")
        self.assertRedirects(response, '/venta/')

    #endregion Authentication

    #region Graphics

    def test_grafica_ordenes_permisos_y_json(self):
        """Verifica que solo el admin vea gráficas y que el formato JSON sea correcto."""
        self.client.login(username="admin_test", password=self.user_pass)
        response = self.client.get(reverse('GraficaOrdenes'))
        
        self.assertEqual(response.status_code, 200)
        data = response.json() 
        
        # Validamos la estructura del JSON que tu view construye
        self.assertIn("ingresos_v", data)
        self.assertIn("labels_x", data)
        self.assertIn("resumen", data)

    #endregion Graphics
    
    #region ForgotPassWord
    
    def test_forgot_password_solo_admin(self):
        """Verifica que un mesero no pueda usar la recuperación de contraseña de admin."""
        # Usamos el cargo mesero creado en el setUp
        mesero = Usuario.objects.create_user(
            username="mesero_sin_acceso", 
            email="mesero@laolla.com", 
            password="123", 
            IdCargo=self.cargo_mesero, 
            EsActivo="1"
        )
        
        # Intentamos validar su correo en el flujo de "Forgot Password"
        response = self.client.post(
            reverse('ValidateEmailForgotPass'), 
            {'txtCorreoForgotPass': 'mesero@laolla.com'}
        )
        
        # Tu vista devuelve status 400 y el mensaje de restricción
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['message'], "Esta función solo está disponible para administradores")
    
    #endregion ForgotPassWord
    
    #region EdgeCases

    def test_acceso_graficas_sin_login(self):
        """CASO: Entrar a gráficas sin sesión (usando render manual)."""
        self.client.logout()
        response = self.client.get(reverse('GraficaOrdenes'))
        
        # Verificamos que aunque sea 200, la plantilla cargada sea la de login
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "login.html")

    def test_platillo_inactivo_no_aparece(self):
        """
        CASO: Un platillo está marcado como EsActivo="0" (fuera de menú).
        EXPECTATIVA: No debe figurar en la lista de platillos disponibles.
        """
        # Creamos un tipo de platillo y un platillo INACTIVO
        tipo = TipoPlatillo.objects.create(Nombre="Bebidas")
        Platillo.objects.create(
            IdTipoPlatillo=tipo, 
            Nombre="Cerveza Toña", 
            Precio=50, 
            EsActivo="0"
        )
        
        self.client.login(username="admin_test", password=self.user_pass)
        # Suponiendo que tu URL de venta se llama 'Venta'
        response = self.client.get(reverse('venta')) 
        
        # Verificamos que el platillo inactivo NO esté en el contexto enviado al HTML
        platillos_en_vista = response.context['Platillos']
        self.assertFalse(any(p.Nombre == "Cerveza Toña" for p in platillos_en_vista))

    def test_usuario_desactivado_no_puede_loguear(self):
        """
        CASO: Un administrador desactiva a un empleado (EsActivo="0").
        EXPECTATIVA: El sistema debe rechazar sus credenciales aunque la clave sea correcta.
        """
        # Creamos un usuario desactivado
        Usuario.objects.create_user(
            username="ex_empleado", 
            password="123", 
            IdCargo=self.cargo_mesero, 
            EsActivo="0"
        )
        
        data = {'txtUsername': 'ex_empleado', 'txtPassword': '123'}
        response = self.client.post(reverse('loginUser'), data)
        
        # No debe redirigir al index (302), debe quedarse en el login (200) con error
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['message'], "La cuenta está inactiva")

    #endregion EdgeCases

#endregion IntegrationTests


