# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
#from django.forms import ModelForm, Textarea, CharField, Select
from django.shortcuts import render, render_to_response, get_object_or_404, get_list_or_404
#from django.template import RequestContext, Context
from django.views import generic
#from django.forms.models import inlineformset_factory
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from settings import THUMBS_PER_PAGE

from roleplay.models import *
from roleplay import settings



def test(request):
    return HttpResponse("Hello, world. You're at the poll index.")
    
    
    
    
class GameIndexView(generic.ListView):
    #model = Game
    #template_name = 'roleplay/game_list.html'
    queryset = Game.objects.order_by('-date')
    paginate_by = settings.GAMES_PER_PAGE
    '''
    def get_context_data(self, **kwargs):
        context = super(GameIndexView, self).get_context_data(**kwargs)
        return context
    '''

class GameView(generic.DetailView):
    model = Game
    #template_name = 'roleplay/game_detail.html'
    slug_url_kwarg = "game_slug"

    def get_object(self):
        return get_object_or_404(Game, slug=self.kwargs["game_slug"])


    
    
    
    
def gl_detail(request, game_slug, location_slug):
    game = get_object_or_404(Game, slug=game_slug)
    location = get_object_or_404(Location, slug=location_slug)
    
    gl = get_object_or_404(GameLocations, game=game, location=location)
    
    context = {"game": game, "location": location, "gl": gl}
    return render(request, 'roleplay/gl_detail.html', context)

'''
# Делает тоже, что и функция выше, но Class-Based,
# вообщем читается хуже
class GameLocation(generic.DetailView):
    #model = GameLocations
    template_name = 'roleplay/gl_detail.html'
        
    def get_object(self):
        self.game = get_object_or_404(Game, slug = self.kwargs["game_slug"])
        self.location = get_object_or_404(Location, slug = self.kwargs["location_slug"])
        return get_object_or_404(GameLocations, game=self.game, location=self.location)

    def get_context_data(self, **kwargs):
        context = super(GameLocation, self).get_context_data(**kwargs)
        context["game"] = self.game
        context["location"] = self.location
        context["gl"] = self.object
        return context
    
'''   
    
def gle_detail(request, game_slug, location_slug, event_slug):
    game = get_object_or_404(Game, slug=game_slug)
    location = get_object_or_404(Location, slug=location_slug)
    event = get_object_or_404(Event, slug=event_slug)
    
    gl = get_object_or_404(GameLocations, game=game, location=location)
    gle = get_object_or_404(GameLocationsEvents, game_location=gl, event=event)

    #chars = GameLocationsEventsChars.objects.filter(game_location_event=gle)
    "По умолчанию сортируем по Дате снимка - exif_date"
    order = request.GET.get("order", 'exif_date')
    
    order_list = [
                  {"field": "exif_date", "verbose_name": "Дате снимка"},
                  {"field": "add_date", "verbose_name": "Дате добавления"},
                  {"field": "image", "verbose_name": "Имени файла"},
                  ]
    
   
    images = ImageFile.objects.filter(game=game,
                                      location=location,
                                      event=event,
                                      ).order_by(order)
    

    paginator = Paginator(images, THUMBS_PER_PAGE) # Show limit items per page
    page = request.GET.get("page", 1)

    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        images = paginator.page(1)
        page = 1
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        images = paginator.page(paginator.num_pages)
        page = paginator.num_pages

    page_obj = paginator.page(page)
    
    query_string = ""
    if request.GET.has_key("order"):
        query_string = "order=" + request.GET["order"] + "&"

    
    context = {"game": game,
               "location": location,
               "event": event,
               "gl": gl,
               "gle": gle,
               #"chars": chars,
               "order": order,
               "order_list": order_list,
               "images": images,
               "paginator": paginator,
               "page_obj": page_obj,
               "query_string": query_string,
               }
    return render(request, 'roleplay/gle_detail.html', context)
    
    
    
def gle_chars(request, game_slug, location_slug, event_slug):
    game = get_object_or_404(Game, slug=game_slug)
    location = get_object_or_404(Location, slug=location_slug)
    event = get_object_or_404(Event, slug=event_slug)
    
    gl = get_object_or_404(GameLocations, game=game, location=location)
    gle = get_object_or_404(GameLocationsEvents, game_location=gl, event=event)
    
    chars = GameLocationsEventsChars.objects.filter(game_location_event=gle)
    images = ImageFile.objects.filter(game=game,
                                      location=location,
                                      event=event)
    
    context = {"game": game,
               "location": location,
               "event": event,
               "gl": gl,
               "gle": gle,
               "chars": chars,
               }
    
    
    return render(request, 'roleplay/gle_chars.html', context)
    
    

    
    
    