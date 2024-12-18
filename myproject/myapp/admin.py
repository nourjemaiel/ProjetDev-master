from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Author, Book, Category, Review, Commande, CustomUser, Panier

# Enregistrez CustomUser comme utilisateur
admin.site.register(CustomUser, UserAdmin)

# Enregistrez les autres modèles
admin.site.register(Author)
admin.site.register(Book)
admin.site.register(Category)
admin.site.register(Review)
admin.site.register(Commande)
admin.site.register(Panier)


# Register your models here.
