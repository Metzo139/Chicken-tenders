from decimal import Decimal
from menu.models import Product, Sauce, Extra

class Cart:
    def __init__(self, request):
        """Initialise le panier à partir de la session Django."""
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart

    def add(self, product, quantity=1, sauce_id=None, extra_ids=None, override_quantity=False):
        """Ajoute un produit au panier avec sa sauce et ses extras."""
        sauce = None
        if sauce_id:
            try:
                sauce = Sauce.objects.get(id=sauce_id)
            except Sauce.DoesNotExist:
                pass

        extras = []
        if extra_ids:
            extras = list(Extra.objects.filter(id__in=extra_ids))

        # Clé unique pour différencier le même produit avec des options différentes
        sauce_key = f"s{sauce.id}" if sauce else "s0"
        extra_key = "e" + "_".join(sorted([str(e.id) for e in extras])) if extras else "e0"
        item_key = f"{product.id}_{sauce_key}_{extra_key}"

        if item_key not in self.cart:
            # Calcul du prix unitaire incluant les options
            unit_price = product.price
            if sauce:
                unit_price += sauce.additional_price
            for extra in extras:
                unit_price += extra.price

            self.cart[item_key] = {
                'item_key': item_key,
                'product_id': product.id,
                'product_name': product.name,
                'image_url': product.image.url if product.image else '',
                'unit_price': int(unit_price),
                'quantity': 0,
                'sauce_id': sauce.id if sauce else None,
                'sauce_name': sauce.name if sauce else None,
                'extras': [{'id': e.id, 'name': e.name, 'price': int(e.price)} for e in extras],
            }

        if override_quantity:
            self.cart[item_key]['quantity'] = quantity
        else:
            self.cart[item_key]['quantity'] += quantity

        self.save()

    def save(self):
        """Marque la session comme modifiée pour enregistrer les changements."""
        self.session.modified = True

    def remove(self, item_key):
        """Supprime un article du panier via sa clé unique."""
        if item_key in self.cart:
            del self.cart[item_key]
            self.save()

    def __iter__(self):
        """Parcourt les éléments du panier et calcule le prix total par ligne."""
        for item in self.cart.values():
            item_copy = item.copy()
            item_copy['total_price'] = item_copy['unit_price'] * item_copy['quantity']
            yield item_copy

    def __len__(self):
        """Compte le nombre total d'articles dans le panier."""
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        """Calcule le montant total cumulé du panier."""
        return sum(item['unit_price'] * item['quantity'] for item in self.cart.values())

    def clear(self):
        """Vide entièrement le panier de la session."""
        del self.session['cart']
        self.save()