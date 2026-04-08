from decimal import Decimal

from django.test import Client, TestCase
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from .models import Cargo, Usuario, AreaMesa, Mesa, Orden, TipoPlatillo, Platillo, DetalleOrden, OTP

from django.contrib.auth.hashers import check_password

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

#region MenuTests

class MenuIntegrationTest(TestCase):

    def setUp(self):
        self.client = Client()
        # Cargos
        self.cargo_admin = Cargo.objects.create(Nombre="Administrador")
        self.cargo_cajero = Cargo.objects.create(Nombre="Cajero")
        self.cargo_mesero = Cargo.objects.create(Nombre="Mesero")

        # Usuarios con correos únicos para evitar el IntegrityError
        self.pass_comun = "Pass123"
        
        self.admin = Usuario.objects.create_user(
            username="admin_inv", 
            email="admin_inv@laolla.com", # <--- Agregamos esto
            password=self.pass_comun, 
            IdCargo=self.cargo_admin, 
            EsActivo="1"
        )
        
        self.cajero = Usuario.objects.create_user(
            username="cajero_inv", 
            email="cajero_inv@laolla.com", # <--- Agregamos esto
            password=self.pass_comun, 
            IdCargo=self.cargo_cajero, 
            EsActivo="1"
        )

        # Datos base de inventario (estos están bien)
        self.tipo_activo = TipoPlatillo.objects.create(Nombre="Bebidas", EsActivo="1")
        self.tipo_inactivo = TipoPlatillo.objects.create(Nombre="Postres", EsActivo="0")
        
        self.platillo_activo = Platillo.objects.create(
            Nombre="Coca Cola", Precio=30, IdTipoPlatillo=self.tipo_activo, EsActivo="1"
        )
        self.platillo_eliminado = Platillo.objects.create(
            Nombre="Fanta", Precio=25, IdTipoPlatillo=self.tipo_activo, EsActivo="0"
        )

    #region Acceso y Seguridad
    
    def test_cajero_no_puede_ver_inventario(self):
        """Verifica que el Cajero sea redirigido al index al intentar entrar a inventario."""
        self.client.login(username="cajero_inv", password=self.pass_comun)
        response = self.client.get(reverse('inventario_platillos'))
        self.assertRedirects(response, reverse('index'))

    def test_admin_puede_ver_inventario(self):
        """Verifica que el Admin tenga acceso exitoso."""
        self.client.login(username="admin_inv", password=self.pass_comun)
        response = self.client.get(reverse('inventario_platillos'))
        self.assertEqual(response.status_code, 200)
        
    #endregion Acceso y Seguridad

    #region Filtrado de Platillos
    
    def test_filtrar_platillos_activos(self):
        """Verifica que por defecto no se muestren platillos con EsActivo='0'."""
        self.client.login(username="admin_inv", password=self.pass_comun)
        # verEliminados = 0 por defecto
        response = self.client.get(reverse('FiltrarPlatillos'), {'verEliminados': '0'})
        
        platillos = response.context['Platillos']
        self.assertIn(self.platillo_activo, platillos)
        self.assertNotIn(self.platillo_eliminado, platillos)

    def test_filtrar_platillos_incluir_eliminados(self):
        """Verifica que al marcar verEliminados=1 aparezcan todos."""
        self.client.login(username="admin_inv", password=self.pass_comun)
        response = self.client.get(reverse('FiltrarPlatillos'), {'verEliminados': '1'})
        
        platillos = response.context['Platillos']
        self.assertEqual(platillos.count(), 2)
        self.assertIn(self.platillo_eliminado, platillos)
        
    #endregion Filtrado de Platillos

    #region Lógica de Negocio Específica
    
    def test_ocultar_platillos_de_tipo_inactivo(self):
        """
        PRUEBA CRÍTICA: Si el TipoPlatillo está inactivo, el platillo no debe 
        aparecer aunque el platillo en sí esté activo.
        """
        # Creamos un platillo cuyo TIPO está inactivo
        Platillo.objects.create(
            Nombre="Pastel de Chocolate", Precio=40, 
            IdTipoPlatillo=self.tipo_inactivo, EsActivo="1"
        )
        
        self.client.login(username="admin_inv", password=self.pass_comun)
        response = self.client.get(reverse('inventario_platillos'))
        
        platillos = response.context['Platillos']
        # No debería haber ningún platillo de tipo "Postres" (inactivo)
        self.assertFalse(any(p.IdTipoPlatillo.Nombre == "Postres" for p in platillos))

    def test_filtrar_tipos_activos_vs_todos(self):
        """Verifica el filtrado en la lista de categorías (TipoPlatillo)."""
        self.client.login(username="admin_inv", password=self.pass_comun)
        
        # Solo activos
        res_activos = self.client.get(reverse('FiltrarTipoPlatillos'), {'verEliminados': '0'})
        self.assertEqual(res_activos.context['TypePlatillo'].count(), 1)
        
        # Todos
        res_todos = self.client.get(reverse('FiltrarTipoPlatillos'), {'verEliminados': '1'})
        self.assertEqual(res_todos.context['TypePlatillo'].count(), 2)
    
    #endregion Lógica de Negocio Específica

