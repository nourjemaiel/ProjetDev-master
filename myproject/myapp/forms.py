from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Review

# Sign Up Form for creating a new user
class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)
    profile_image = forms.ImageField(required=False)

    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'profile_image']

    def save(self, commit=True):
        user = super().save(commit=False)
        # Save additional fields
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.picture = self.cleaned_data.get('profile_image')
        user.set_password(self.cleaned_data["password1"])

        if commit:
            user.save()
        return user


# Login Form for user authentication
class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, required=True, label="Username")
    password = forms.CharField(widget=forms.PasswordInput, required=True, label="Password")


# Review Form for submitting book reviews
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'texte']   # Fields for the review (book, text, and rating)
