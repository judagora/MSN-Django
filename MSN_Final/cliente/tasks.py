from celery import shared_task
from django.core.mail import send_mail
from django.utils.timezone import now
from inicio.models import Notificaciones

@shared_task
def enviar_notificacion():
    hoy  = now().date()
    notificaciones = Notificaciones.objects.filter(fecha_recordatorio=hoy)

    for notificacion in notificaciones:
        cliente_email = notificacion.id_cliente.id_usuario.correo_electronico
        motivo = notificacion.motivo
        notas  = notificacion.notas if notificacion.notas else "Sin notas"
        send_mail(
            subject=f"Recordatorio: {motivo}",
            message=f"Hola {notificacion.id_cliente.id_usuario.nombres},\n\nEste es un recordatorio:\nMotivo: {motivo}\nNotas: {notas}\n\nAtentamente, Motors Safety Net.",
            from_email='motorssafetynet@gmail.com',
            recipient_list=[cliente_email],
            fail_silently=False,
        )
    return f"Se enviaron {notificaciones.count()} notificaciones."    

@shared_task
def test_task():
    return "Celery está funcionando correctamente."   