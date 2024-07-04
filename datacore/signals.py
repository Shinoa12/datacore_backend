from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Ajustes, User


@receiver(post_save, sender=Ajustes)
def update_user_settings(sender, instance, **kwargs):
    if instance.codigo == "RECURSOS_MAX" or instance.codigo == "HORAS_MAX":
        with transaction.atomic():
            recursos_max = Ajustes.objects.get(codigo="RECURSOS_MAX").valor
            horas_max = Ajustes.objects.get(codigo="HORAS_MAX").valor
            User.objects.update(
                recursos_max=int(recursos_max), horas_max=int(horas_max)
            )
