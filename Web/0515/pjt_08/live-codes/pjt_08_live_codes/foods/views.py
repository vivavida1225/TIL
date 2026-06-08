from django.shortcuts import render, redirect
from .models import Recipe
from .forms import RecipeForm

# Create your views here.


def index(request):
    recipes = Recipe.objects.all()
    context = {
        'recipes': recipes,
    }
    return render(request, 'foods/index.html', context)


def create(request):
    if request.method == 'POST':
        recipe_form = RecipeForm(request.POST)

        if recipe_form.is_valid():
            recipe_form.save()
            return redirect('foods:index')
    else:
        recipe_form = RecipeForm()
    context = {
        'recipe_form': recipe_form,
    }
    return render(request, 'foods/create.html', context)
