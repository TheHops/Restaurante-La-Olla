from django.db import models
from django.contrib.auth.models import AbstractUser

# class Personal(AbstractUser):
#     id = models.AutoField(primary_key=True)
#     # Field name made lowercase.
#     idcargo = models.ForeignKey(Cargo, models.DO_NOTHING, default=3)
#     # Field name made lowercase.
#     nombreusuario = models.CharField(
#         db_column='NombreUsuario', max_length=20, blank=True, null=True)
#     # Field name made lowercase.
#     nombres = models.CharField(db_column='Nombres', max_length=15, default="")
#     # Field name made lowercase.
#     apellidos = models.CharField(
#         db_column='Apellidos', max_length=15, default="")
#     # Field name made lowercase.
#     direccionpers = models.CharField(
#         db_column='DireccionPers', max_length=70, blank=True, null=True, default="")
#     # Field name made lowercase.
#     correopers = models.CharField(
#         db_column='CorreoPers', max_length=70, default="")
#     # Field name made lowercase.
#     telefonopers = models.CharField(
#         db_column='TelefonoPers', max_length=20, blank=True, null=True)
#     # Field name made lowercase.
#     # clave = models.CharField(db_column='Clave', max_length=20)
#     # Field name made lowercase. This field type is a guess.
#     # activo = models.TextField(db_column='Activo', blank=True, null=True)

#     ESTADOS = [("1", "Activo"), ("0", "Inactivo")]
#     activo = models.CharField(max_length=10, choices=ESTADOS, default="1")

#     # def __str__(self):
#     #     return f"ID = {self.id} | Usuario = {self.nombreusuario} | Existe = {self.existe}"

#     class Meta:
#         db_table = 'personal'

#     def __str__(self):
#         return f"Nombre de usuario = {self.username} | Cargo = {self.idcargo.nombrecargo} | Correo = {self.email}"

# Create your models here.

#region AreaMesa

class Areamesa(models.Model):
    id = models.AutoField(primary_key=True)
    # Field name made lowercase.
    nombream = models.CharField(db_column='NombreAM', max_length=20)
    # Field name made lowercase. This field type is a guess.
    # activo = models.TextField(db_column='Activo', blank=True, null=True)

    ESTADOS = [("1", "Activo"), ("0", "Eliminado")]
    activo = models.CharField(max_length=10, choices=ESTADOS, default="1")

    class Meta:
        db_table = 'areamesa'

    def __str__(self):
        return f"Area de mesa = {self.nombream} | ID = {self.id}"
    
#endregion AreaMesa

#region Cargo

class Cargo(models.Model):
    id = models.AutoField(primary_key=True)
    # Field name made lowercase.
    nombrecargo = models.CharField(db_column='NombreCargo', max_length=20)
    # Field name made lowercase. This field type is a guess.
    # activo = models.TextField(db_column='Activo', blank=True, null=True)

    ESTADOS = [("1", "Activo"), ("0", "Eliminado")]
    activo = models.CharField(max_length=10, choices=ESTADOS, default="1")

    class Meta:
        db_table = 'cargo'

    def __str__(self):
        return f"Cargo = {self.nombrecargo} | ID = {self.id}"
    
#endregion Cargo

#region DetalleOrden (wip)

class DetalleOrden(models.Model):
    id = models.AutoField(primary_key=True)
    # Field name made lowercase.
    idfactura = models.ForeignKey(
        'Factura', models.DO_NOTHING)
    # Field name made lowercase.
    idplatillo = models.ForeignKey(
        'Platillo', models.DO_NOTHING)
    # Field name made lowercase.
    cantidad = models.IntegerField(db_column='Cantidad')
    # Field name made lowercase.
    precioventa = models.DecimalField(
        db_column='PrecioVenta', max_digits=6, decimal_places=2)
    # Field name made lowercase. This field type is a guess.
    # activo = models.TextField(db_column='Activo', blank=True, null=True)

    ESTADOS = [("1", "Activo"), ("0", "Eliminado")]
    activo = models.CharField(max_length=10, choices=ESTADOS, default="1")

    class Meta:
        db_table = 'detallefactura'

    def __str__(self):
        return f"ID factura = {self.idfactura} | ID platillo = {self.idplatillo}"

#endregion DetalleOrden (wip)

#region Orden (wip)

