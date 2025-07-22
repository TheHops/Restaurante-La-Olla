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
        # areas = [
        #     {"Id": 1, "Nombre": "Interior", "EsActivo": "1"},
        #     {"Id": 2, "Nombre": "Terraza", "EsActivo": "1"},
        # ]
        # for data in areas:
        #     AreaMesa.objects.update_or_create(Id=data["Id"], defaults=data)

        # Tipos de platillo
        # tipos = [
        #     {"Id": 1, "Nombre": "Plato fuerte", "EsActivo": "1"},
        #     {"Id": 2, "Nombre": "Bebida", "EsActivo": "1"},
        #     {"Id": 3, "Nombre": "Postre", "EsActivo": "1"},
        # ]
        # for data in tipos:
        #     TipoPlatillo.objects.update_or_create(Id=data["Id"], defaults=data)

