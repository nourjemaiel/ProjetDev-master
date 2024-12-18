from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib import messages
import requests
from .models import Author, Book, Review, Category, Commande, CustomUser  # Replaced Utilisateur with CustomUser
from .forms import ReviewForm, SignUpForm, LoginForm

from django.http import HttpResponseForbidden


# Home Page View
def home(request):
    trending_books = Book.objects.all()[:5]  # Récupère les 5 premiers livres
    books_data = fetch_books_from_api()  # Appelle la fonction pour récupérer les livres de l'API
    print(books_data)  # Affiche les données dans la console

    return render(request, 'home.html', {'trending_books': trending_books, 'books_data': books_data})

def about_us(request):
    return render(request, 'about-us.html')

def fetch_books_from_api():
    api_url = 'https://www.googleapis.com/books/v1/volumes?q=python+programming'
    response = requests.get(api_url)

    if response.status_code == 200:
        data = response.json()
        books = data.get('items', [])

        print(books)  # Debug: Print fetched books

        for book_data in books:
            volume_info = book_data.get('volumeInfo', {})
            authors = volume_info.get('authors', ['Auteur inconnu'])
            author_name = ', '.join(authors) if authors != ['Auteur inconnu'] else 'Auteur inconnu'

            prenom = ''
            nom = author_name if author_name != 'Auteur inconnu' else 'Nom inconnu'

            # Get or create the author
            author, created = Author.objects.get_or_create(
                nom=nom,
                defaults={
                    'prenom': prenom,
                    'datenaissance': None,
                    'origine': '',
                    'biographie': 'N/A',
                }
            )

            # Fetch other book details
            title = volume_info.get('title', 'Titre inconnu')
            description = volume_info.get('description', 'Pas de description')
            cover_image_url = volume_info.get('imageLinks', {}).get('thumbnail', '')
            genre = ', '.join(volume_info.get('categories', ['Genre inconnu']))

            # Get or create the category
            category, created = Category.objects.get_or_create(nom=genre)

            # Create or update the book
            book, created = Book.objects.update_or_create(
                title=title,
                author=author,
                defaults={
                    'genre': genre,
                    'prix': 0.00,
                    'description': description,
                    'note': 0,
                    'categorie': category,
                    'cover_image': cover_image_url,
                }
            )

            if created:
                print(f"Book '{title}' created.")
            else:
                print(f"Book '{title}' updated.")

        return books

    else:
        print("Erreur de récupération des données :", response.status_code)
        return []


# Book List View
def book_list(request):
    # Récupère tous les livres
    books = Book.objects.all()

    # Recherche par titre
    query = request.GET.get('q', '')
    if query:
        books = books.filter(titre__icontains=query)

    # Filtre par auteur
    auteur_id = request.GET.get('auteur')
    if auteur_id:
        books = books.filter(auteur_id=auteur_id)

    # Filtre par genre
    genre = request.GET.get('genre')
    if genre:
        books = books.filter(genre__icontains=genre)

    # Filtre par catégorie
    categorie_id = request.GET.get('categorie')
    if categorie_id:
        books = books.filter(categorie_id=categorie_id)

    # Données pour les filtres
    auteurs = Author.objects.all()
    categories = Category.objects.all()

    return render(request, 'book_list.html', {
        'books': books,
        'auteurs': auteurs,
        'categories': categories,
        'query': query,
    })

# Book Detail View
def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    reviews = Review.objects.filter(livre=book)
    full_stars = range(book.note)  # Number of full stars based on the rating
    empty_stars = range(5 - book.note)  # Number of empty stars based on the rating
    return render(request, 'book_detail.html', {'book': book, 'reviews': reviews, 'full_stars': full_stars, 'empty_stars': empty_stars})

# Author Detail View
def author_detail(request, author_id):
    author = get_object_or_404(Author, id=author_id)
    books_by_author = Book.objects.filter(author=author)
    return render(request, 'author_detail.html', {'author': author, 'books': books_by_author})

# Create a Review View
@login_required
def create_review(request, book_id):
    if not request.user.is_authenticated:
        return HttpResponseForbidden("Vous devez être connecté pour laisser un commentaire.")
    
    book = get_object_or_404(Book, pk=book_id)
    
    if request.method == 'POST':
        texte = request.POST['texte']
        rating = int(request.POST['rating'])

        # Créez la revue en associant l'utilisateur connecté
        review = Review.objects.create(
            livre=book,
            utilisateur=request.user,  # L'utilisateur connecté
            texte=texte,
            rating=rating
        )
        review.save()

        return redirect('book_detail', book_id=book.id)  # Redirige après avoir ajouté la revue

    return render(request, 'book_detail.html', {'book': book})


# Signup view
def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

# Login view
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Login successful!')
                return redirect('book_list')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})
