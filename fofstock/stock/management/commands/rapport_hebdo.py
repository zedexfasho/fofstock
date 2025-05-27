from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils import timezone
from django.conf import settings
from .models import Produit, Vente

def envoyer_rapport_hebdomadaire():
    produits = Produit.objects.all()
    ventes = Vente.objects.filter(date_vente__week=timezone.now().isocalendar()[1])
    total_revenu = sum(v.prix_total for v in ventes)
    produits_faible_stock = produits.filter(quantite__lt=5)
    context = {
        'produits': produits,
        'ventes': ventes,
        'total_revenu': total_revenu,
        'produits_faible_stock': produits_faible_stock,
    }
    subject = 'Rapport hebdomadaire Fofboutik'
    message = render_to_string('stock/email_rapport.html', context)
    send_mail(
        subject,
        '',
        settings.DEFAULT_FROM_EMAIL,
        [settings.REPORT_EMAIL],
        html_message=message
    )
