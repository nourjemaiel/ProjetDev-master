from django.urls import path
from . import views
from django.contrib.auth import views as auth_views 

urlpatterns = [
    path('', views.home, name='home'),
    path('about-us/', views.about_us, name='about_us'),
    path('books/', views.book_list, name='book_list'),  
    path('books/<int:book_id>/', views.book_detail, name='book_detail'),  
    path('authors/<int:author_id>/', views.author_detail, name='author_detail'),  
    path('books/<int:book_id>/review/', views.create_review, name='create_review'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    #path('posts/', views.post_list, name='post_list'),
    #path('posts/<int:post_id>/', views.post_detail, name='post_detail'),
    #path('posts/create/', views.create_post, name='create_post'),
]