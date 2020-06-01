from django.urls import path
from . import views

urlpatterns = [
    path('pdf_view/', views.ViewPDF.as_view(), name="pdf_view"),
    path('downloads/', views.DownloadPDF.as_view(), name='pdf_download'),
    path('recipes/<int:amount>', views.recipe_list),
    path('recipe_gen', views.index),
    path('', views.home),
]
