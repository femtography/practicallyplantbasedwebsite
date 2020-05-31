from django.shortcuts import render
from .models import Recipe
import random

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

    args = {"recipes": r_list, 'ing_li': main_i, 'oils_li': oils_i, 'seasons_li': seasoning_i, 'bg_pic': bg_i[0]}


    return render(request, 'generator/recipe_page.html', args)
