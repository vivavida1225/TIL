from django.shortcuts import render
from django.views.decorators.http import require_safe


# Create your views here.
@require_safe
def index(request):
    pass


def filter_genre(request):
    pass


@require_safe
def recommended(request):
    pass
