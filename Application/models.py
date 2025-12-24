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

    IdCargo = models.ForeignKey(Cargo, on_delete=models.SET_NULL, null=True, verbose_name="Cargo", db_column='id_cargo', related_name='Usuarios')
    Nombres = models.CharField(max_length=15, default="", db_column='nombres')
    Apellidos = models.CharField(max_length=15, default="", db_column='apellidos')
    Direccion = models.CharField(max_length=120, blank=True, null=True, default="", db_column='direccion')
    Telefono = models.CharField(max_length=20, blank=True, null=True, db_column='telefono')
    
    email = models.EmailField(unique=True, null=True, default=None, db_column="email")

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
    
    Nombre = models.CharField(db_column='nombre', max_length=30)

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
    
    IdAreaMesa = models.ForeignKey(AreaMesa, models.DO_NOTHING, db_column='id_area_mesa', related_name='Mesas')
    
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
    
    IdAreaDeMesa = models.ForeignKey(AreaMesa, models.DO_NOTHING, db_column='id_area_de_mesa', null=True, blank=True)
    
    AreaDeMesa = models.CharField(max_length=30, null=True, blank=True, db_column='area_de_mesa')
    
    Descripcion = models.CharField(max_length=100, null=True, blank=True, db_column='descripcion')
    
    Motivo = models.CharField(max_length=70, null=True, blank=True, db_column='motivo')
    
    NumRef = models.CharField(max_length=15, null=True, blank=True, db_column='num_ref')
    
    Total = models.DecimalField(db_column='total', null=True, blank=True, default=0, max_digits=8, decimal_places=2)
    
    Monto = models.DecimalField(db_column='monto', null=True, blank=True, default=0, max_digits=8, decimal_places=2)
    
    Cambio = models.DecimalField(db_column='cambio', null=True, blank=True, default=0, max_digits=8, decimal_places=2)
    
    Propina = models.DecimalField(db_column='propina', null=True, blank=True, default=0, max_digits=8, decimal_places=2)
    
    Descuento = models.DecimalField(db_column='descuento', null=True, blank=True, default=0, max_digits=8, decimal_places=2)
    
    Fecha = models.DateTimeField(db_column='fecha', auto_now_add=True)
    
    UltimaModificacion = models.DateTimeField(db_column='ultima_modificacion', auto_now_add=True)
    
    FueEditada = models.BooleanField(db_column="fue_editada", null=True, default=False)
    DescripcionEdicion = models.CharField(max_length=100, null=True, blank=True, db_column='descripcion_edicion')
    
    METODOPAGO = [("1", "Efectivo"), ("2", "Tarjeta"), ("3", "Transferencia"), ("4", "EfectivoYTarjeta")]
    MetodoPago = models.CharField(max_length=10, choices=METODOPAGO, default="1", db_column='metodo_pago')

    ESTADO = [("0", "Facturado"), ("1", "Pendiente"), ("2", "Anulado"), ("3", "Preparado"), ("4", "EnPreparacion")]
    Estado = models.CharField(max_length=10, choices=ESTADO, default="1", db_column='estado')
    
    BANCOS = [("1", "Lafise"), ("2", "Banpro"), ("3", "BAC"), ("4", "Ficohsa"), ("5", "Avanz"), ("6", "Banco Atlántida"), ("7", "BFP"), ("8", "FDL")]
    Banco = models.CharField(max_length=10, choices=BANCOS, null=True, blank=True, db_column='banco')

    ACTIVO = [("1", "Activo"), ("0", "Eliminado")]
    EsActivo = models.CharField(max_length=10, choices=ACTIVO, default="1", db_column='es_activo')
    # activo = models.TextField(db_column='Activo', blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Orden'
        db_table = 'orden'
        
    def recalcular_estado(self):
        activos = self.Detalles.filter(EsActivo="1").count()
        self.EsActivo = "1" if activos > 0 else "0"
        self.save()

    def __str__(self):
        return f"ID = {self.Id} | Usuario = {self.IdUsuario.username} | Fecha = {self.Fecha} | Estado = {self.Estado} | Area = {self.AreaDeMesa}"

#endregion Orden

#region MesasPorOrden

class MesasPorOrden(models.Model):
    Id = models.AutoField(primary_key=True, db_column='id_mesas_por_orden')
    
    IdOrden = models.ForeignKey(Orden, models.DO_NOTHING, db_column='id_orden', related_name='Mesas')
    IdMesa = models.ForeignKey(Mesa, models.DO_NOTHING, db_column='id_mesa')

    ESTADOS = [("1", "Activo"), ("0", "Eliminado")]
    EsActivo = models.CharField(max_length=10, choices=ESTADOS, default="1", db_column='es_activo')

    class Meta:
        verbose_name_plural = 'MesasPorOrden'
        db_table = 'mesas_por_orden'

    def __str__(self):
        return f"ID = {self.Id} | Orden = #{self.IdOrden.Id} | Activo = {self.EsActivo} | Mesa = {self.IdMesa.Numero}"

#endregion MesasPorOrden

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
    
    IdTipoPlatillo = models.ForeignKey(TipoPlatillo, models.DO_NOTHING, db_column='id_tipo_platillo', related_name='Platillos')
    
    Nombre = models.CharField(db_column='nombre', max_length=50)
    
    Precio = models.DecimalField(db_column='precio', max_digits=8, decimal_places=2)
    
    Descripcion = models.CharField(db_column='descripcion', max_length=300, blank=True, null=True)
    
    # imagenplatillo = models.TextField(db_column='ImagenPlatillo', blank=True, null=True)

    ImagenUrl = models.ImageField(upload_to="platillos", default="platillos/ProductoSinFoto.png", db_column='imagen_url')

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
        Orden, models.DO_NOTHING, db_column='id_orden', related_name='Detalles')
    
    IdPlatillo = models.ForeignKey(
        Platillo, models.DO_NOTHING, db_column='id_platillo')
    
    Cantidad = models.IntegerField(db_column='cantidad')
    
    PrecioVenta = models.DecimalField(db_column='precio_venta', max_digits=8, decimal_places=2)

    SubTotal = models.DecimalField(db_column='sub_total', max_digits=8, decimal_places=2)
    
    # Sirve para indicar si fué editado o creado en una edición
    DesdeEdicion = models.BooleanField(db_column="desde_edicion", null=True, default=False)

    # activo = models.TextField(db_column='Activo', blank=True, null=True)

    ESTADOS = [("1", "Activo"), ("0", "Eliminado")]
    EsActivo = models.CharField(max_length=10, choices=ESTADOS, default="1", db_column='es_activo')

    class Meta:
        verbose_name_plural = 'DetalleOrden'
        db_table = 'detalle_orden'

    def __str__(self):
        return f"ID = {self.Id} | ID Orden = {self.IdOrden} | ID platillo = {self.IdPlatillo}"

#endregion DetalleOrden