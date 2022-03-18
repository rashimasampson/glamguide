from django.urls import path
from . import views


urlpatterns = [
    path('', views.index),
    path('register',views.register),
    path('login', views.login),
    path('wishes', views.wishes),
    path('wishes/new', views.new_wish),
    path('wishes/create/<int:user_id>', views.create_wish),
    path('like/<int:user_id>', views.add_like),
    path('wishes/edit/<int:wish_id>', views.edit),
    path('wishes/<int:wish_id>/delete', views.delete),
    path('wishes/update/<int:wish_id>', views.update),
    path("wishes/<int:wish_id>", views.show_one),
    path('logout', views.logout),
]
