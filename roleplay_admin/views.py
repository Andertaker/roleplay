# -*- coding: utf-8 -*-
import json

from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
#from django.forms import ModelForm, Textarea, CharField, Select
from django.shortcuts import render, render_to_response, get_object_or_404, get_list_or_404
#from django.template import RequestContext, Context
from django.views import generic
#from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.forms.models import inlineformset_factory
#from django.forms.models import BaseModelFormSet, BaseInlineFormSet
from django.core.exceptions import ValidationError, NON_FIELD_ERRORS
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from roleplay.models import *
from roleplay import settings


  

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name')
        widgets = {
            'username': forms.TextInput(attrs={'required': "required", "size": 40}),
            'first_name': forms.TextInput(attrs={'required': "required", "size": 40}),
            'last_name': forms.TextInput(attrs={'required': "required", "size": 40}),
            #'description': forms.Textarea(attrs={'cols': 60, 'rows': 2}),
            #'locations': forms.Select(attrs={'size': 15, 'multiple': 'multiple'}),
        }
    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        cleaned_data["username"] = cleaned_data["username"].strip()
        cleaned_data["first_name"] = cleaned_data["first_name"].strip()
        cleaned_data["last_name"] = cleaned_data["last_name"].strip()
        
        return cleaned_data
    
    
class UserIndexView(generic.ListView):
    model = User
    queryset = User.objects.filter(is_superuser=False)
    paginate_by = settings.USERS_PER_PAGE
    
    
class UserView(generic.DetailView):
    model = User
    context_object_name = "u"
    #template_name = 'roleplay_admin/user_detail.html'
    
class UserAddView(generic.CreateView):
    model = User
    form_class = UserForm
    #template_name = 'roleplay_admin/user_form.html'
    
    def form_valid(self, form):
        u = form.save()
        return HttpResponseRedirect(reverse('rp_admin:user_detail', kwargs={"pk": u.id}))

    
class UserEditView(generic.UpdateView):
    model = User
    form_class = UserForm
    #template_name = 'roleplay_admin/user_form.html'
    context_object_name = "u"

    '''
    def get_object(self):
        return get_object_or_404(User, pk=self.kwargs["pk"])
    '''      
    def form_valid(self, form):
        u = form.save()
        return HttpResponseRedirect(reverse('rp_admin:user_detail', kwargs={"pk": u.id}))
        "показываем ту же страницу"
        context = self.get_context_data()
        context["form"] = form
        return self.render_to_response(context)
    
    
class GameIndexView(generic.ListView):
    model = Game
    template_name = 'roleplay_admin/game_list.html'
    #queryset = Game.objects.order_by('-date')[:20]
    paginate_by = settings.GAMES_PER_PAGE




class GameView(generic.DetailView):
    model = Game
    template_name = 'roleplay_admin/game_detail.html'
    context_object_name = "game"

    def get_object(self):
        return get_object_or_404(Game, pk=self.kwargs["pk"])

    
    
    
class GameForm(forms.ModelForm):
    class Meta:
        model = Game
        exclude = ('locations', )   #для локаций используем формсет
        widgets = {
            'name': forms.TextInput(attrs={'required': "required", "size": 60}),
            'slug': forms.TextInput(attrs={'required': "required", "size": 30}),
            'date': forms.DateInput(attrs={'required': "required","class":"datepicker"}),
            'description': forms.Textarea(attrs={'cols': 60, 'rows': 2}),
            #'locations': forms.Select(attrs={'size': 15, 'multiple': 'multiple'}),
        }
    


class GameLocationsForm(forms.ModelForm):
    class Meta:
        model = GameLocations
        fields = ["location"]

GameLocationsFormSet = inlineformset_factory(Game, GameLocations,
                                             form=GameLocationsForm)


