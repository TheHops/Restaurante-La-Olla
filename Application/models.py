from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

#region Cargo

class Cargo(models.Model):
    Id = models.AutoField(primary_key=True, db_column='id_cargo')
    
    Nombre = models.CharField(db_column='nombre', max_length=20)

    # activo = models.TextField(db_column='Activo', blank=True, null=True)

    ESTADOS = [("1", "Activo"), ("0", "Eliminado")]
    EsActivo = models.CharField(max_length=10, choices=ESTADOS, default="1", db_column='es_activo')

    class Meta:
        verbose_name_plural = 'Cargo'
        db_table = 'cargo'

    def __str__(self):
        return f"ID = {self.Id} | Cargo = {self.Nombre}"
    
#endregion Cargo

#region Usuario

class Usuario(AbstractUser):
    Id = models.AutoField(primary_key=True, db_column='id_usuario')

    IdCargo = models.ForeignKey(Cargo, on_delete=models.SET_NULL, null=True, verbose_name="Cargo", db_column='id_cargo')

    Nombres = models.CharField(max_length=15, default="", db_column='nombres')
    
    Apellidos = models.CharField(max_length=15, default="", db_column='apellidos')
    
    Direccion = models.CharField(max_length=120, blank=True, null=True, default="", db_column='direccion')
    
    Telefono = models.CharField(max_length=20, blank=True, null=True, db_column='telefono')

    ESTADOS = [("1", "Activo"), ("0", "Inactivo")]
    EsActivo = models.CharField(max_length=1, choices=ESTADOS, default="1", db_column='es_activo')

    class Meta:
        verbose_name_plural = 'Usuario'
        db_table = 'usuario'

    def __str__(self):
        return f"ID = {self.Id} | UserName = {self.username} | Nombres = {self.Nombres} | Apellidos = {self.Apellidos} | EsActivo = {self.EsActivo}"

#endregion Usuario

#region AreaMesa

class AreaMesa(models.Model):
    Id = models.AutoField(primary_key=True, db_column='id_area_mesa')
    
    Nombre = models.CharField(db_column='nombre', max_length=20)

    # activo = models.TextField(db_column='Activo', blank=True, null=True)

    ESTADOS = [("1", "Activo"), ("0", "Eliminado")]
    EsActivo = models.CharField(max_length=10, choices=ESTADOS, default="1", db_column='es_activo')

    class Meta:
        verbose_name_plural = 'AreaMesa'
        db_table = 'area_mesa'

    def __str__(self):
        return f"ID = {self.Id} | Area de mesa = {self.Nombre}"
    
#endregion AreaMesa

#region Mesa

class Mesa(models.Model):
    Id = models.AutoField(primary_key=True, db_column='id_mesa')
    
    IdAreaMesa = models.ForeignKey(AreaMesa, models.DO_NOTHING, db_column='id_area_mesa')
    
    Numero = models.IntegerField(db_column='numero')
    
    Capacidad = models.IntegerField(db_column='capacidad', blank=True, null=True)

    ESTADOSMESA = [("1", "Disponible"), ("0", "Ocupado")]
    Estado = models.CharField(max_length=15, choices=ESTADOSMESA, blank=True, null=True, db_column='estado')

    # activo = models.TextField(db_column='Activo', blank=True, null=True)

    ESTADOS = [("1", "Activo"), ("0", "Eliminado")]
    EsActivo = models.CharField(max_length=10, choices=ESTADOS, default="1", db_column='es_activo')

    class Meta:
        verbose_name_plural = 'Mesa'
        db_table = 'mesa'

    def __str__(self):
        return f"ID = {self.Id} | Mesa = {self.Numero} | Area de mesa = {self.IdAreaMesa.Nombre} | Estado = {self.Estado}"

#endregion Mesa

#region Orden

