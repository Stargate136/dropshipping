# e-shop
## Pour utiliser stripe
- ajouter les produits sur stripe

### en local
- installer stripe CLI https://stripe.com/docs/stripe-cli#install
**Dans un terminal** 
- taper la commande 'stripe login' dans un terminal
- taper la commande 'stripe listen --forward-to <url de la vue stripe_webhook>'
- ajouter la clé affichée dans le terminal dans .env avec le nom ENDPOINT_SECRET

### en production
- sur stripe onglet développeurs / webhook
- ajouter un endpoint
- rentrer l'url <nom_de_domaine>/stripe-webhook
- copier la clé secrete dans ENDPOINT_SECRET de .env
- copier la clé d'API dans STRIPE_API_KEY de .env

## Avant de mettre en production
- Changer les images dans shop/static/img (banner, default et logo) MAIS LES NOMMER PAREIL (100px de hauteur pour la bannière)
- Modifier tous les templates pour mettre le nom de la boutique
- Choisir un theme dans le dossier shop/css/themes et l'appliquer dans le fichier shop/templates/base.html