def game_add(request):
  
    if request.method == "POST":
        form = GameForm(request.POST)
        formset = GameLocationsFormSet(request.POST)
        
        if form.is_valid():
            game = form.save()

            "Сохраняем локации, если есть дубли они не сохранятся"
            formset = GameLocationsFormSet(request.POST, instance=game)
            if formset.is_valid():
                formset.save()
            '''    
            else:
                #print formset.errors    #какая-то локация выбрана дважды
                instances = formset.save(commit=False)
                for instance in instances:
                    try:
                        instance.validate_unique()
    
                    except ValidationError as e:
                        non_field_errors = e.message_dict[NON_FIELD_ERRORS]
                    else:
                        instance.save()
            '''
            
            
            return HttpResponseRedirect(reverse('rp_admin:game_detail', kwargs={"pk": game.id}))
        else:   #показываем ошибки
            pass
    
    else:
        form = GameForm()
        formset = GameLocationsFormSet()

    
    context = {"form": form, "formset": formset}
    return render(request, 'roleplay_admin/game_add.html', context)
    
    
    
    
    
def game_edit(request, pk):
    game = get_object_or_404(Game, pk=pk)
            
    if request.method == "POST":
        form = GameForm(request.POST, instance=game)

        if form.is_valid():
            game = form.save(commit=False)
            game.save()
           
        #else:
            #print form.errors
            #return render(request, "roleplay_admin/errors.html", {"errors": form.errors})
            #return HttpResponse( str(form.errors) )
            
        "Сохраняем локации, если есть дубли они не сохранятся"
        formset = GameLocationsFormSet(request.POST, instance=game)
        if formset.is_valid():
            instances = formset.save()  #commit=False
             
        if form.is_valid():
            return HttpResponseRedirect(reverse('rp_admin:game_detail', kwargs={"pk": game.id}))      

    else:
        form = GameForm(instance=game)
    
    
    formset = GameLocationsFormSet(instance=game)

    context = {"form": form, "game": game, "formset": formset}
    return render(request, 'roleplay_admin/game_edit.html', context)
    
    
    
    
GameLocEventsFormSet = inlineformset_factory(
                             GameLocations, GameLocationsEvents,
                             extra=3,
                             exclude=("game_location", "chars", "users"),
                             #can_order=True
                            )
    
    
    
def gl_edit(request, game_id, pk):
    gl = get_object_or_404(GameLocations, pk=pk)
    
    if request.method == "POST":
        formset = GameLocEventsFormSet(request.POST, instance=gl)
        
        if formset.is_valid():
            if formset.has_changed():
        
                instances = formset.save(commit=False)
                for instance in instances:
                    try:
                        instance.validate_unique()
                    except ValidationError as e:
                        non_field_errors = e.message_dict[NON_FIELD_ERRORS]
                    else:
                        instance.save()
                    
        elif formset.errors:
            return render(request, "roleplay_admin/errors.html", {"errors": formset.errors})
        
        #return HttpResponseRedirect(reverse('rp_admin:game_detail', kwargs={"pk": gl.game.id}))  
        return HttpResponseRedirect(reverse('rp_admin:gl_edit', kwargs={"game_id": game_id, "pk": gl.id})) 
    
    
    else:
        formset = GameLocEventsFormSet(instance=gl)
     

        context = {"gl": gl, "formset": formset}
        return render(request, 'roleplay_admin/gl_edit.html', context)
    
 




GameLocationsEventsCharsFormSet = inlineformset_factory(
                                 GameLocationsEvents, GameLocationsEventsChars,
                                 extra=10,
                                 exclude=("game_location_event"),
                                 #can_order=True
                                )



class ImageFileForm(forms.ModelForm):
    """ Эта форма нужна для теста загрузки одного файла
        и для получения объекта в формы в функции,
        которая принимает один загруженный файл
        (файлы посылаются один за другим при помощи FileAPI)
    
    """
    class Meta:
        model = ImageFile
        #exclude = ('event_chars', 'name')   #остальные скрыты
        fields = ('game', 'location', 'event', 'image', )
        widgets = {
            'game': forms.HiddenInput(),
            'location': forms.HiddenInput(),
            'event': forms.HiddenInput(), #attrs={'required': "required"}
        }



