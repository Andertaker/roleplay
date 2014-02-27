# -*- coding: utf-8 -*-

import os

from django.contrib.auth.models import User
from django.db import models
from django.db.models.fields.files import ImageFieldFile, ImageFileDescriptor
from django.core.files.uploadedfile import UploadedFile

from snippets.image_thumb_field import ImageThumbField
from roleplay.settings import THUMB_DIR, THUMB_SIZE
from django.core.exceptions import ValidationError


  
  
def check_min_date(_date):
    tm_year = _date.timetuple().tm_year
    if tm_year < 2014:
        raise ValidationError(u"Дата не может быть ранее 01.01.2014")
    
     


        
class Char(models.Model):
    ''' 
        Персонаж (Character)
        Например:
            Ланселот,
            Король Артур,
            Орк,
            Гоблин,
    '''   
    name = models.CharField('Название', max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField('Описание', blank=True)
    
    class Meta:
        verbose_name = ('Персонаж')
        verbose_name_plural = ('Персонажи')

    def __unicode__(self):
        return self.name
 
    def clean(self):
        self.name = self.name.strip()
        self.description = self.description.strip()
        super(Char, self).clean() 

        
        
class Event(models.Model):
    '''
    
    События локации, например: Штурм, Коронация, Свадьба
    
    '''   
    name = models.CharField('Название', max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField('Описание', blank=True)
    
    class Meta:
        verbose_name = ('Событие')
        verbose_name_plural = ('События')

    def __unicode__(self):
        return self.name
        
    def clean(self):
        self.name = self.name.strip()
        self.description = self.description.strip()
        super(Event, self).clean() 
        

        
class Location(models.Model):
    '''
    
    Локация игры, например: Шир,Норгатрон
    
    '''   
    name = models.CharField('Название', max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField('Описание', blank=True)
   
    class Meta:
        verbose_name = ('Локация')
        verbose_name_plural = ('Локации')

    def __unicode__(self):
        return self.name

    def clean(self):
        self.name = self.name.strip()
        self.description = self.description.strip()
        super(Location, self).clean() 

              
        
        
class Game(models.Model):
    name = models.CharField('Название', max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    date = models.DateField('Дата игры', db_index=True, validators=[check_min_date])
    description = models.TextField('Описание', blank=True)
    
    locations = models.ManyToManyField(Location, through='GameLocations')
    #gamelocation = models.ManyToManyField('GameLocations', through='GameLocations')

    class Meta:
        verbose_name = ('Игра')
        verbose_name_plural = ('Игры')
        ordering =("date",)

    def __unicode__(self):
        return self.name

    def clean(self):
        self.name = self.name.strip()
        self.description = self.description.strip()
        super(Game, self).clean()
        
    def imagefile_count(self):
        return self.imagefile_set.all().count()
    imagefile_count.short_description = 'Кол-во фото'
    
        
        
        
class GameLocations(models.Model):
    game = models.ForeignKey(Game)
    location = models.ForeignKey(Location)
    
    events = models.ManyToManyField(Event, through='GameLocationsEvents')
    
    class Meta:
        unique_together = ("game", "location")
        ordering = ["id"]
        
        
        
class GameLocationsEvents(models.Model):
    '''
        Событие привязываем к конкретной локации
    '''
    game_location = models.ForeignKey(GameLocations)
    event = models.ForeignKey(Event)
    
    users  = models.ManyToManyField(User, through='GameLocationsEventsChars')
    chars  = models.ManyToManyField(Char, through='GameLocationsEventsChars')
        
    class Meta:
        unique_together = ("game_location", "event")

    def chars_count(self):
        return self.gamelocationseventschars_set.count()
    
        
        
        
class GameLocationsEventsChars(models.Model):
    '''
    Кто и каким персонажем был на конкретном событии
        
    '''
    game_location_event = models.ForeignKey(GameLocationsEvents)
    user = models.ForeignKey(User)
    char = models.ForeignKey(Char)        #char_id
    
    class Meta:
        unique_together = ("game_location_event", "user", "char")
        
        

  
        
        
class ImageFile(models.Model):
    """
        У фото указываем к какой игре относится
        к какой локации определённой игры
        или же к какому событию определённой локации определённой игры
    """
    game = models.ForeignKey(Game)      #игра должна быть задана
    location = models.ForeignKey(Location, null=True, blank=True)
    event = models.ForeignKey(Event, null=True, blank=True)
    name = models.CharField('Название', max_length=100, default="", blank=True)
    image = ImageThumbField(upload_to="uploads",
                            width_field="width",
                            height_field="height",
                            thumb_upload_to=THUMB_DIR,
                            thumb_size=THUMB_SIZE,
                            exif_date_field="exif_date",
                            db_index=True,
                            )
    width = models.PositiveSmallIntegerField(editable=False)
    height = models.PositiveSmallIntegerField(editable=False)
    exif_date = models.DateTimeField('Дата снимка', null=True, default=None, editable=False, db_index=True)     # берётся из exif
    add_date = models.DateTimeField('Дата добавления', auto_now_add=True, db_index=True, validators=[check_min_date])
    
    event_chars = models.ManyToManyField(GameLocationsEventsChars, through='EventCharImage')

    class Meta:
        #unique_together = ("game", "location", "event", "image")
        verbose_name = ('Фото')
        verbose_name_plural = ('Фотографии')
        
    
    def clean(self):
        if self.game_id is None:
            raise ValidationError(u"Поле 'Игра' должно быть задано")

    
        "Проверяем есть ли файл в этой игре, если нет то сохраняем"
        #проверям только если загружается файл
        if isinstance(self.image.file, UploadedFile):
            field = self.image.field
            "то что сохранится в БД после преобразования имени изображения"
            image = field.upload_to + "/" + field.get_filename(self.image.name)
            count = ImageFile.objects.filter(game=self.game, image=image).count()
            if count:
                raise ValidationError(u"В игре '%s' файл с именем '%s' уже существует" %
                                            (self.game.name, self.image.name))
            
            
            
            
        "поле game и так обязательно"
        "проверяем есть ли в игре данная локация"
        if self.location:
            try:
                gl = GameLocations.objects.get(game=self.game, location=self.location)
            except GameLocations.DoesNotExist:
                raise ValidationError(u"В игре '%s' нет локации '%s'" %
                                       (self.game, self.location))
        
        elif(self.event):   #Событие выбрано, а локация - нет.
            raise ValidationError(u"Выберите локацию")
            
            
        if(self.event): #gl получили выше
            if not GameLocationsEvents.objects.filter(
                                game_location=gl, event=self.event).count():
                raise ValidationError(u"Игра %s -> %s не имеет события %s" %
                                      (self.game, self.location, self.event))
            
            
        super(ImageFile, self).clean()    
            
        
        
#class GameLocationsEventsCharsImage(models.Model):
class EventCharImage(models.Model):
    ''' 
        Привязка записей персонажей события фотографии
        Вообщем в этой модели хранится кто изображён на фото
        Фото и записи участников должны быть из одного Event'a
        
    '''
    image_file = models.ForeignKey(ImageFile)
    
    'указываем id записи, в которой указан человек и его персонаж'
    game_location_event_char = models.ForeignKey(GameLocationsEventsChars)
    coordinates = models.CharField('Кординаты', max_length=100)
        
        
        
        
        
    
    
    

        
        
