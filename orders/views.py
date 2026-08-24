import urllib.parse
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import OrderItem
from .forms import OrderCreateForm
from .cart import Cart
from menu.models import Product

def cart_detail(request):
    """Affiche le détail du panier."""
    cart = Cart(request)
    return render(request, 'orders/cart_detail.html', {'cart': cart})

def cart_add(request, product_id):
    """Ajoute un produit au panier."""
    product = get_object_or_404(Product, id=product_id)
    cart = Cart(request)
    
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        sauce_id = request.POST.get('sauce_id')
        extra_ids = request.POST.getlist('extra_ids')
        
        # Convertir les IDs en entiers s'ils ne sont pas vides
        extra_ids = [int(id) for id in extra_ids if id]
        sauce_id = int(sauce_id) if sauce_id else None
        
        cart.add(
            product=product,
            quantity=quantity,
            sauce_id=sauce_id,
            extra_ids=extra_ids if extra_ids else None
        )
        
        # Redirection selon le type de requête
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'status': 'success',
                'message': f'{product.name} ajouté au panier',
                'cart_count': len(cart)
            })
        
        return redirect('orders:cart_detail')
    
    # GET request - afficher le formulaire d'ajout
    return render(request, 'menu/product_detail.html', {'product': product})

def cart_remove(request, item_key):
    """Supprime un article du panier."""
    cart = Cart(request)
    cart.remove(item_key)
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'status': 'success',
            'message': 'Article supprimé du panier',
            'cart_count': len(cart)
        })
    
    return redirect('orders:cart_detail')

def checkout(request):
    """Valide la commande et redirige le client vers WhatsApp avec le recapitulatif."""
    cart = Cart(request)
    if len(cart) == 0:
        return redirect('pages:home')

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.total_amount = cart.get_total_price()
            order.save()

            # Construction du message texte WhatsApp
            msg_lines = [
                f"🍗 *NOUVELLE COMMANDE CHICKEN TENDERS #{order.id}*",
                f"👤 Client: {order.customer_name}",
                f"📞 Tél: {order.customer_phone}",
            ]
            
            if order.order_type == 'delivery':
                msg_lines.append(f"📍 Zone: {order.delivery_zone}")
                msg_lines.append(f"🏠 Adresse: {order.delivery_address}")
            else:
                msg_lines.append("🛍️ Option: À emporter")

            msg_lines.append("\n🛒 *Détails du panier :*")
            
            for item in cart:
                line = f"- {item['quantity']}x {item['product_name']} ({item['unit_price']} FCFA)"
                if item.get('sauce_name'):
                    line += f" [Sauce: {item['sauce_name']}]"
                msg_lines.append(line)

                OrderItem.objects.create(
                    order=order,
                    product_id=item['product_id'],
                    quantity=item['quantity'],
                    unit_price=item['unit_price']
                )

            msg_lines.append(f"\n💰 *TOTAL À PAYER: {order.total_amount} FCFA*")
            if order.notes:
                msg_lines.append(f"📝 Notes: {order.notes}")

            cart.clear()

            # Remplacez ce numéro par votre numéro WhatsApp professionnel à Dakar
            restaurant_whatsapp = "221782379280" 
            encoded_message = urllib.parse.quote("\n".join(msg_lines))
            whatsapp_url = f"https://wa.me/{restaurant_whatsapp}?text={encoded_message}"

            return redirect(whatsapp_url)
    else:
        form = OrderCreateForm()

    return render(request, 'orders/checkout.html', {'cart': cart, 'form': form})