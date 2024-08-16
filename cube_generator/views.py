from django.shortcuts import render
from django.views.generic import ListView
from cube_generator.models import Card

# Create your views here.


class GetCard(ListView):
    model = Card
