from django.shortcuts import render, get_object_or_404, redirect
from movies.models import Movie
from .utils import calculate_cart_total
from .models import Order, Item
from django.contrib.auth.decorators import login_required

def index(request):
    cart = request.session.get('cart', {})
    movie_ids = list(cart.keys())

    movies_in_cart = []
    cart_total = 0
    movie_data = []

    if movie_ids:
        int_ids = [int(mid) for mid in movie_ids]
        movies_in_cart = Movie.objects.filter(id__in=int_ids)
        cart_total = calculate_cart_total(cart, movies_in_cart)
        
        for movie in movies_in_cart:
            movie_data.append({
                'movie': movie,
                'quantity': cart[str(movie.id)]
            })

    template_data = {
        'title': 'Cart',
        'movie_data': movie_data,
        'cart_total': cart_total,
    }
    return render(request, 'cart/index.html', {'template_data': template_data})

def add(request, id):
    get_object_or_404(Movie, id=id)

    if request.method == 'POST':
        cart = request.session.get('cart', {})
        qty = request.POST.get('quantity', '1')
        cart[str(id)] = qty
        request.session['cart'] = cart
    return redirect('cart.index')

def clear(request):
    request.session['cart'] = {}
    return redirect('cart.index')

@login_required
def purchase(request):
    cart = request.session.get('cart', {})
    movie_ids = list(cart.keys())
    if movie_ids == []:
        return redirect('cart.index')

    movies_in_cart = Movie.objects.filter(id__in=movie_ids)
    cart_total = calculate_cart_total(cart, movies_in_cart)

    order = Order(user=request.user, total=cart_total)
    order.save()

    for movie in movies_in_cart:
        Item.objects.create(
            movie=movie,
            price=movie.price,
            order=order,
            quantity=cart[str(movie.id)]
        )

    request.session['cart'] = {}
    template_data = {'title': 'Purchase confirmation', 'order_id': order.id}
    return render(request, 'cart/purchase.html', {'template_data': template_data})