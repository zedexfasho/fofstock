from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),

    path('produits/', views.ListeProduitsView.as_view(), name='produit_liste'),
    path('produit/<int:pk>/', views.DetailProduitView.as_view(), name='detail_produit'),
    path('produit/ajouter/', views.AjouterProduitView.as_view(), name='produit_ajouter'),
    path('produit/<int:pk>/modifier/', views.ModifierProduitView.as_view(), name='modifier_produit'),
    path('produit/<int:pk>/supprimer/', views.SupprimerProduitView.as_view(), name='supprimer_produit'),

    path('categorie/ajouter/', views.AjouterCategorieView.as_view(), name='ajouter_categorie'),

    path('vente/ajouter/', views.EnregistrerVenteView.as_view(), name='ajouter_vente'),
]