#endregion MenuTests

#region PersonalTests

class PersonalTest(TestCase):
    def setUp(self):
        self.client = Client()
        
        # 1. Crear Cargos
        self.cargo_admin = Cargo.objects.create(Id=1, Nombre="Administrador", EsActivo="1")
        self.cargo_mesero = Cargo.objects.create(Id=2, Nombre="Mesero", EsActivo="1")
        
        # 2. Crear Usuarios con EMAILS ÚNICOS
        self.admin_user = Usuario.objects.create_user(
            username="admin_test",
            email="admin@laolla.com",  # <--- Agrega esto
            password="password123",
            Nombres="Admin",
            Apellidos="User",
            IdCargo=self.cargo_admin,
            EsActivo="1"
        )
        
        self.mesero_user = Usuario.objects.create_user(
            username="mesero_test",
            email="mesero@laolla.com", # <--- Agrega esto
            password="password123",
            Nombres="Mesero",
            Apellidos="User",
            IdCargo=self.cargo_mesero,
            EsActivo="1"
        )

    ## --- PRUEBAS DE ACCESO (SEGURIDAD) ---

    def test_acceso_denegado_a_mesero(self):
        """Verifica que un mesero sea redirigido al home si intenta ver personal."""
        self.client.login(username="mesero_test", password="password123")
        response = self.client.get(reverse('personal')) # Asegúrate que el name en urls.py sea 'personal'
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/")

    def test_acceso_permitido_a_admin(self):
        """Verifica que un administrador pueda entrar a la gestión de personal."""
        self.client.login(username="admin_test", password="password123")
        response = self.client.get(reverse('personal'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "personal.html")

    ## --- PRUEBAS DE CRUD (JSON RESPONSES) ---

    def test_agregar_personal_exitoso(self):
        """Prueba la creación de un nuevo usuario mediante POST."""
        self.client.login(username="admin_test", password="password123")
        data = {
            'Nombre': 'Juan',
            'Apellido': 'Perez',
            'User': 'jperez',
            'Pass': 'Juan.2026*',
            'Correo': 'juan@gmail.com',
            'Telefono': '88888888',
            'Cargo': self.cargo_mesero.Id
        }
        response = self.client.post(reverse('AgregarPersonal'), data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'ok')
        self.assertTrue(Usuario.objects.filter(username='jperez').exists())

    def test_agregar_personal_usuario_duplicado(self):
        """No debe permitir crear un usuario con un username que ya existe."""
        self.client.login(username="admin_test", password="password123")
        data = {
            'Nombre': 'Otro',
            'Apellido': 'Admin',
            'User': 'admin_test', # Ya existe en setUp
            'Pass': '123',
            'Cargo': self.cargo_admin.Id
        }
        response = self.client.post(reverse('AgregarPersonal'), data)
        self.assertEqual(response.json()['status'], 'error')
        self.assertIn('ya existe', response.json()['message'])

    ## --- PRUEBAS DE LÓGICA ESPECIAL ---

    def test_restablecer_contrasena_temporal(self):
        """Verifica que se genere una nueva clave y el flag DebeCambiarPass sea True."""
        self.client.login(username="admin_test", password="password123")
        response = self.client.post(reverse('RestablecerPass'), {'ID': self.mesero_user.Id})
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['status'], 'ok')
        
        # Recargar usuario de la BD
        self.mesero_user.refresh_from_db()
        self.assertTrue(self.mesero_user.DebeCambiarPass)
        # Verificar que la nueva contraseña funciona (encriptada)
        self.assertTrue(check_password(data['new_pass'], self.mesero_user.password))

    def test_dar_baja_personal(self):
        """Prueba el borrado lógico (EsActivo = '0')."""
        self.client.login(username="admin_test", password="password123")
        self.client.post(reverse('DarBajaPersonal'), {'ID': self.mesero_user.Id})
        
        self.mesero_user.refresh_from_db()
        self.assertEqual(self.mesero_user.EsActivo, "0")

    def test_filtrar_personal_excluir_usuario_actual(self):
        """La lista de personal no debería incluir al usuario que está logueado."""
        self.client.login(username="admin_test", password="password123")
        response = self.client.get(reverse('FiltrarPersonal'))
        
        personal_list = response.context['Personal']
        # El admin no debería verse a sí mismo en la lista
        self.assertNotIn(self.admin_user, personal_list)
        # Pero sí debería ver al mesero
        self.assertIn(self.mesero_user, personal_list)

