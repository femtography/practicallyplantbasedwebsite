from django.shortcuts import render
from .models import Recipe
import random
import io
from io import BytesIO
from django.http import HttpResponse, FileResponse
from django.template.loader import get_template
from django.views import View
from xhtml2pdf import pisa
from reportlab.pdfgen import canvas

# Create your views here.
def index(request):
    return render(request, 'generator/index.html')

def home(request):
    return render(request, 'generator/home.html')

def recipe_list(request, amount):
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

def pdf_gen(item_dict={}):
    buffer = io.BytesIO()
    pdfl = canvas.Canvas(buffer)

    x = 50
    y = 750
    pdfl.drawString(x, y, "Your Grocery List:")
    y = y - 30

    for key in item_dict.keys():
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
    pdfl.save()

    buffer.seek(0)
    return buffer

class ViewPDF(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse(pdf_gen(pdf_ing), content_type='application/pdf')

class DownloadPDF(View):
    def get(self, request, *args, **kwargs):
        return FileResponse(pdf_gen(pdf_ing), as_attachment=True, filename='MyRecipe(s).pdf')
