from django.db import models
from django import forms

CATEGORIE_ICONES = {
    'cosmetique': 'cosmetique',
    'chaussure': 'chaussure',
    'basin': 'basin',
    'alimentaire': 'alimentaire',
    'electronique': 'electronique',
    'vetement': 'vetement',
    'accessoire': 'accessoire',
    'maison': 'maison',
    'jouet': 'jouet',
    'autre': 'autre',
}


class Categorie(models.Model):
    nom = models.CharField(max_length=50)
    icone = models.CharField(max_length=50, blank=True, help_text="Nom de l'icône FontAwesome ou SVG", default='')

    def save(self, *args, **kwargs):
        if not self.icone or self.icone == '':
            key = self.nom.strip().lower()
            self.icone = CATEGORIE_ICONES.get(key, 'autre')
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nom


class Produit(models.Model):
    nom = models.CharField(max_length=100)
    quantite = models.PositiveIntegerField(default=0)
    quantite_vendue = models.PositiveIntegerField(default=0)
    prix_unitaire = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    categorie = models.ForeignKey(Categorie, on_delete=models.SET_NULL, null=True, blank=True, related_name='produits')
    # Autres champs pertinents


class Vente(models.Model):
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE, related_name='ventes')
    quantite = models.PositiveIntegerField()
    prix_total = models.DecimalField(max_digits=12, decimal_places=2)
    date_vente = models.DateTimeField(auto_now_add=True)
    # Autres champs pertinents


class CategorieForm(forms.ModelForm):
    class Meta:
        model = Categorie
        fields = ['nom']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom de la catégorie'})
        }
