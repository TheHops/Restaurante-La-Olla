# Application/signals.py

from django.db import transaction
from django.contrib.auth.hashers import make_password
from .models import Cargo, AreaMesa, TipoPlatillo, Usuario

def initial_data(sender, **kwargs):
    with transaction.atomic():
        # Cargos
        cargos = [
            {"Id": 1, "Nombre": "Administrador", "EsActivo": "1"},
            {"Id": 2, "Nombre": "Mesero", "EsActivo": "1"},
            {"Id": 3, "Nombre": "Cocinero", "EsActivo": "1"},
            {"Id": 4, "Nombre": "Cajero", "EsActivo": "1"},
        ]
        
        for data in cargos:
            Cargo.objects.update_or_create(Id=data["Id"], defaults=data)

        # Áreas de mesa
        areas = [
            {"Id": 1, "Nombre": "Salón principal", "EsActivo": "1"},
            {"Id": 2, "Nombre": "Cabañita", "EsActivo": "1"},
            {"Id": 3, "Nombre": "Cabaña de arriba", "EsActivo": "1"},
            {"Id": 4, "Nombre": "Mesas de borde", "EsActivo": "1"},
            {"Id": 5, "Nombre": "Cabaña piso rojo", "EsActivo": "1"},
            {"Id": 6, "Nombre": "Salón de eventos", "EsActivo": "0"},
        ]
        
        for data in areas:
            AreaMesa.objects.update_or_create(Id=data["Id"], defaults=data)
            
        # Mesas
        mesas = [
            # Salón principal
            {"Id": 1, "IdAreaMesa": 1, "Numero": 1, "Capacidad": None, "Estado": "1", "EsActivo": "1"},
            {"Id": 2, "IdAreaMesa": 1, "Numero": 2, "Capacidad": None, "Estado": "1", "EsActivo": "1"},
            {"Id": 3, "IdAreaMesa": 1, "Numero": 3, "Capacidad": None, "Estado": "1", "EsActivo": "1"},
            {"Id": 4, "IdAreaMesa": 1, "Numero": 4, "Capacidad": None, "Estado": "1", "EsActivo": "1"},
            {"Id": 5, "IdAreaMesa": 1, "Numero": 5, "Capacidad": None, "Estado": "1", "EsActivo": "1"},
            {"Id": 6, "IdAreaMesa": 1, "Numero": 6, "Capacidad": None, "Estado": "1", "EsActivo": "1"},
            {"Id": 7, "IdAreaMesa": 1, "Numero": 7, "Capacidad": None, "Estado": "1", "EsActivo": "1"},
            {"Id": 8, "IdAreaMesa": 1, "Numero": 8, "Capacidad": None, "Estado": "1", "EsActivo": "1"},
            
            # Cabañita
            {"Id": 9, "IdAreaMesa": 2, "Numero": 1, "Capacidad": None, "Estado": "1", "EsActivo": "1"},
            {"Id": 10, "IdAreaMesa": 2, "Numero": 2, "Capacidad": None, "Estado": "1", "EsActivo": "1"},
            {"Id": 11, "IdAreaMesa": 2, "Numero": 3, "Capacidad": None, "Estado": "1", "EsActivo": "1"},
            
            # Cabaña de arriba
            {"Id": 12, "IdAreaMesa": 3, "Numero": 1, "Capacidad": None, "Estado": "1", "EsActivo": "1"},
            {"Id": 13, "IdAreaMesa": 3, "Numero": 2, "Capacidad": None, "Estado": "1", "EsActivo": "1"},
            {"Id": 14, "IdAreaMesa": 3, "Numero": 3, "Capacidad": None, "Estado": "1", "EsActivo": "1"},
            {"Id": 15, "IdAreaMesa": 3, "Numero": 4, "Capacidad": None, "Estado": "1", "EsActivo": "1"},
            
            # Mesas de borde
            {"Id": 16, "IdAreaMesa": 4, "Numero": 1, "Capacidad": None, "Estado": "1", "EsActivo": "1"},
            {"Id": 17, "IdAreaMesa": 4, "Numero": 2, "Capacidad": None, "Estado": "1", "EsActivo": "1"},
            {"Id": 18, "IdAreaMesa": 4, "Numero": 3, "Capacidad": None, "Estado": "1", "EsActivo": "1"},
            {"Id": 19, "IdAreaMesa": 4, "Numero": 4, "Capacidad": None, "Estado": "1", "EsActivo": "1"},
            
            # Cabaña piso rojo
            {"Id": 20, "IdAreaMesa": 5, "Numero": 1, "Capacidad": None, "Estado": "1", "EsActivo": "1"},
            {"Id": 21, "IdAreaMesa": 5, "Numero": 2, "Capacidad": None, "Estado": "1", "EsActivo": "1"},
            {"Id": 22, "IdAreaMesa": 5, "Numero": 3, "Capacidad": None, "Estado": "1", "EsActivo": "1"},
            {"Id": 23, "IdAreaMesa": 5, "Numero": 4, "Capacidad": None, "Estado": "1", "EsActivo": "1"},
        ]

        # Tipos de platillo
        tipos = [
            {"Id": 1, "Nombre": "Entradas", "EsActivo": "1"},
            {"Id": 2, "Nombre": "Carnes", "EsActivo": "1"},
            {"Id": 3, "Nombre": "Cerdo", "EsActivo": "1"},
            {"Id": 4, "Nombre": "Pollo", "EsActivo": "1"},
            {"Id": 5, "Nombre": "Para los niños", "EsActivo": "1"},
            {"Id": 6, "Nombre": "Postres", "EsActivo": "1"},
            {"Id": 7, "Nombre": "Extras", "EsActivo": "1"},
            {"Id": 8, "Nombre": "Corvina", "EsActivo": "1"},
            {"Id": 9, "Nombre": "Camarones", "EsActivo": "1"},
            {"Id": 10, "Nombre": "Cocktail", "EsActivo": "1"},
            {"Id": 11, "Nombre": "Cafe", "EsActivo": "1"},
            {"Id": 12, "Nombre": "Bebidas", "EsActivo": "1"},
            {"Id": 13, "Nombre": "Cervezas", "EsActivo": "1"},
            {"Id": 14, "Nombre": "Flor de caña", "EsActivo": "1"},
            {"Id": 15, "Nombre": "Licores importados", "EsActivo": "1"}
        ]
        
        for data in tipos:
            TipoPlatillo.objects.update_or_create(Id=data["Id"], defaults=data)
            
        platillos = [
            #region 1 - Entradas
            {"Id": 1, "IdTipoPlatillo": 1, "Nombre": "Cocktail de camarones", "Precio": 250, "Descripcion": "", "ImagenUrl": None, "EsActivo": "1"},
            {"Id": 2, "IdTipoPlatillo": 1, "Nombre": "Sopa de mariscos", "Precio": 250, "Descripcion": "", "ImagenUrl": None, "EsActivo": "1"},
            {"Id": 3, "IdTipoPlatillo": 1, "Nombre": "Ensalada de vegetales con dados de queso", "Precio": 200, "Descripcion": "", "ImagenUrl": None, "EsActivo": "1"},
            {"Id": 4, "IdTipoPlatillo": 1, "Nombre": "Ceviche de pescado", "Precio": 200, "Descripcion": "", "ImagenUrl": None, "EsActivo": "1"},
            {"Id": 5, "IdTipoPlatillo": 1, "Nombre": "Tajadas de maduro y dados de queso", "Precio": 140, "Descripcion": "", "ImagenUrl": None, "EsActivo": "1"},
            {"Id": 6, "IdTipoPlatillo": 1, "Nombre": "Tajadas de plátano verde y dados de queso", "Precio": 150, "Descripcion": "", "ImagenUrl": None, "EsActivo": "1"},
            {"Id": 7, "IdTipoPlatillo": 1, "Nombre": "Tostones y dados de queso", "Precio": 180, "Descripcion": "", "ImagenUrl": None, "EsActivo": "1"},
            {"Id": 8, "IdTipoPlatillo": 1, "Nombre": "Frijoles molidos con queso rayado", "Precio": 0, "Descripcion": "", "ImagenUrl": None, "EsActivo": "0"},
            #endregion 1 - Entradas
            #region 2 - Carnes
            {"Id": 9, "IdTipoPlatillo": 2, "Nombre": "Churrasco (con salsa chimichurri)", "Precio": 450, "Descripcion": "", "ImagenUrl": None, "EsActivo": "1"},
            {"Id": 10, "IdTipoPlatillo": 2, "Nombre": "Jalapeño (con salsa jalapeña)", "Precio": 450, "Descripcion": "", "ImagenUrl": None, "EsActivo": "1"},
            {"Id": 11, "IdTipoPlatillo": 2, "Nombre": "Filet Mignon", "Precio": 480, "Descripcion": "Acompañados con arroz, vegetales y papas fritas", "ImagenUrl": None, "EsActivo": "1"},
            {"Id": 12, "IdTipoPlatillo": 2, "Nombre": "Filete a la plancha", "Precio": 470, "Descripcion": "Acompañados de arroz, tajadas de maduro y papas fritas", "ImagenUrl": None, "EsActivo": "1"},
            {"Id": 13, "IdTipoPlatillo": 2, "Nombre": "Antojitos La Olla de Barro", "Precio": 400, "Descripcion": "Un combo típico que lleva: 2 brochetas de carne, frijoles molidos, tajaditas (verde y maduro), dados de queso frito y chorizo.", "ImagenUrl": None, "EsActivo": "1"},
            {"Id": 14, "IdTipoPlatillo": 2, "Nombre": "Lomo de costillas", "Precio": 560, "Descripcion": "Servido con arroz, frijoles molidos, tortilla y tajadas", "ImagenUrl": None, "EsActivo": "1"},
            {"Id": 15, "IdTipoPlatillo": 2, "Nombre": "New York", "Precio": 600, "Descripcion": "Servido con arroz, frijoles molidos, tortilla y tajadas", "ImagenUrl": None, "EsActivo": "1"},
            {"Id": 16, "IdTipoPlatillo": 2, "Nombre": "Tomahawk", "Precio": 1100, "Descripcion": "Servido con arroz, frijoles molidos, tortilla y tajadas", "ImagenUrl": None, "EsActivo": "1"},
            {"Id": 17, "IdTipoPlatillo": 2, "Nombre": "Lengua en salsa", "Precio": 350, "Descripcion": "Servido con arroz, frijoles molidos, tortilla y tajadas", "ImagenUrl": None, "EsActivo": "1"},
            {"Id": 18, "IdTipoPlatillo": 2, "Nombre": "Fajitas de carne", "Precio": 400, "Descripcion": "Un toque mexicano en nuestro menú, servidas con tortilla, ensalada criolla, frijoles molidos y pico de gallo", "ImagenUrl": None, "EsActivo": "1"},
            {"Id": 19, "IdTipoPlatillo": 2, "Nombre": "Carne asada a la nica", "Precio": 400, "Descripcion": "Gallopinto pinolero, tortillas, maduro, ensalada de repollo y pico de gallo", "ImagenUrl": None, "EsActivo": "1"},
            {"Id": 20, "IdTipoPlatillo": 2, "Nombre": "Parrilla mixta", "Precio": 460, "Descripcion": "Combo de res, pollo y cerdo. Acompañado de arroz, tortilla, tajaditas, ensalada criolla y pico de gallo", "ImagenUrl": None, "EsActivo": "1"},
            #endregion 2 - Carnes
            #region 3 - Cerdo
            {"Id": 21, "IdTipoPlatillo": 3, "Nombre": "Lomito asado", "Precio": 350, "Descripcion": "Acompañado de arroz, tortilla, maduro frito y pico de gallo", "ImagenUrl": None, "EsActivo": "1"},
            #endregion 3 - Cerdo
            #region 4 - Pollo
            {"Id": 22, "IdTipoPlatillo": 4, "Nombre": "Pollo al vino (1/2 pollo)", "Precio": 320, "Descripcion": "", "ImagenUrl": None, "EsActivo": "1"},
            {"Id": 23, "IdTipoPlatillo": 4, "Nombre": "Pollo empanizado (1/2 pollo)", "Precio": 320, "Descripcion": "", "ImagenUrl": None, "EsActivo": "1"},
            {"Id": 24, "IdTipoPlatillo": 4, "Nombre": "Fajitas de pollo", "Precio": 270, "Descripcion": "", "ImagenUrl": None, "EsActivo": "1"},
            {"Id": 25, "IdTipoPlatillo": 4, "Nombre": "Dedos de pollo", "Precio": 280, "Descripcion": "", "ImagenUrl": None, "EsActivo": "1"},
            {"Id": 26, "IdTipoPlatillo": 4, "Nombre": "Filete a la plancha", "Precio": 380, "Descripcion": "Servido con salsa de su preferencia (hongo o jalapeña)", "ImagenUrl": None, "EsActivo": "1"},
            #endregion 4 - Pollo
            #region 5 - Para los niños
            {"Id": 27, "IdTipoPlatillo": 5, "Nombre": "Pollo al vino (1/4 pollo)", "Precio": 200, "Descripcion": "Incluye arroz y papas fritas", "ImagenUrl": None, "EsActivo": "1"},
            {"Id": 28, "IdTipoPlatillo": 5, "Nombre": "Pollo empanizado (1/4 pollo)", "Precio": 200, "Descripcion": "Incluye arroz y papas fritas", "ImagenUrl": None, "EsActivo": "1"},
            #endregion 5 - Para los niños
            #region 6 - Postres
            {"Id": 29, "IdTipoPlatillo": 6, "Nombre": "Toronja en miel", "Precio": 85, "Descripcion": "", "ImagenUrl": None, "EsActivo": "1"},
            {"Id": 30, "IdTipoPlatillo": 6, "Nombre": "Tres leches", "Precio": 85, "Descripcion": "", "ImagenUrl": None, "EsActivo": "1"},
            #endregion 6 - Postres
            #region 7 - Extras 
            {"Id": 31, "IdTipoPlatillo": 7, "Nombre": "Arroz", "Precio": 25, "Descripcion": "", "ImagenUrl": None, "EsActivo": "1"},
            {"Id": 32, "IdTipoPlatillo": 7, "Nombre": "Cebollitas", "Precio": 35, "Descripcion": "", "ImagenUrl": None, "EsActivo": "1"},
            {"Id": 33, "IdTipoPlatillo": 7, "Nombre": "Galletas", "Precio": 12, "Descripcion": "", "ImagenUrl": None, "EsActivo": "1"},
            {"Id": 34, "IdTipoPlatillo": 7, "Nombre": "Gallo pinto", "Precio": 35, "Descripcion": "", "ImagenUrl": None, "EsActivo": "1"},
            {"Id": 35, "IdTipoPlatillo": 7, "Nombre": "Papas fritas", "Precio": 60, "Descripcion": "", "ImagenUrl": None, "EsActivo": "1"},
            {"Id": 36, "IdTipoPlatillo": 7, "Nombre": "Queso (6 dados)", "Precio": 90, "Descripcion": "", "ImagenUrl": None, "EsActivo": "1"},
            {"Id": 37, "IdTipoPlatillo": 7, "Nombre": "Tostones", "Precio": 90, "Descripcion": "", "ImagenUrl": None, "EsActivo": "1"},
            {"Id": 38, "IdTipoPlatillo": 7, "Nombre": "Puré de papas", "Precio": 65, "Descripcion": "", "ImagenUrl": None, "EsActivo": "1"},
            {"Id": 39, "IdTipoPlatillo": 7, "Nombre": "Pico de gallo", "Precio": 30, "Descripcion": "", "ImagenUrl": None, "EsActivo": "1"},
            #endregion 7 - Extras 
            #region 8 - Corvina
            {"Id": 40, "IdTipoPlatillo": 8, "Nombre": "Filete de corvina empanizado", "Precio": 360, "Descripcion": "Incluye una ensalada de entrada y son acompañados de arroz, vegetales y papas fritas", "ImagenUrl": None, "EsActivo": "1"},
            {"Id": 41, "IdTipoPlatillo": 8, "Nombre": "Filete de corvina al ajillo", "Precio": 360, "Descripcion": "Incluye una ensalada de entrada y son acompañados de arroz, vegetales y papas fritas", "ImagenUrl": None, "EsActivo": "1"},
            {"Id": 42, "IdTipoPlatillo": 8, "Nombre": "Churros de corvina empanizados", "Precio": 360, "Descripcion": "Incluye una ensalada de entrada y son acompañados de arroz, vegetales y papas fritas", "ImagenUrl": None, "EsActivo": "1"},
            #endregion 8 - Corvina
            #region 9 - Camarones
            {"Id": 43, "IdTipoPlatillo": 9, "Nombre": "Camarones empanizados", "Precio": 420, "Descripcion": "", "ImagenUrl": None, "EsActivo": "1"},
            {"Id": 44, "IdTipoPlatillo": 9, "Nombre": "Camarones al ajillo", "Precio": 420, "Descripcion": "", "ImagenUrl": None, "EsActivo": "1"},
            #endregion 9 - Camarones
            #region 10 - Cocktail
            {"Id": 45, "IdTipoPlatillo": 10, "Nombre": "Macúa", "Precio": 150, "Descripcion": "Cóctel nicaragüense elaborado con ron blanco", "ImagenUrl": None, "EsActivo": "1"},
            #endregion 10 - Cocktail
            #region 11 - Cafe
            {"Id": 46, "IdTipoPlatillo": 11, "Nombre": "Café clásico", "Precio": 45, "Descripcion": "", "ImagenUrl": None, "EsActivo": "1"},
            {"Id": 47, "IdTipoPlatillo": 11, "Nombre": "Cappuccino", "Precio": 60, "Descripcion": "", "ImagenUrl": None, "EsActivo": "1"},
            #endregion 11 - Cafe
            #region 12 - Bebidas
            {"Id": 48, "IdTipoPlatillo": 12, "Nombre": "Té frío (limón o jamaica)", "Precio": 50, "Descripcion": "", "ImagenUrl": None, "EsActivo": "1"},
            {"Id": 49, "IdTipoPlatillo": 12, "Nombre": "Gaseosa 12 onz", "Precio": 40, "Descripcion": "", "ImagenUrl": None, "EsActivo": "1"},
            {"Id": 50, "IdTipoPlatillo": 12, "Nombre": "Coca cola zero lata", "Precio": 55, "Descripcion": "", "ImagenUrl": None, "EsActivo": "1"},
            {"Id": 51, "IdTipoPlatillo": 12, "Nombre": "Cacao", "Precio": 55, "Descripcion": "", "ImagenUrl": None, "EsActivo": "1"},
            {"Id": 52, "IdTipoPlatillo": 12, "Nombre": "Fruit punch", "Precio": 50, "Descripcion": "", "ImagenUrl": None, "EsActivo": "1"},
            {"Id": 53, "IdTipoPlatillo": 12, "Nombre": "Jugo de naranja", "Precio": 50, "Descripcion": "", "ImagenUrl": None, "EsActivo": "1"},
            {"Id": 54, "IdTipoPlatillo": 12, "Nombre": "Agua Fuente Pura 600 ml", "Precio": 30, "Descripcion": "", "ImagenUrl": None, "EsActivo": "1"},
            #endregion 12 - Bebidas
            # 13 - Cervezas
            # 14 - Flor de caña
            # 15 - Licores importados
        ]

