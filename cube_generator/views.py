from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
from cube_generator.models import Card
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect

# Create your views here.


class GetCard(ListView):
    model = Card
