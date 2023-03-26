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
- Changer l'image dans shop/static/img/default