# Application/signals.py

from django.db import transaction
from django.contrib.auth.hashers import make_password
from .models import Cargo, AreaMesa, Mesa, Platillo, TipoPlatillo

def initial_data(sender, **kwargs):
    with transaction.atomic():
        print("Insertando datos iniciales")
        
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
            {"Id": 3, "Nombre": "Cabaña de borde", "EsActivo": "1"},
            {"Id": 4, "Nombre": "Mesas de arriba", "EsActivo": "1"},
            {"Id": 5, "Nombre": "Cabaña piso rojo", "EsActivo": "1"},
            {"Id": 6, "Nombre": "Salón de eventos", "EsActivo": "0"},
        ]
        
        for data in areas:
            AreaMesa.objects.update_or_create(Id=data["Id"], defaults=data)
            
        # Mesas
        mesas = [
            # Salón principal
            {"Id": 1, "IdAreaMesa": AreaMesa.objects.get(Id=1), "Numero": 1, "Capacidad": None, "Estado": "1", "EsActivo": "1"},
            {"Id": 2, "IdAreaMesa": AreaMesa.objects.get(Id=1), "Numero": 2, "Capacidad": None, "Estado": "1", "EsActivo": "1"},
            {"Id": 3, "IdAreaMesa": AreaMesa.objects.get(Id=1), "Numero": 3, "Capacidad": None, "Estado": "1", "EsActivo": "1"},
            {"Id": 4, "IdAreaMesa": AreaMesa.objects.get(Id=1), "Numero": 4, "Capacidad": None, "Estado": "1", "EsActivo": "1"},
            {"Id": 5, "IdAreaMesa": AreaMesa.objects.get(Id=1), "Numero": 5, "Capacidad": None, "Estado": "1", "EsActivo": "1"},
            {"Id": 6, "IdAreaMesa": AreaMesa.objects.get(Id=1), "Numero": 6, "Capacidad": None, "Estado": "1", "EsActivo": "1"},
            {"Id": 7, "IdAreaMesa": AreaMesa.objects.get(Id=1), "Numero": 7, "Capacidad": None, "Estado": "1", "EsActivo": "1"},
            {"Id": 8, "IdAreaMesa": AreaMesa.objects.get(Id=1), "Numero": 8, "Capacidad": None, "Estado": "1", "EsActivo": "1"},
            
            # Cabañita
            {"Id": 9, "IdAreaMesa": AreaMesa.objects.get(Id=2), "Numero": 9, "Capacidad": None, "Estado": "1", "EsActivo": "1"},
            {"Id": 10, "IdAreaMesa": AreaMesa.objects.get(Id=2), "Numero": 10, "Capacidad": None, "Estado": "1", "EsActivo": "1"},
            {"Id": 11, "IdAreaMesa": AreaMesa.objects.get(Id=2), "Numero": 11, "Capacidad": None, "Estado": "1", "EsActivo": "1"},
            
            # Cabaña de borde
            {"Id": 12, "IdAreaMesa": AreaMesa.objects.get(Id=3), "Numero": 12, "Capacidad": None, "Estado": "1", "EsActivo": "1"},
            {"Id": 13, "IdAreaMesa": AreaMesa.objects.get(Id=3), "Numero": 13, "Capacidad": None, "Estado": "1", "EsActivo": "1"},
            {"Id": 14, "IdAreaMesa": AreaMesa.objects.get(Id=3), "Numero": 14, "Capacidad": None, "Estado": "1", "EsActivo": "1"},
            {"Id": 15, "IdAreaMesa": AreaMesa.objects.get(Id=3), "Numero": 15, "Capacidad": None, "Estado": "1", "EsActivo": "1"},
            
            # Mesas de arriba
            {"Id": 16, "IdAreaMesa": AreaMesa.objects.get(Id=4), "Numero": 16, "Capacidad": None, "Estado": "1", "EsActivo": "1"},
            {"Id": 17, "IdAreaMesa": AreaMesa.objects.get(Id=4), "Numero": 17, "Capacidad": None, "Estado": "1", "EsActivo": "1"},
            {"Id": 18, "IdAreaMesa": AreaMesa.objects.get(Id=4), "Numero": 18, "Capacidad": None, "Estado": "1", "EsActivo": "1"},
            {"Id": 19, "IdAreaMesa": AreaMesa.objects.get(Id=4), "Numero": 19, "Capacidad": None, "Estado": "1", "EsActivo": "1"},
            
            # Cabaña piso rojo
            {"Id": 20, "IdAreaMesa": AreaMesa.objects.get(Id=5), "Numero": 20, "Capacidad": None, "Estado": "1", "EsActivo": "1"},
            {"Id": 21, "IdAreaMesa": AreaMesa.objects.get(Id=5), "Numero": 21, "Capacidad": None, "Estado": "1", "EsActivo": "1"},
            {"Id": 22, "IdAreaMesa": AreaMesa.objects.get(Id=5), "Numero": 22, "Capacidad": None, "Estado": "1", "EsActivo": "1"},
            {"Id": 23, "IdAreaMesa": AreaMesa.objects.get(Id=5), "Numero": 23, "Capacidad": None, "Estado": "1", "EsActivo": "1"},
        ]
        
        for mesa in mesas:
            Mesa.objects.update_or_create(Id=mesa["Id"], defaults=mesa)

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
            
        # TODO: Agregar instancia al IdTipoPlatillo
        platillos = [
            #region 1 - Entradas
            {"Id": 1, "IdTipoPlatillo": TipoPlatillo.objects.get(Id=1), "Nombre": "Cocktail de camarones", "Precio": 250, "Descripcion": "", "ImagenUrl": None, "EsActivo": "1"},
            {"Id": 2, "IdTipoPlatillo": TipoPlatillo.objects.get(Id=1), "Nombre": "Sopa de mariscos", "Precio": 250, "Descripcion": "", "ImagenUrl": None, "EsActivo": "1"},
            {"Id": 3, "IdTipoPlatillo": TipoPlatillo.objects.get(Id=1), "Nombre": "Ensalada de vegetales con dados de queso", "Precio": 200, "Descripcion": "", "ImagenUrl": None, "EsActivo": "1"},
            {"Id": 4, "IdTipoPlatillo": TipoPlatillo.objects.get(Id=1), "Nombre": "Ceviche de pescado", "Precio": 200, "Descripcion": "", "ImagenUrl": None, "EsActivo": "1"},
            {"Id": 5, "IdTipoPlatillo": TipoPlatillo.objects.get(Id=1), "Nombre": "Tajadas de maduro y dados de queso", "Precio": 140, "Descripcion": "", "ImagenUrl": None, "EsActivo": "1"},
            {"Id": 6, "IdTipoPlatillo": TipoPlatillo.objects.get(Id=1), "Nombre": "Tajadas de plátano verde y dados de queso", "Precio": 150, "Descripcion": "", "ImagenUrl": None, "EsActivo": "1"},
            {"Id": 7, "IdTipoPlatillo": TipoPlatillo.objects.get(Id=1), "Nombre": "Tostones y dados de queso", "Precio": 180, "Descripcion": "", "ImagenUrl": None, "EsActivo": "1"},
            {"Id": 8, "IdTipoPlatillo": TipoPlatillo.objects.get(Id=1), "Nombre": "Frijoles molidos con queso rayado", "Precio": 0, "Descripcion": "", "ImagenUrl": None, "EsActivo": "0"},
            #endregion 1 - Entradas
            #region 2 - Carnes
            {"Id": 9, "IdTipoPlatillo": TipoPlatillo.objects.get(Id=2), "Nombre": "Churrasco (con salsa chimichurri)", "Precio": 50, "Descripcion": "", "ImagenUrl": None, "EsActivo": "1"},
            {"Id": 10, "IdTipoPlatillo": TipoPlatillo.objects.get(Id=2), "Nombre": "Jalapeño (con salsa jalapeña)", "Precio": 450, "Descripcion": "", "ImagenUrl": None, "EsActivo": "1"},
            {"Id": 11, "IdTipoPlatillo": TipoPlatillo.objects.get(Id=2), "Nombre": "Filet Mignon", "Precio": 480, "Descripcion": "Acompañados con arroz, vegetales y papas fritas", "ImagenUrl": None, "EsActivo": "1"},
            {"Id": 12, "IdTipoPlatillo": TipoPlatillo.objects.get(Id=2), "Nombre": "Filete a la plancha", "Precio": 470, "Descripcion": "Acompañados de arroz, tajadas de maduro y papas fritas", "ImagenUrl": None, "EsActivo": "1"},
            {"Id": 13, "IdTipoPlatillo": TipoPlatillo.objects.get(Id=2), "Nombre": "Antojitos La Olla de Barro", "Precio": 400, "Descripcion": "Un combo típico que lleva: 2 brochetas de carne, frijoles molidos, tajaditas (verde y maduro), dados de queso frito y chorizo.", "ImagenUrl": None, "EsActivo": "1"},
            {"Id": 14, "IdTipoPlatillo": TipoPlatillo.objects.get(Id=2), "Nombre": "Lomo de costillas", "Precio": 560, "Descripcion": "Servido con arroz, frijoles molidos, tortilla y tajadas", "ImagenUrl": None, "EsActivo": "1"},
            {"Id": 15, "IdTipoPlatillo": TipoPlatillo.objects.get(Id=2), "Nombre": "New York", "Precio": 600, "Descripcion": "Servido con arroz, frijoles molidos, tortilla y tajadas", "ImagenUrl": None, "EsActivo": "1"},
            {"Id": 16, "IdTipoPlatillo": TipoPlatillo.objects.get(Id=2), "Nombre": "Tomahawk", "Precio": 1100, "Descripcion": "Servido con arroz, frijoles molidos, tortilla y tajadas", "ImagenUrl": None, "EsActivo": "1"},
            {"Id": 17, "IdTipoPlatillo": TipoPlatillo.objects.get(Id=2), "Nombre": "Lengua en salsa", "Precio": 350, "Descripcion": "Servido con arroz, frijoles molidos, tortilla y tajadas", "ImagenUrl": None, "EsActivo": "1"},
            {"Id": 18, "IdTipoPlatillo": TipoPlatillo.objects.get(Id=2), "Nombre": "Fajitas de carne", "Precio": 400, "Descripcion": "Un toque mexicano en nuestro menú, servidas con tortilla, ensalada criolla, frijoles molidos y pico de gallo", "ImagenUrl": None, "EsActivo": "1"},
            {"Id": 19, "IdTipoPlatillo": TipoPlatillo.objects.get(Id=2), "Nombre": "Carne asada a la nica", "Precio": 400, "Descripcion": "Gallopinto pinolero, tortillas, maduro, ensalada de repollo y pico de gallo", "ImagenUrl": None, "EsActivo": "1"},
            {"Id": 20, "IdTipoPlatillo": TipoPlatillo.objects.get(Id=2), "Nombre": "Parrilla mixta", "Precio": 460, "Descripcion": "Combo de res, pollo y cerdo. Acompañado de arroz, tortilla, tajaditas, ensalada criolla y pico de gallo", "ImagenUrl": None, "EsActivo": "1"},
            #endregion 2 - Carnes
            #region 3 - Cerdo
            {"Id": 21, "IdTipoPlatillo": TipoPlatillo.objects.get(Id=3), "Nombre": "Lomito asado", "Precio": 350, "Descripcion": "Acompañado de arroz, tortilla, maduro frito y pico de gallo", "ImagenUrl": None, "EsActivo": "1"},
            #endregion 3 - Cerdo
            #region 4 - Pollo
            {"Id": 22, "IdTipoPlatillo": TipoPlatillo.objects.get(Id=4), "Nombre": "Pollo al vino (1/2 pollo)", "Precio": 320, "Descripcion": "", "ImagenUrl": None, "EsActivo": "1"},
            {"Id": 23, "IdTipoPlatillo": TipoPlatillo.objects.get(Id=4), "Nombre": "Pollo empanizado (1/2 pollo)", "Precio": 320, "Descripcion": "", "ImagenUrl": None, "EsActivo": "1"},
            {"Id": 24, "IdTipoPlatillo": TipoPlatillo.objects.get(Id=4), "Nombre": "Fajitas de pollo", "Precio": 270, "Descripcion": "", "ImagenUrl": None, "EsActivo": "1"},
            {"Id": 25, "IdTipoPlatillo": TipoPlatillo.objects.get(Id=4), "Nombre": "Dedos de pollo", "Precio": 280, "Descripcion": "", "ImagenUrl": None, "EsActivo": "1"},
            {"Id": 26, "IdTipoPlatillo": TipoPlatillo.objects.get(Id=4), "Nombre": "Filete a la plancha", "Precio": 380, "Descripcion": "Servido con salsa de su preferencia (hongo o jalapeña)", "ImagenUrl": None, "EsActivo": "1"},
            #endregion 4 - Pollo
            #region 5 - Para los niños
            {"Id": 27, "IdTipoPlatillo": TipoPlatillo.objects.get(Id=5), "Nombre": "Pollo al vino (1/4 pollo)", "Precio": 200, "Descripcion": "Incluye arroz y papas fritas", "ImagenUrl": None, "EsActivo": "1"},
            {"Id": 28, "IdTipoPlatillo": TipoPlatillo.objects.get(Id=5), "Nombre": "Pollo empanizado (1/4 pollo)", "Precio": 200, "Descripcion": "Incluye arroz y papas fritas", "ImagenUrl": None, "EsActivo": "1"},
            #endregion 5 - Para los niños
            #region 6 - Postres
            {"Id": 29, "IdTipoPlatillo": TipoPlatillo.objects.get(Id=6), "Nombre": "Toronja en miel", "Precio": 85, "Descripcion": "", "ImagenUrl": None, "EsActivo": "1"},
            {"Id": 30, "IdTipoPlatillo": TipoPlatillo.objects.get(Id=6), "Nombre": "Tres leches", "Precio": 85, "Descripcion": "", "ImagenUrl": None, "EsActivo": "1"},
            #endregion 6 - Postres
            #region 7 - Extras 
            {"Id": 31, "IdTipoPlatillo": TipoPlatillo.objects.get(Id=7), "Nombre": "Arroz", "Precio": 25, "Descripcion": "", "ImagenUrl": None, "EsActivo": "1"},
            {"Id": 32, "IdTipoPlatillo": TipoPlatillo.objects.get(Id=7), "Nombre": "Cebollitas", "Precio": 35, "Descripcion": "", "ImagenUrl": None, "EsActivo": "1"},
            {"Id": 33, "IdTipoPlatillo": TipoPlatillo.objects.get(Id=7), "Nombre": "Galletas", "Precio": 12, "Descripcion": "", "ImagenUrl": None, "EsActivo": "1"},
            {"Id": 34, "IdTipoPlatillo": TipoPlatillo.objects.get(Id=7), "Nombre": "Gallo pinto", "Precio": 35, "Descripcion": "", "ImagenUrl": None, "EsActivo": "1"},
            {"Id": 35, "IdTipoPlatillo": TipoPlatillo.objects.get(Id=7), "Nombre": "Papas fritas", "Precio": 60, "Descripcion": "", "ImagenUrl": None, "EsActivo": "1"},
            {"Id": 36, "IdTipoPlatillo": TipoPlatillo.objects.get(Id=7), "Nombre": "Queso (6 dados)", "Precio": 90, "Descripcion": "", "ImagenUrl": None, "EsActivo": "1"},
            {"Id": 37, "IdTipoPlatillo": TipoPlatillo.objects.get(Id=7), "Nombre": "Tostones", "Precio": 90, "Descripcion": "", "ImagenUrl": None, "EsActivo": "1"},
            {"Id": 38, "IdTipoPlatillo": TipoPlatillo.objects.get(Id=7), "Nombre": "Puré de papas", "Precio": 65, "Descripcion": "", "ImagenUrl": None, "EsActivo": "1"},
            {"Id": 39, "IdTipoPlatillo": TipoPlatillo.objects.get(Id=7), "Nombre": "Pico de gallo", "Precio": 30, "Descripcion": "", "ImagenUrl": None, "EsActivo": "1"},
            #endregion 7 - Extras 
            #region 8 - Corvina
            {"Id": 40, "IdTipoPlatillo": TipoPlatillo.objects.get(Id=8), "Nombre": "Filete de corvina empanizado", "Precio": 360, "Descripcion": "Incluye una ensalada de entrada y son acompañados de arroz, vegetales y papas fritas", "ImagenUrl": None, "EsActivo": "1"},
            {"Id": 41, "IdTipoPlatillo": TipoPlatillo.objects.get(Id=8), "Nombre": "Filete de corvina al ajillo", "Precio": 360, "Descripcion": "Incluye una ensalada de entrada y son acompañados de arroz, vegetales y papas fritas", "ImagenUrl": None, "EsActivo": "1"},
            {"Id": 42, "IdTipoPlatillo": TipoPlatillo.objects.get(Id=8), "Nombre": "Churros de corvina empanizados", "Precio": 360, "Descripcion": "Incluye una ensalada de entrada y son acompañados de arroz, vegetales y papas fritas", "ImagenUrl": None, "EsActivo": "1"},
            #endregion 8 - Corvina
            #region 9 - Camarones
            {"Id": 43, "IdTipoPlatillo": TipoPlatillo.objects.get(Id=9), "Nombre": "Camarones empanizados", "Precio": 420, "Descripcion": "", "ImagenUrl": None, "EsActivo": "1"},
            {"Id": 44, "IdTipoPlatillo": TipoPlatillo.objects.get(Id=9), "Nombre": "Camarones al ajillo", "Precio": 420, "Descripcion": "", "ImagenUrl": None, "EsActivo": "1"},
            #endregion 9 - Camarones
            #region 10 - Cocktail
            {"Id": 45, "IdTipoPlatillo": TipoPlatillo.objects.get(Id=10), "Nombre": "Macúa", "Precio": 150, "Descripcion": "Cóctel nicaragüense elaborado con ron blanco", "ImagenUrl": None, "EsActivo": "1"},
            #endregion 10 - Cocktail
            #region 11 - Cafe
            {"Id": 46, "IdTipoPlatillo": TipoPlatillo.objects.get(Id=11), "Nombre": "Café clásico", "Precio": 45, "Descripcion": "", "ImagenUrl": None, "EsActivo": "1"},
            {"Id": 47, "IdTipoPlatillo": TipoPlatillo.objects.get(Id=11), "Nombre": "Cappuccino", "Precio": 60, "Descripcion": "", "ImagenUrl": None, "EsActivo": "1"},
            #endregion 11 - Cafe
            #region 12 - Bebidas
            {"Id": 48, "IdTipoPlatillo": TipoPlatillo.objects.get(Id=12), "Nombre": "Té frío (limón o jamaica)", "Precio": 50, "Descripcion": "", "ImagenUrl": None, "EsActivo": "1"},
            {"Id": 49, "IdTipoPlatillo": TipoPlatillo.objects.get(Id=12), "Nombre": "Gaseosa 12 onz", "Precio": 40, "Descripcion": "", "ImagenUrl": None, "EsActivo": "1"},
            {"Id": 50, "IdTipoPlatillo": TipoPlatillo.objects.get(Id=12), "Nombre": "Coca cola zero lata", "Precio": 55, "Descripcion": "", "ImagenUrl": None, "EsActivo": "1"},
            {"Id": 51, "IdTipoPlatillo": TipoPlatillo.objects.get(Id=12), "Nombre": "Cacao", "Precio": 55, "Descripcion": "", "ImagenUrl": None, "EsActivo": "1"},
            {"Id": 52, "IdTipoPlatillo": TipoPlatillo.objects.get(Id=12), "Nombre": "Fruit punch", "Precio": 50, "Descripcion": "", "ImagenUrl": None, "EsActivo": "1"},
            {"Id": 53, "IdTipoPlatillo": TipoPlatillo.objects.get(Id=12), "Nombre": "Jugo de naranja", "Precio": 50, "Descripcion": "", "ImagenUrl": None, "EsActivo": "1"},
            {"Id": 54, "IdTipoPlatillo": TipoPlatillo.objects.get(Id=12), "Nombre": "Agua Fuente Pura 600 ml", "Precio": 30, "Descripcion": "", "ImagenUrl": None, "EsActivo": "1"},
            #endregion 12 - Bebidas
            #region 13 - Cervezas
            {"Id": 55, "IdTipoPlatillo": TipoPlatillo.objects.get(Id=13), "Nombre": "Victoria Frost", "Precio": 50, "Descripcion": "", "ImagenUrl": None, "EsActivo": "1"},
            {"Id": 56, "IdTipoPlatillo": TipoPlatillo.objects.get(Id=13), "Nombre": "Victoria Clásica", "Precio": 55, "Descripcion": "", "ImagenUrl": None, "EsActivo": "1"},
            {"Id": 57, "IdTipoPlatillo": TipoPlatillo.objects.get(Id=13), "Nombre": "Toña", "Precio": 55, "Descripcion": "", "ImagenUrl": None, "EsActivo": "1"},
            {"Id": 58, "IdTipoPlatillo": TipoPlatillo.objects.get(Id=13), "Nombre": "Toña Light", "Precio": 55, "Descripcion": "", "ImagenUrl": None, "EsActivo": "1"},
            {"Id": 59, "IdTipoPlatillo": TipoPlatillo.objects.get(Id=13), "Nombre": "Miller Lite", "Precio": 65, "Descripcion": "", "ImagenUrl": None, "EsActivo": "1"},
            {"Id": 60, "IdTipoPlatillo": TipoPlatillo.objects.get(Id=13), "Nombre": "Heineken", "Precio": 85, "Descripcion": "", "ImagenUrl": None, "EsActivo": "1"},
            {"Id": 61, "IdTipoPlatillo": TipoPlatillo.objects.get(Id=13), "Nombre": "Sol", "Precio": 75, "Descripcion": "", "ImagenUrl": None, "EsActivo": "1"},
            {"Id": 62, "IdTipoPlatillo": TipoPlatillo.objects.get(Id=13), "Nombre": "Corona", "Precio": 90, "Descripcion": "", "ImagenUrl": None, "EsActivo": "1"},
            {"Id": 63, "IdTipoPlatillo": TipoPlatillo.objects.get(Id=13), "Nombre": "Smirnoff Ice", "Precio": 85, "Descripcion": "Red, Rapsberry, Green Apple", "ImagenUrl": None, "EsActivo": "1"},
            {"Id": 64, "IdTipoPlatillo": TipoPlatillo.objects.get(Id=13), "Nombre": "Bliss frutas mixtas", "Precio": 74, "Descripcion": "", "ImagenUrl": None, "EsActivo": "1"},
            {"Id": 65, "IdTipoPlatillo": TipoPlatillo.objects.get(Id=13), "Nombre": "Bamboo", "Precio": 60, "Descripcion": "Daiquirí fresa y mojito", "ImagenUrl": None, "EsActivo": "1"},
            {"Id": 66, "IdTipoPlatillo": TipoPlatillo.objects.get(Id=13), "Nombre": "Spark", "Precio": 60, "Descripcion": "Mandarina, Limón hierbabuena, Rapsberry, Manzana verde", "ImagenUrl": None, "EsActivo": "1"},
            {"Id": 67, "IdTipoPlatillo": TipoPlatillo.objects.get(Id=13), "Nombre": "Adán & Eva", "Precio": 60, "Descripcion": "Frutos rojos, Limón jengibre, Coco limón, Maracuyá & piña con Ron, Durazno Rosé con Vodka", "ImagenUrl": None, "EsActivo": "1"},
            #endregion 13 - Cervezas
            #region 14 - Flor de caña
            {"Id": 68, "IdTipoPlatillo": TipoPlatillo.objects.get(Id=14), "Nombre": "Ultra lite (shot)", "Precio": 50, "Descripcion": "", "ImagenUrl": None, "EsActivo": "1"},
            {"Id": 69, "IdTipoPlatillo": TipoPlatillo.objects.get(Id=14), "Nombre": "Ultra lite (1/4)", "Precio": 170, "Descripcion": "", "ImagenUrl": None, "EsActivo": "1"},
            {"Id": 70, "IdTipoPlatillo": TipoPlatillo.objects.get(Id=14), "Nombre": "Ultra lite (1/2)", "Precio": 320, "Descripcion": "", "ImagenUrl": None, "EsActivo": "1"},
            {"Id": 71, "IdTipoPlatillo": TipoPlatillo.objects.get(Id=14), "Nombre": "Extra lite (shot)", "Precio": 50, "Descripcion": "", "ImagenUrl": None, "EsActivo": "1"},
            {"Id": 72, "IdTipoPlatillo": TipoPlatillo.objects.get(Id=14), "Nombre": "Extra lite (1/4)", "Precio": 190, "Descripcion": "", "ImagenUrl": None, "EsActivo": "1"},
            {"Id": 73, "IdTipoPlatillo": TipoPlatillo.objects.get(Id=14), "Nombre": "Extra lite (1/2)", "Precio": 360, "Descripcion": "", "ImagenUrl": None, "EsActivo": "1"},
            {"Id": 74, "IdTipoPlatillo": TipoPlatillo.objects.get(Id=14), "Nombre": "Gran reserva (shot)", "Precio": 65, "Descripcion": "", "ImagenUrl": None, "EsActivo": "1"},
            {"Id": 75, "IdTipoPlatillo": TipoPlatillo.objects.get(Id=14), "Nombre": "Gran reserva (1/4)", "Precio": 240, "Descripcion": "", "ImagenUrl": None, "EsActivo": "1"},
            {"Id": 76, "IdTipoPlatillo": TipoPlatillo.objects.get(Id=14), "Nombre": "Gran reserva (1/2)", "Precio": 450, "Descripcion": "", "ImagenUrl": None, "EsActivo": "1"},
            {"Id": 77, "IdTipoPlatillo": TipoPlatillo.objects.get(Id=14), "Nombre": "Centenario 12 (shot)", "Precio": 80, "Descripcion": "", "ImagenUrl": None, "EsActivo": "1"},
            {"Id": 78, "IdTipoPlatillo": TipoPlatillo.objects.get(Id=14), "Nombre": "Centenario 12 (1/4)", "Precio": 440, "Descripcion": "", "ImagenUrl": None, "EsActivo": "1"},
            {"Id": 79, "IdTipoPlatillo": TipoPlatillo.objects.get(Id=14), "Nombre": "Centenario 12 (1/2)", "Precio": 850, "Descripcion": "", "ImagenUrl": None, "EsActivo": "1"},
            #endregion 14 - Flor de caña
            #region 15 - Licores importados
            {"Id": 80, "IdTipoPlatillo": TipoPlatillo.objects.get(Id=15), "Nombre": "Whisky Chivas regal (shot)", "Precio": 140, "Descripcion": "", "ImagenUrl": None, "EsActivo": "1"},
            {"Id": 81, "IdTipoPlatillo": TipoPlatillo.objects.get(Id=15), "Nombre": "Whisky Chivas regal (1/2)", "Precio": 1700, "Descripcion": "", "ImagenUrl": None, "EsActivo": "1"},
            {"Id": 82, "IdTipoPlatillo": TipoPlatillo.objects.get(Id=15), "Nombre": "Whisky Johnnie Wal. Red label (shot)", "Precio": 140, "Descripcion": "", "ImagenUrl": None, "EsActivo": "1"},
            {"Id": 83, "IdTipoPlatillo": TipoPlatillo.objects.get(Id=15), "Nombre": "Whisky Johnnie Wal. Red label (1/2)", "Precio": 1200, "Descripcion": "", "ImagenUrl": None, "EsActivo": "1"},
            {"Id": 84, "IdTipoPlatillo": TipoPlatillo.objects.get(Id=15), "Nombre": "Whisky Johnnie Wal. Black label (shot)", "Precio": 145, "Descripcion": "", "ImagenUrl": None, "EsActivo": "1"},
            {"Id": 85, "IdTipoPlatillo": TipoPlatillo.objects.get(Id=15), "Nombre": "Whisky Johnnie Wal. Black label (1/2)", "Precio": 1500, "Descripcion": "", "ImagenUrl": None, "EsActivo": "1"},
            {"Id": 86, "IdTipoPlatillo": TipoPlatillo.objects.get(Id=15), "Nombre": "Vodka Finlandia (shot)", "Precio": 60, "Descripcion": "", "ImagenUrl": None, "EsActivo": "1"},
            {"Id": 87, "IdTipoPlatillo": TipoPlatillo.objects.get(Id=15), "Nombre": "Vodka Finlandia (1/2)", "Precio": 750, "Descripcion": "", "ImagenUrl": None, "EsActivo": "1"},
            #endregion 15 - Licores importados
        ]
        
        for platillo in platillos:
            Platillo.objects.update_or_create(Id=platillo["Id"], defaults=platillo)

