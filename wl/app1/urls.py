from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path("add-wish/", views.add_wish, name="add_wish"),
    path("wishes/", views.wish_list, name="wish_list"),
    path('public-wishes/', views.public_wishes, name='public_wish_list'),
    path('wish/<int:wish_id>/edit/', views.edit_wish, name='edit_wish'),
    path('wish/<int:wish_id>/delete/', views.delete_wish, name='delete_wish'),
    path('wish/<int:wish_id>/comment/', views.add_comment, name='add_comment'),
]