from django.shortcuts import render
from .models import Recipe
import random
import io
from io import BytesIO
from django.http import HttpResponse, FileResponse
from django.views import View
from reportlab.pdfgen import canvas

# Create your views here.
def index(request):
    return render(request, 'generator/index.html')

def home(request):
    return render(request, 'generator/home.html')

def recipe_list(request, amount):
    global r_list

    m_list = Recipe.objects.all()
    r_list = random.sample(list(m_list), amount)
    main_i = []
    oils_i = []
    seasoning_i =[]
    bg_i = random.sample([2, 5, 10, 11, 12, 15], 1)

    for r in r_list:
        main_i = main_i + [x.replace(',', '') for x in r.main.split('\r\n') if x.replace(',', '') not in main_i ]
        oils_i = oils_i + [x.replace(',', '') for x in r.oils.split('\r\n')if x.replace(',', '') not in oils_i ]
        seasoning_i = seasoning_i + [x.replace(',', '') for x in r.seasoning.split('\r\n') if x.replace(',', '') not in seasoning_i ]

    global pdf_ing
    pdf_ing = {'ing_li': main_i, 'oils_li': oils_i, 'seasons_li': seasoning_i}

    args = {"recipes": r_list, 'ing_li': main_i, 'oils_li': oils_i, 'seasons_li': seasoning_i, 'bg_pic': bg_i[0]}


    return render(request, 'generator/recipe_page.html', args)

def pdf_gen(item_dict={}, recipes={}):
    buffer = io.BytesIO()
    pdfl = canvas.Canvas(buffer)

    x = 50
    y = 750
    pdfl.drawString(x, y, "Your Grocery List:")
    y = y - 30

    for key in item_dict.keys():
        if y < 50:
            pdfl.showPage()
            y = 800
        if key == 'oils_li':
            y = y - 20
            pdfl.drawString(x, y, "This is assuming that you have the following Oils/Sauces:")
            y = y - 30
        elif key == 'seasons_li':
            y = y - 20
            pdfl.drawString(x, y, "This is assuming that you have the following Seasonings:")
            y = y - 30

        for value in item_dict[key]:
            pdfl.drawString(x, y, value)
            y = y - 20

    pdfl.showPage()
    y = 800

    y = y - 30
    pdfl.drawString(x, y, "Recipes:")
    y = y - 30

    for r in recipes:
        y = y - 30
        pdfl.drawString(x, y, r.name)
        y = y - 40
        pdfl.drawString(x, y, "Main Ingredients:")
        y = y - 30
        for item in [x.replace(',', '') for x in r.main.split('\r\n')]:
            pdfl.drawString(x, y, item)
            y = y - 20
        y = y - 20
        pdfl.drawString(x, y, "Seasonings:")
        y = y - 30
        for item in [x.replace(',', '') for x in r.seasoning.split('\r\n')]:
            pdfl.drawString(x, y, item)
            y = y - 20
        y = y - 20
        pdfl.drawString(x, y, "Oils/Sauces:")
        y = y - 30
        for item in [x.replace(',', '') for x in r.oils.split('\r\n')]:
            pdfl.drawString(x, y, item)
            y = y - 20
        y = y - 20
        pdfl.drawString(x, y, "Instructions:")
        y = y - 30
        for item in [x.replace(',', '') for x in r.preparation.split('\r\n')]:
            pdfl.drawString(x, y, item)
            y = y - 20
        y = y - 20

        pdfl.showPage()
        y = 800

    pdfl.save()

    buffer.seek(0)
    return buffer

class ViewPDF(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse(pdf_gen(pdf_ing, r_list), content_type='application/pdf')

class DownloadPDF(View):
    def get(self, request, *args, **kwargs):
        return FileResponse(pdf_gen(pdf_ing, r_list), as_attachment=True, filename='MyRecipe(s).pdf')
