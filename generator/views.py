from django.shortcuts import render
from .models import Recipe
import random
import io
from io import BytesIO
from django.http import HttpResponse, FileResponse
from django.views import View
from reportlab.pdfgen import canvas
from django.core.mail import send_mail
from django.conf import settings


# Create your views here.
def index(request):
    return render(request, 'generator/index.html')

def home(request):
    if request.method == "POST":
        message = request.POST['message', 'name', 'email']
        send_mail(name + " is reaching out from" + email, message, settings.EMAIL_HOST_USER, ['practicallyplantpowered@gmail.com'], fail_silently=FALSE)
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

def g_list_to_pdf( pdf, item_dict={}):
    pdf.setFont('Helvetica', 36)
    x = 50
    y = 750
    pdf.drawString(50, y, "Your Grocery List")
    y = y - 40

    for key in item_dict.keys():
        x = 50
        if y < 50:
            pdf.showPage()
            y = 800
        pdf.setFont('Helvetica', 18)
        if key == 'oils_li':
            if y < 250:
                pdf.showPage()
                y = 800
                pdf.setFont('Helvetica', 18)
            y = y - 20
            pdf.drawString(x, y, "This is assuming that you have the following Oils/Sauces:")
            y = y - 30
        elif key == 'seasons_li':
            if y < 250:
                pdf.showPage()
                y = 800
                pdf.setFont('Helvetica', 18)
            y = y - 20
            pdf.drawString(x, y, "This is assuming that you have the following Seasonings:")
            y = y - 30

        pdf.setFont('Helvetica', 12)
        for value in item_dict[key]:
            if len(value) > 2:
                pdf.drawString(x, y, value)
                y = y - 20

    pdf.showPage()
    y = 800

def recipes_to_pdf(y_val, pdf, recipes={}):
    x = 50
    y = y_val
    for r in recipes:
        pdf.setFont('Helvetica', 30)
        y = y - 30
        pdf.drawString(x, y, r.name)
        y = y - 50
        obj_options = [r.main, r.seasoning, r.oils]
        for i, t in enumerate(["Main Ingredients:", "Seasonings:", "Oils/Sauces:"]):
            obj_op = obj_options[i]
            pdf.setFont('Helvetica', 20)
            pdf.drawString(x, y, t)
            y = y - 30
            pdf.setFont('Helvetica', 12)
            for item in [x.replace(',', '') for x in obj_op.split('\r\n')]:
                pdf.drawString(x, y, item)
                y = y - 20
            y = y - 20

        pdf.setFont('Helvetica', 20)
        pdf.drawString(x, y, "Instructions:")
        y = y - 30
        pdf.setFont('Helvetica', 12)
        for item in [x.replace(',', '') for x in r.preparation.split('\r\n')]:
            item_split = item.split('. ')
            for i in item_split:
                i_list = [x for x in i.split(' ')]
                if len(i_list) <= 14:
                    if "." not in i:
                        pdf.drawString(x, y, i + '.')
                    y = y - 20
                elif len(i_list) > 14 and len(i_list) <= 28:
                    s = 0
                    t = len(i_list)//2
                    u = len(i_list)
                    a = i_list[s:t]
                    b = i_list[t:u]
                    if "." not in i:
                        b[-1] = b[-1]+'.'
                    pdf.drawString(x, y, " ".join(a))
                    y = y - 20
                    pdf.drawString(x, y, " ".join(b))
                    y = y - 20
                elif len(i_list) > 28:
                    s = 0
                    t = len(i_list)//3
                    u = t*2
                    r = len(i_list)
                    a = i_list[s:t]
                    b = i_list[t:u]
                    c = i_list[u:r]
                    if "." not in i:
                        c[-1] = c[-1]+'.'
                    pdf.drawString(x, y, " ".join(a))
                    y = y - 20
                    pdf.drawString(x, y, " ".join(b))
                    y = y - 20
                    pdf.drawString(x, y, " ".join(c))
                    y = y - 20
        y = y - 20

        pdf.showPage()
        y = 800

def pdf_gen(item_dict={}, recipes={}):
    pdfl = io.BytesIO()
    pdf_doc = canvas.Canvas(pdfl)
    pdf_doc.setTitle("MyRecipe(s).pdf")
    y = 800

    g_list_to_pdf(pdf_doc, item_dict)
    recipes_to_pdf(y, pdf_doc, recipes)

    pdf_doc.save()

    pdfl.seek(0)
    return pdfl

class ViewPDF(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse(pdf_gen(pdf_ing, r_list), content_type='application/pdf')

class DownloadPDF(View):
    def get(self, request, *args, **kwargs):
        return FileResponse(pdf_gen(pdf_ing, r_list), as_attachment=True, filename='MyRecipe(s).pdf')