def gle_view(request, pk):
    gle = get_object_or_404(GameLocationsEvents, pk=pk)
    game_loc = gle.game_location
    game = gle.game_location.game
    
    chars = GameLocationsEventsChars.objects.filter(game_location_event=gle)
    images = ImageFile.objects.filter(game=game,
                                      location=game_loc.location,
                                      event=gle.event)
    
    initial_data = {"game": game.id,
                    "location": game_loc.location.id,
                    "event": gle.event.id}
    
    image_upload_form = ""
    image_upload_form = ImageFileForm(initial=initial_data) #включить для теста

    
    context = {"game": game,
               "game_loc": game_loc,
               "gle": gle,
               "chars": chars,
               "images": images,
               "image_upload_form": image_upload_form,
               }
    
    return render(request, 'roleplay_admin/gle_view.html', context)



def gle_chars_edit(request, pk):
    gle = GameLocationsEvents.objects.get(pk=pk)
    game_loc = gle.game_location
    game = gle.game_location.game
    
    if request.method == "POST":
        formset = GameLocationsEventsCharsFormSet(request.POST, instance=gle)
        
        if formset.is_valid():
            if formset.has_changed():
                instances = formset.save(commit=False)
                for instance in instances:
                    try:
                        instance.validate_unique()
                    except ValidationError as e:
                        non_field_errors = e.message_dict[NON_FIELD_ERRORS]
                    else:
                        instance.save()

        elif formset.errors:
            return render(request, "roleplay_admin/errors.html", {"errors": formset.errors})
        
        return HttpResponseRedirect(reverse('rp_admin:gle_chars_edit', kwargs={"pk": gle.id}))  
    else:
    
        formset = GameLocationsEventsCharsFormSet(instance=gle)

        context = {"game": game,
                   "game_loc": game_loc,
                   "gle": gle,
                   "formset": formset
                   }
        
        return render(request, 'roleplay_admin/gle_chars_edit.html', context)




'''
"Загрузка файлов через формсет - не удобно"
ImageFileFormSet = modelformset_factory(ImageFile,
                     extra=2,
                     exclude = ('game', 'location', 'event', 'event_chars', 'name'),
                     can_delete=True,
                    )

def gle_file_upload(request, gle_id):
    form = ImageFileForm(request.POST, request.FILES)
    gle = GameLocationsEvents.objects.get(pk=gle_id)

    formset = ImageFileFormSet(request.POST, request.FILES)
    
    if formset.is_valid():
        if formset.has_changed():
    
            instances = formset.save(commit=False)
            for instance in instances:
                    instance.game_id = 1
                    instance.game_location_id  = 1
                    instance.game_location_event  = gle
                    instance.save()


    return HttpResponseRedirect(reverse('rp_admin:gle_view', kwargs={"pk": gle.id})) 
'''



def file_upload(request):
    response = HttpResponse(mimetype='application/json')
    result = {"status": "error"}
    form = ImageFileForm(request.POST, request.FILES)
    
    print form.is_valid()
   
    if form.errors:
        result["err_messages"] = form.errors.values()
        response.write(json.dumps(   result   ))
        return response


    instance = form.save()
    
    if instance.id:
        result["status"] = "success"
        result["rec_id"] = instance.id
        result["image_ulr"] = instance.image.url
    else:
        result["err_message"] = "Ошибка сохранения: неизвестно"

    response.write(json.dumps(   result  )) 
    return response






    
from django.template import RequestContext
from django.http import HttpRequest

def test_default(request):
    pass


def test(request):
    #print request
    print request
    '''
    print dir(request)

    print dir(HttpRequest)
    #print HttpRequest.path_info
    #print HttpRequest.get_full_path()
    #print HttpRequest.GET
    
    r = HttpRequest()
    print r.GET
    print dir(r)
    print r.path_info
    print r.path
    #print r.get_full_path(r)
    '''
    
    context = {}
    rslv = request.resolver_match
    
    context["url_name"] = rslv.url_name
    context["app_name"] = rslv.app_name
    context["args"] = rslv.args
    context["kwargs"] = rslv.kwargs
    context["namespace"] = rslv.namespace
    context["namespaces"] = rslv.namespaces
    print rslv
    print dir(rslv)
    
    print rslv.__dict__
    print context



    
    c = RequestContext(request, {'foo': 'bar'})
    
    return render(request, 'roleplay_admin/test.html', c)
    
    
    
    
    
    
    