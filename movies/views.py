from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Movie, Review

def index(request):
    search_term = request.GET.get('search')
    if search_term:
        movies = Movie.objects.filter(name__icontains=search_term)
    else:
        movies = Movie.objects.all()

    template_data = {
        'title': 'Movies',
        'movies': movies
    }
    return render(request, 'movies/index.html', {'template_data': template_data})

def show(request, id):
    movie = get_object_or_404(Movie, id=id)
    reviews = Review.objects.filter(movie=movie).order_by('-date')
    template_data = {
        'title': movie.name,
        'movie': movie,
        'reviews': reviews
    }
    return render(request, 'movies/show.html', {'template_data': template_data})

@login_required
def create_review(request, id):
    if request.method == 'POST' and request.POST.get('comment', '').strip():
        movie = get_object_or_404(Movie, id=id)
        Review.objects.create(
            comment=request.POST['comment'].strip(),
            movie=movie,
            user=request.user
        )
    return redirect('movies.show', id=id)

@login_required
def edit_review(request, id, review_id):
    review = get_object_or_404(Review, id=review_id)
    if request.user != review.user:
        return redirect('movies.show', id=id)

    if request.method == 'GET':
        template_data = {
            'title': 'Edit Review',
            'review': review
        }
        return render(request, 'movies/edit_review.html', {'template_data': template_data})

    new_comment = request.POST.get('comment', '').strip()
    if new_comment:
        review.comment = new_comment
        review.save()
    return redirect('movies.show', id=id)

@login_required
def delete_review(request, id, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    review.delete()
    return redirect('movies.show', id=id)
