from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model 

# Custom User Model
class CustomUser(AbstractUser):
    picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)  # Photo de profil
    nom = models.CharField(max_length=100)  # Nom de l'utilisateur
    adresse = models.CharField(max_length=255, blank=True, null=True)  # Adresse de l'utilisateur

    # Add related_name to prevent clashes
    groups = models.ManyToManyField(
        'auth.Group', related_name='customuser_groups', blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission', related_name='customuser_permissions', blank=True
    )

    def __str__(self):
        return self.username

    def inscrire(self):
        #INSCRIRE function
        pass

    def seconnecter(self):
        # Fonction de connexion
        pass

    def modifierprofile(self):
        # Fonction de modification de profil
        pass

    def ajouteraupanier(self, livre):
        # Fonction d'ajout au panier
        pass

    def consulterlivre(self, livre):
        # Fonction de consultation de livre
        pass

    def passercommande(self, panier):
        # Fonction de passer commande
        pass


class Author(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100, blank=True, null=True)  # nullable
    datenaissance = models.DateField(blank=True, null=True)
    origine = models.CharField(max_length=100, blank=True, null=True)  # nullable
    biographie = models.TextField(blank=True, default='N/A')

    def __str__(self):
        return f"{self.nom} {self.prenom}".strip()

    def afficherInfoAuteur(self):
        # Fonction pour afficher les informations de l'auteur
        pass


class Category(models.Model):
    nom = models.CharField(max_length=100)

    def __str__(self):
        return self.nom


class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='livres')
    genre = models.CharField(max_length=50)
    prix = models.DecimalField(max_digits=5, decimal_places=2)
    description = models.TextField()
    note = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])  # Validateurs ajoutés
    categorie = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='livres')
    cover_image = models.URLField(max_length=200, blank=True, null=True, default='https://placehold.co/600x400/EEE/31343C')

    def __str__(self):
        return self.title

    def ConsulterDetails(self):
        # Fonction de consultation des détails du livre
        pass

    def AjouterCommentaire(self, utilisateur, texte):
        Review.objects.create(utilisateur=utilisateur, livre=self, texte=texte)


class Commande(models.Model):
    utilisateur = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='commandes')
    DateCommande = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20)
    Livres = models.ManyToManyField(Book, related_name='commandes')

    def Afficherdetails(self):
        # Fonction pour afficher les détails de la commande
        pass

    def AnnulerCommande(self):
        # Fonction pour annuler la commande
        pass


class Panier(models.Model):
    utilisateur = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='panier')
    livres = models.ManyToManyField(Book, related_name='paniers')

    def AjouterLivre(self, livre):
        self.livres.add(livre)

    def SupprimerLivre(self, livre):
        self.livres.remove(livre)

    def ValiderCommande(self):
        # Fonction de validation de la commande
        pass


class Review(models.Model):
    utilisateur = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    livre = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='commentaires')
    texte = models.TextField()
    rating = models.PositiveIntegerField(
        choices=[(i, f'{i} ★') for i in range(1, 6)]
    )
    date = models.DateTimeField(auto_now_add=True)

    def AfficherCommentaire(self):
        # Fonction d'affichage du commentaire
        pass
