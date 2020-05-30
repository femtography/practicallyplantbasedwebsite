from django.urls import path
from . import views

urlpatterns = [
    path('recipes/<int:amount>', views.recipe_list),
    path('recipe_gen', views.index),
    path('', views.home),
]
