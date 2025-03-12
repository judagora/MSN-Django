from django.db import models

# Create your models here.
from django.db import models

class Usuario(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    nombres = models.CharField(max_length=30)
    apellidos = models.CharField(max_length=30)
    telefono = models.CharField(max_length=20)
    correo_electronico = models.EmailField(max_length=40)
    nombre_usuario = models.CharField(max_length=30)
    contraseña = models.CharField(max_length=64)
    rol_usuario = models.CharField(max_length=30, default="Cliente")

    def __str__(self):
        return f"{self.nombres} {self.apellidos}"


class Mantenimiento(models.Model):
    id_mantenimiento = models.AutoField(primary_key=True)
    tipo_mantenimiento = models.CharField(max_length=20, choices=[('Preventivo', 'Preventivo'), ('Correctivo', 'Correctivo')])
    descripcion = models.CharField(max_length=255)
    costo = models.CharField(max_length=15)
    notas_adicionales = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Mantenimiento {self.id_mantenimiento} - {self.tipo_mantenimiento}"


class Peritaje(models.Model):
    id_peritaje = models.AutoField(primary_key=True)
    descripcion = models.TextField()

    def __str__(self):
        return f"Peritaje {self.id_peritaje}"


class RepuestosModificados(models.Model):
    id_repuestos_modificados = models.AutoField(primary_key=True)
    motivo_del_cambio = models.CharField(max_length=255)
    descripcion_del_cambio = models.CharField(max_length=255)
    costo_repuesto = models.TextField()

    def __str__(self):
        return f"Repuesto Modificado {self.id_repuestos_modificados}"


class Cliente(models.Model):
    id_cliente = models.AutoField(primary_key=True)
    estado_de_la_cuenta = models.CharField(max_length=10, choices=[('ACTIVO', 'ACTIVO'), ('INACTIVO', 'INACTIVO')])
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    def __str__(self):
        return f"Cliente {self.id_cliente} - {self.id_usuario.nombres}"


class MantenimientoProgramado(models.Model):
    id_mantenimiento = models.AutoField(primary_key=True)
    tipo_Mantenimiento = models.CharField(max_length=30)
    id_mecanico = models.ForeignKey('Mecanico', on_delete=models.SET_NULL, null=True)
    id_vehiculo = models.ForeignKey('Vehiculo', on_delete=models.CASCADE)
    id_taller_mecanico = models.ForeignKey('TallerMecanico', on_delete=models.SET_NULL, null=True)
    fecha_mantenimiento = models.DateField()
    hora_mantenimiento = models.TimeField()
    notas = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"Mantenimiento Programado {self.id_mantenimiento}"


class Notificaciones(models.Model):
    id_notificaciones = models.AutoField(primary_key=True)
    motivo = models.CharField(max_length=45)
    fecha_recordatorio = models.DateField()
    hora_recordatorio = models.TimeField()
    notas = models.CharField(max_length=100, blank=True, null=True)
    id_cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)

    def __str__(self):
        return f"Notificación {self.id_notificaciones} - {self.motivo}"


class Vehiculo(models.Model):
    id_vehiculo = models.AutoField(primary_key=True)
    modelo = models.CharField(max_length=4)
    tipo = models.CharField(max_length=20, choices=[('Automovil', 'Automovil'), ('Camioneta', 'Camioneta'), ('Motocicleta', 'Motocicleta')])
    marca = models.CharField(max_length=30)
    placa = models.CharField(max_length=6)
    color = models.CharField(max_length=20)
    kilometraje = models.IntegerField()
    id_cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    id_peritaje = models.ForeignKey(Peritaje, on_delete=models.SET_NULL, null=True)
    id_mantenimiento = models.ForeignKey(Mantenimiento, on_delete=models.SET_NULL, null=True)
    id_repuestos_modificados = models.ForeignKey(RepuestosModificados, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"Vehículo {self.placa} - {self.marca} {self.modelo}"


class Soat(models.Model):
    id_soat = models.AutoField(primary_key=True)
    estado_poliza = models.CharField(max_length=20, choices=[('Activa', 'Activa'), ('Espera', 'Espera'), ('En espera', 'En espera')])
    aseguradora = models.CharField(max_length=30)
    fecha_vencimiento = models.DateField()
    id_vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE)

    def __str__(self):
        return f"SOAT {self.id_soat} - {self.aseguradora}"


class Mecanico(models.Model):
    id_mecanico = models.AutoField(primary_key=True)
    horario_de_trabajo = models.TimeField()
    experiencia_laboral = models.CharField(max_length=255)
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    def __str__(self):
        return f"Mecánico {self.id_mecanico} - {self.id_usuario.nombres}"


class MecanicoMantenimiento(models.Model):
    id_mecanico = models.ForeignKey(Mecanico, on_delete=models.CASCADE)
    id_mantenimiento = models.ForeignKey(Mantenimiento, on_delete=models.CASCADE)

    def __str__(self):
        return f"Mecánico {self.id_mecanico} - Mantenimiento {self.id_mantenimiento}"


class VehiculoMantenimiento(models.Model):
    id_vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE)
    id_mantenimiento = models.ForeignKey(Mantenimiento, on_delete=models.CASCADE)

    def __str__(self):
        return f"Vehículo {self.id_vehiculo} - Mantenimiento {self.id_mantenimiento}"


class VehiculoPeritaje(models.Model):
    id_vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE)
    id_peritaje = models.ForeignKey(Peritaje, on_delete=models.CASCADE)

    def __str__(self):
        return f"Vehículo {self.id_vehiculo} - Peritaje {self.id_peritaje}"


class VehiculoRepuestosModificados(models.Model):
    id_vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE)
    id_repuestos_modificados = models.ForeignKey(RepuestosModificados, on_delete=models.CASCADE)

    def __str__(self):
        return f"Vehículo {self.id_vehiculo} - Repuesto Modificado {self.id_repuestos_modificados}"


class Administrador(models.Model):
    id_administrador = models.AutoField(primary_key=True)
    ubicacion = models.CharField(max_length=45)
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    def __str__(self):
        return f"Administrador {self.id_administrador} - {self.id_usuario.nombres}"


class TallerMecanico(models.Model):
    id_taller_mecanico = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=30)
    direccion = models.CharField(max_length=60)
    telefono = models.CharField(max_length=20)
    horario_de_atencion = models.TimeField()
    id_administrador = models.ForeignKey(Administrador, on_delete=models.CASCADE)
    id_mecanico = models.ForeignKey(Mecanico, on_delete=models.CASCADE)

    def __str__(self):
        return f"Taller Mecánico {self.nombre}"


class MantenimientoRepuestosModificados(models.Model):
    id_mantenimiento = models.ForeignKey(Mantenimiento, on_delete=models.CASCADE)
    id_repuestos_modificados = models.ForeignKey(RepuestosModificados, on_delete=models.CASCADE)

    def __str__(self):
        return f"Mantenimiento {self.id_mantenimiento} - Repuesto Modificado {self.id_repuestos_modificados}"