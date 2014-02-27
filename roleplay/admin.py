# -*- coding: utf-8 -*-

from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.db import models
from django import forms
from django.contrib.auth.models import User

from models import *




class EventAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ('name', 'slug')
    search_fields = ['name',]


class LocationAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['name', 'slug']}),
        ('Описание', {'fields': ['description'], 'classes': ['collapse']}),
    ]


    prepopulated_fields = {"slug": ("name",)}
    list_display = ('name', 'slug')
    search_fields = ['name',]


'''
class ImageFileInline(admin.TabularInline):
    model = ImageFile
    extra = 5
'''








class GameLocationsInline(admin.TabularInline):
    model = GameLocations
    #form = ''
    extra = 1



class GameForm(forms.ModelForm):

    class Meta:
        model = Game
        



class GameAdmin(admin.ModelAdmin):
    #form = GameForm
    
    fieldsets = [
        #('Локация', {'fields': ['location']}),
        #('Карта', {'fields': ['map']}),
        
        (None,               {'fields': ['name', 'slug', 'date']}),
        ('Описание', {'fields': ['description'], 'classes': ['collapse']}),
    ]
    
    list_filter = ('date', 'locations__name' )

    
    inlines = [GameLocationsInline]
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ['name', 'locations__name']      #, 'event__name'
    list_display = ('name', 'slug', 'date', 'imagefile_count')  #, 'locations__name',

    



class CharAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ['name'] 
    


class UserAdmin(admin.ModelAdmin):
    model = User
    fieldsets = [
        (None,               {'fields': ['last_name', 'first_name']}),
        (None,               {'fields': ['username', 'email']}),

    ]
    prepopulated_fields = {"username": ("last_name",)}
    list_display = ('username', 'first_name', 'last_name', 'is_active')
    
    
    def save_model(self, request, obj, form, change):
        obj.is_active = False
        obj.save()






class GameListFilter(SimpleListFilter):
    title = ('Игра')
    parameter_name = 'game'

    def lookups(self, request, model_admin):
        return [(i.id, i.name) for i in Game.objects.all()]

    def queryset(self, request, queryset):
        return queryset


class LocationListFilter(SimpleListFilter):
    title = ('Локация')
    parameter_name = 'location'

    def lookups(self, request, model_admin):
        game_id = request.GET.get("game", 0)
        if game_id:
            g = Game.objects.get(id=game_id)
            return [(i.id, i.name) for i in g.locations.all()]
        
        return [(i.id, i.name) for i in Location.objects.all()]

    def queryset(self, request, queryset):
        location_id = request.GET.get("location", 0)
        if location_id:
            queryset = queryset.filter(location_id=location_id)
        
        return queryset


class EventListFilter(SimpleListFilter):
    title = ('События')
    parameter_name = 'event'
    
    def lookups(self, request, model_admin):
        game_id = request.GET.get("game", 0)
        location_id = request.GET.get("location", 0)
        if game_id and location_id:
            gl = GameLocations.objects.get(game_id=game_id, location_id=location_id)
            return [(i.id, i.name) for i in gl.events.all()]
            
        return [(i.id, i.name) for i in Event.objects.all()]

    def queryset(self, request, queryset):
        event_id = request.GET.get("event", 0)
        if event_id:
            queryset = queryset.filter(event_id=event_id)
        
        return queryset



class ImageFileAdmin(admin.ModelAdmin):
    list_display = ('image', 'game', 'location', 'event', 'exif_date', 'add_date')
    readonly_fields = ('exif_date', 'width', 'height', 'add_date')

    list_filter = (GameListFilter, LocationListFilter, EventListFilter, 'exif_date', 'add_date')
    search_fields = ['image']
    
    

    '''
    def save_model(self, request, obj, form, change):
        print "ImageFileAdmin save:"
        #obj.user = request.user
        obj.save()
    def save(self, *args, **kwargs):
        super(ImageFileAdmin, self).save(*args, **kwargs)
    '''






admin.site.register(Game, GameAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Event, EventAdmin)

admin.site.register(Char, CharAdmin)

admin.site.register(ImageFile, ImageFileAdmin)


#admin.site.unregister(User)
#admin.site.register(User, UserAdmin)

