class Orden(models.Model):
    id = models.AutoField(primary_key=True)
    # Field name made lowercase.
    idpersonal = models.ForeignKey(
        'Personal', models.DO_NOTHING)
    # Field name made lowercase.
    idmetodopago = models.ForeignKey(
        'Metodopago', models.DO_NOTHING, default=1)
    # Field name made lowercase.
    idmesa = models.ForeignKey('Mesa', models.DO_NOTHING)
    # Field name made lowercase.
    total = models.IntegerField(db_column='Total')
    # Field name made lowercase.
    monto = models.IntegerField(
        db_column='Monto', null=True, blank=True, default=0)
    # Field name made lowercase.
    cambio = models.IntegerField(
        db_column='Cambio', null=True, blank=True, default=0)
    # Field name made lowercase.
    fechaventa = models.DateTimeField(
        db_column='FechaVenta', auto_now_add=True)
    # Field name made lowercase. This field type is a guess.
    # activo = models.TextField(db_column='Activo', blank=True, null=True)

    ESTADO = [("1", "Pendiente"), ("0", "Facturado"), ("2", "Anulado")]
    estado = models.CharField(max_length=10, choices=ESTADO, default="1")

    ACTIVO = [("1", "Activo"), ("0", "Eliminado")]
    activo = models.CharField(max_length=10, choices=ACTIVO, default="1")

    propina = models.IntegerField(
        db_column='Propina', null=True, blank=True, default=0)

    class Meta:
        db_table = 'factura'

    def __str__(self):
        return f"ID = {self.id} | Personal = {self.idpersonal.username} | Fecha de venta = {self.fechaventa} | Estado = {self.estado}"

#endregion Orden

#region Mesa

class Mesa(models.Model):
    id = models.AutoField(primary_key=True)
    # Field name made lowercase.
    idareamesa = models.ForeignKey(
        Areamesa, models.DO_NOTHING)
    # Field name made lowercase.
    numeromesa = models.IntegerField(db_column='NumeroMesa')
    # Field name made lowercase.
    capacidad = models.IntegerField(db_column='Capacidad')
    # Field name made lowercase. This field type is a guess.
    estado = models.TextField(db_column='Estado', blank=True, null=True)
    # Field name made lowercase. This field type is a guess.
    # activo = models.TextField(db_column='Activo', blank=True, null=True)

    ESTADOS = [("1", "Activo"), ("0", "Eliminado")]
    activo = models.CharField(max_length=10, choices=ESTADOS, default="1")

    class Meta:
        db_table = 'mesa'

    def __str__(self):
        return f"Mesa = {self.numeromesa} | Area de mesa = {self.idareamesa.nombream} | ID = {self.id}"

#endregion Mesa

#region Platillo

class Platillo(models.Model):
    id = models.AutoField(primary_key=True)
    # Field name made lowercase.
    idtipoplatillo = models.ForeignKey(
        'Tipoplatillo', models.DO_NOTHING)
    # Field name made lowercase.
    nombreplatillo = models.CharField(
        db_column='NombrePlatillo', max_length=50)
    # Field name made lowercase.
    precioplatillo = models.DecimalField(
        db_column='PrecioPlatillo', max_digits=7, decimal_places=2)
    # Field name made lowercase.
    descripcionplatillo = models.CharField(
        db_column='DescripcionPlatillo', max_length=150, blank=True, null=True)
    # Field name made lowercase.
    # imagenplatillo = models.TextField(db_column='ImagenPlatillo', blank=True, null=True)

    imagen_platillo = models.ImageField(
        upload_to="platillos", default="platillos/ProductoSinFoto.png", null=True, blank=True)

    # Field name made lowercase. This field type is a guess.
    # activo = models.TextField(db_column='Activo', blank=True, null=True)

    ESTADOS = [("1", "Activo"), ("0", "Eliminado")]
    activo = models.CharField(max_length=10, choices=ESTADOS, default="1")

    class Meta:
        db_table = 'platillo'

    def __str__(self):
        return f"ID = {self.id} | Platillo = {self.nombreplatillo} | Tipo de platillo = {self.idtipoplatillo.nombretp}"

#endregion Platillo

#region TipoPlatillo

class Tipoplatillo(models.Model):
    id = models.AutoField(primary_key=True)
    # Field name made lowercase.
    nombretp = models.CharField(db_column='NombreTP', max_length=15)
    # Field name made lowercase. This field type is a guess.
    # activo = models.TextField(db_column='Activo', blank=True, null=True)

    ESTADOS = [("1", "Activo"), ("0", "Eliminado")]
    activo = models.CharField(max_length=10, choices=ESTADOS, default="1")

    class Meta:
        db_table = 'tipoplatillo'

    def __str__(self):
        return f"Tipo de platillo = {self.nombretp} | ID = {self.id} | activo = {self.activo}"

#endregion TipoPlatillo