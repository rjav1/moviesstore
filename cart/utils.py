def calculate_cart_total(cart, movies_in_cart):
    total = 0
    for movie in movies_in_cart:
        quantity = int(cart[str(movie.id)])
        total += movie.price * quantity
    return total 