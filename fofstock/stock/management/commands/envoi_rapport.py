from django.core.management.base import BaseCommand
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from stock.models import Produit

class Command(BaseCommand):
    help = 'Envoie le rapport hebdomadaire des transactions'

    def handle(self, *args, **kwargs):
        produits = Produit.objects.all()
        context = {
            'produits': produits,
        }
        message = render_to_string('inventory/email_rapport.html', context)
        email = EmailMessage(
            'Rapport hebdomadaire des transactions',
            message,
            'votre_email@example.com',
            ['destinataire@example.com'],
        )
        email.content_subtype = 'html'
        email.send()