class Orden(models.Model):
    Id = models.AutoField(primary_key=True)
    
    IdUsuario = models.ForeignKey(Usuario, models.DO_NOTHING, db_column='id_usuario')
    
    IdMesa = models.ForeignKey(Mesa, models.DO_NOTHING, db_column='id_mesa')
    
    Total = models.DecimalField(db_column='total', null=True, blank=True, default=0, max_digits=8, decimal_places=2)
    
    Monto = models.DecimalField(db_column='monto', null=True, blank=True, default=0, max_digits=8, decimal_places=2)
    
    Cambio = models.DecimalField(db_column='cambio', null=True, blank=True, default=0, max_digits=8, decimal_places=2)
    
    Propina = models.DecimalField(db_column='propina', null=True, blank=True, default=0, max_digits=8, decimal_places=2)
    
    Descuento = models.DecimalField(db_column='descuento', null=True, blank=True, default=0, max_digits=8, decimal_places=2)
    
    Fecha = models.DateTimeField(db_column='fecha', auto_now_add=True)
    
    METODOPAGO = [("1", "Efectivo"), ("2", "Tarjeta"), ("3", "Transferencia")]
    MetodoPago = models.CharField(max_length=10, choices=METODOPAGO, default="1", db_column='metodo_pago')

    ESTADO = [("0", "Facturado"), ("1", "Pendiente"), ("2", "Anulado"), ("4", "Preparado")]
    Estado = models.CharField(max_length=10, choices=ESTADO, default="1", db_column='estado')

    ACTIVO = [("1", "Activo"), ("0", "Eliminado")]
    EsActivo = models.CharField(max_length=10, choices=ACTIVO, default="1", db_column='es_activo')
    # activo = models.TextField(db_column='Activo', blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Orden'
        db_table = 'orden'

    def __str__(self):
        return f"ID = {self.Id} | Usuario = {self.IdUsuario.username} | Fecha = {self.Fecha} | Estado = {self.Estado} | Mesa = {self.IdMesa.Numero} | Area = {self.IdMesa.IdAreaMesa.Nombre}"

#endregion Orden

#region TipoPlatillo

class TipoPlatillo(models.Model):
    Id = models.AutoField(primary_key=True, db_column='id_tipo_platillo')
    
    Nombre = models.CharField(max_length=70, db_column='nombre')
    # activo = models.TextField(db_column='Activo', blank=True, null=True)

    ESTADOS = [("1", "Activo"), ("0", "Eliminado")]
    EsActivo = models.CharField(max_length=10, choices=ESTADOS, default="1", db_column='es_activo')

    class Meta:
        verbose_name_plural = 'TipoPlatillo'
        db_table = 'tipo_platillo'

    def __str__(self):
        return f"ID = {self.Id} | Tipo de platillo = {self.Nombre} | Activo = {self.EsActivo}"

#endregion TipoPlatillo

#region Platillo

class Platillo(models.Model):
    Id = models.AutoField(primary_key=True, db_column='id_platillo')
    
    IdTipoPlatillo = models.ForeignKey(TipoPlatillo, models.DO_NOTHING, db_column='id_tipo_platillo')
    
    Nombre = models.CharField(db_column='nombre', max_length=50)
    
    Precio = models.DecimalField(db_column='precio', max_digits=8, decimal_places=2)
    
    Descripcion = models.CharField(db_column='descripcion', max_length=300, blank=True, null=True)
    
    # imagenplatillo = models.TextField(db_column='ImagenPlatillo', blank=True, null=True)

    ImagenUrl = models.ImageField(upload_to="platillos", default="platillos/ProductoSinFoto.png", null=True, blank=True, db_column='imagen_url')

    # activo = models.TextField(db_column='Activo', blank=True, null=True)

    ESTADOS = [("1", "Activo"), ("0", "Eliminado")]
    EsActivo = models.CharField(max_length=10, choices=ESTADOS, default="1", db_column='es_activo')

    class Meta:
        verbose_name_plural = 'Platillo'
        db_table = 'platillo'

    def __str__(self):
        return f"ID = {self.Id} | Platillo = {self.Nombre} | Tipo de platillo = {self.IdTipoPlatillo.Nombre}"

#endregion Platillo

#region DetalleOrden

class DetalleOrden(models.Model):
    Id = models.AutoField(primary_key=True, db_column='id_detalle_orden')
    
    IdOrden = models.ForeignKey(
        Orden, models.DO_NOTHING, db_column='id_orden')
    
    IdPlatillo = models.ForeignKey(
        Platillo, models.DO_NOTHING, db_column='id_platillo')
    
    Cantidad = models.IntegerField(db_column='cantidad')
    
    PrecioVenta = models.DecimalField(db_column='precio_venta', max_digits=8, decimal_places=2)

    SubTotal = models.DecimalField(db_column='sub_total', max_digits=8, decimal_places=2)

    # activo = models.TextField(db_column='Activo', blank=True, null=True)

    ESTADOS = [("1", "Activo"), ("0", "Eliminado")]
    EsActivo = models.CharField(max_length=10, choices=ESTADOS, default="1", db_column='es_activo')

    class Meta:
        verbose_name_plural = 'DetalleOrden'
        db_table = 'detalle_orden'

    def __str__(self):
        return f"ID = {self.Id} | ID Orden = {self.IdOrden} | ID platillo = {self.IdPlatillo}"

#endregion DetalleOrden