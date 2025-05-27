from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Produit, Categorie, CategorieForm, Vente
from django.shortcuts import render
from django.views.generic.edit import FormView
from django import forms



class ListeProduitsView(ListView):
    model = Produit
    template_name = 'stock/produit_liste.html'
    context_object_name = 'produits'

class DetailProduitView(DetailView):
    model = Produit
    template_name = 'stock/produit_detail.html'

class AjouterProduitView(CreateView):
    model = Produit
    fields = ['nom', 'quantite', 'prix_unitaire', 'categorie']
    template_name = 'stock/produit_form.html'
    success_url = reverse_lazy('produit_liste')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Categorie.objects.all()
        return context

class ModifierProduitView(UpdateView):
    model = Produit
    fields = ['nom', 'quantite', 'prix_unitaire', 'categorie']
    template_name = 'stock/produit_form.html'
    success_url = reverse_lazy('produit_liste')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Categorie.objects.all()
        return context

class SupprimerProduitView(DeleteView):
    model = Produit
    template_name = 'stock/produit_confirm_delete.html'
    success_url = reverse_lazy('produit_liste')

class AjouterCategorieView(FormView):
    template_name = 'stock/categorie_form.html'
    form_class = CategorieForm
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

def dashboard(request):
    produits = Produit.objects.all()
    categories = Categorie.objects.all()
    ventes = Vente.objects.all()
    total_produits = produits.count()
    total_vendus = sum(p.quantite_vendue for p in produits)
    total_stock = sum(p.quantite for p in produits)
    produits_faible_stock = produits.filter(quantite__lt=5)
    total_revenu = sum(v.prix_total for v in ventes)
    total_ventes = ventes.count()
    
    context = {
        'produits': produits,
        'categories': categories,
        'total_produits': total_produits,
        'total_vendus': total_vendus,
        'total_stock': total_stock,
        'produits_faible_stock': produits_faible_stock,
        'total_revenu': total_revenu,
        'total_ventes': total_ventes,
        'ventes': ventes,
    }
    return render(request, 'stock/dashboard.html', context)

class VenteForm(forms.ModelForm):
    class Meta:
        model = Vente
        fields = ['produit', 'quantite']

    def clean(self):
        cleaned_data = super().clean()
        produit = cleaned_data.get('produit')
        quantite = cleaned_data.get('quantite')
        if produit and quantite:
            if quantite > produit.quantite:
                self.add_error('quantite', "Stock insuffisant pour cette vente.")
        return cleaned_data

class EnregistrerVenteView(FormView):
    template_name = 'stock/vente_form.html'
    form_class = VenteForm
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        vente = form.save(commit=False)
        produit = vente.produit
        vente.prix_total = produit.prix_unitaire * vente.quantite
        produit.quantite -= vente.quantite
        produit.quantite_vendue += vente.quantite
        produit.save()
        vente.save()
        return super().form_valid(form)


# Create your views here.