#endregion PersonalTests

#region MiPerfilTests

class PerfilTest(TestCase):
    def setUp(self):
        self.client = Client()
        
        # Cargos necesarios
        self.cargo = Cargo.objects.create(Id=1, Nombre="Mesero", EsActivo="1")
        
        # Usuario para las pruebas
        self.user_pass = "OldPassword123!"
        self.user = Usuario.objects.create_user(
            username="testuser",
            email="test@laolla.com",
            password=self.user_pass,
            Nombres="Test",
            Apellidos="User",
            IdCargo=self.cargo,
            Telefono="12345678",
            EsActivo="1"
        )
        
        # Otro usuario para probar duplicados
        self.other_user = Usuario.objects.create_user(
            username="otheruser",
            email="other@laolla.com",
            password="OtherPassword123!",
            IdCargo=self.cargo
        )
        
        # Loguear al usuario principal
        self.client.login(username="testuser", password=self.user_pass)

    ## --- Pruebas de Visualización ---

    def test_acceso_mi_perfil_autenticado(self):
        """Verifica que un usuario logueado pueda ver su perfil."""
        response = self.client.get(reverse('MiPerfil'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "mi_perfil.html")

    ## --- Pruebas de Edición de Datos ---

    def test_editar_perfil_exitoso(self):
        """Prueba la actualización válida de correo y teléfono."""
        data = {
            "txtCorreoEditarPerfil": "nuevo@laolla.com",
            "txtTelefonoEditarPerfil": "88888888",
            "txtUserNameEditarPerfil": "testuser_nuevo"
        }
        response = self.client.post(reverse('EditarMiPerfil'), data)
        self.assertEqual(response.json()["status"], "ok")
        
        # Verificar en base de datos
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, "nuevo@laolla.com")
        self.assertEqual(self.user.username, "testuser_nuevo")

    def test_editar_perfil_email_duplicado(self):
        """No debe permitir usar un email que ya pertenece a otro usuario."""
        data = {
            "txtCorreoEditarPerfil": "other@laolla.com", # Ya lo tiene other_user
            "txtTelefonoEditarPerfil": "12345678",
            "txtUserNameEditarPerfil": "testuser"
        }
        response = self.client.post(reverse('EditarMiPerfil'), data)
        self.assertEqual(response.json()["status"], "error")
        self.assertIn("correo ya está registrado", response.json()["message"])

    ## --- Pruebas de Cambio de Contraseña ---

    def test_cambiar_pass_exitoso(self):
        """Prueba el cambio de contraseña con datos correctos."""
        new_pass = "NewStrongPass2026!"
        data = {
            "OldPass": self.user_pass,
            "NewPass": new_pass,
            "VerifyPass": new_pass
        }
        response = self.client.post(reverse('CambiarPass'), data)
        self.assertEqual(response.json()["status"], "ok")
        
        # Verificar que la contraseña cambió realmente
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password(new_pass))

    def test_cambiar_pass_actual_incorrecta(self):
        """Error si la contraseña 'vieja' no coincide."""
        data = {
            "OldPass": "PasswordErronea123",
            "NewPass": "NewPass123!",
            "VerifyPass": "NewPass123!"
        }
        response = self.client.post(reverse('CambiarPass'), data)
        self.assertEqual(response.json()["status"], "error")
        self.assertEqual(response.json()["message"], "La contraseña actual es incorrecta")

    def test_cambiar_pass_no_coinciden(self):
        """Error si la nueva contraseña y su confirmación son distintas."""
        data = {
            "OldPass": self.user_pass,
            "NewPass": "NewPass123!",
            "VerifyPass": "Diferente123!"
        }
        response = self.client.post(reverse('CambiarPass'), data)
        self.assertEqual(response.json()["status"], "error")
        self.assertEqual(response.json()["message"], "Las contraseñas no coinciden")

    def test_cambiar_pass_validacion_django(self):
        """Prueba que las validaciones de seguridad de Django (longitud, etc.) actúen."""
        data = {
            "OldPass": self.user_pass,
            "NewPass": "123", # Demasiado corta/simple
            "VerifyPass": "123"
        }
        response = self.client.post(reverse('CambiarPass'), data)
        self.assertEqual(response.json()["status"], "error")
        # El mensaje vendrá de los validadores de Django configurados en settings.py

#endregion MiPerfilTests





