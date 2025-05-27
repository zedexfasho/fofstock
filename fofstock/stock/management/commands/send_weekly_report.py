from django.core.management.base import BaseCommand
from stock.management.commands.rapport_hebdo import envoyer_rapport_hebdomadaire

class Command(BaseCommand):
    help = 'Envoie le rapport hebdomadaire des ventes, stocks, revenus et alertes de stock faible.'

    def handle(self, *args, **kwargs):
        envoyer_rapport_hebdomadaire()
        self.stdout.write(self.style.SUCCESS('Rapport hebdomadaire envoyé avec succès.'))
