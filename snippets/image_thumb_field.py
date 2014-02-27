# -*- coding: utf-8 -*-

from StringIO import StringIO
from datetime import datetime

from django.db import models
from django.db.models.fields.files import ImageFieldFile, ImageFileDescriptor

from PIL import Image



        
        
class ImageThumbFieldFile(ImageFieldFile):
    
    #thumb["name"] = "thumb_" + self.image.name.split("/").pop()
    #thumb["url"] = THUMB_ROOT + "/" + thumb["name"]
    #self.image.__setattr__("thumb", thumb)
    """
    def __init__(self, instance, field, name):
        super(ImageThumbFieldFile, self).__init__(instance, field, name)
        #print dir(self)
        
        print "__init__"
        print "instance: ", instance
        print dir(instance)
        print "field: ", field
        print "name: ", name
        
        #instance.date_time = "sdfsdf"
        
        '''
        image = instance.image
        print "image: ", image
        print dir(image)
        '''
        
    """

    
    
    def save(self, name, content, save=True):
        super(ImageThumbFieldFile, self).save(name, content, save=save)
        '''
        print "save_file"
        print "name: ", name
        print self.name
        print "save: ", save
        print dir(self)
        instance", self.instance.__class__
        print dir(self.instance)
        '''
        
        THUMB_DIR = self.field.thumb_upload_to
        THUMB_ROOT = self.storage.location + "/" + THUMB_DIR    #self.storage.location  равно settings.MEDIA_ROOT
        THUMB_SIZE = self.field.thumb_size
        
        "Делаем и сохраняем thumbnail"
        self.instance.image.open()
        s = self.instance.image.read()
        im = Image.open(StringIO(s))
        im.thumbnail(THUMB_SIZE)
        
        
        img_name = self.name.split("/").pop()   # 'uploads/img.jpg' - берём имя файла
        thumb_name = "thumb_" + img_name
        im.save(THUMB_ROOT + "/" + thumb_name)
    
        if hasattr(im, "_getexif"):
            "Записываем дату создания снимка берём её из exif"
            info = im._getexif()
            #exif_date = info[306]   #306 = date_time - key
            if 306 in info:
                try:
                    dt = datetime.strptime(info[306], "%Y:%m:%d %H:%M:%S")
                    self.instance.exif_date = dt
                except ValueError:
                    self.instance.exif_date = None
        
        
    '''    
    def delete(self, save=True):
        print "delete"
        super(ImageThumbFieldFile, self).delete(save=save)
        print self.name
        print self.thumb.name
        
        self.storage.delete(self.thumb.name)
    delete.alters_data = True
    '''
    
    
    def _get_thumb(self):
        self._require_file()
        thumb = {}
        print self.name
        
        # self.name = field.upload_to + имя файла
        # вместо upload_to берём папку где хранится превьюшки(THUMB_DIR)
        # и присоединяем имя файла

        
        thumb["name"] = self.field.thumb_upload_to + "/thumb_" + self.name.split("/").pop()
        thumb["url"] = self.storage.url(thumb["name"])
        #return self.storage.url(self.name)
        return thumb
    thumb = property(_get_thumb)
    
    
    

        
'''        
class ImageThumbFileDescriptor(ImageFileDescriptor):
   
    def __set__(self, instance, value):
        previous_file = instance.__dict__.get(self.field.name)
        super(ImageThumbFileDescriptor, self).__set__(instance, value)
'''

        
        
        
class ImageThumbField(models.ImageField):
    attr_class = ImageThumbFieldFile
    #descriptor_class = ImageThumbFileDescriptor
    description = "Image with thumb"
    """ """   

    #print dir(self)
    
    #__metaclass__ = models.SubfieldBase
    "добавлена опция exif_date_field"
    
    def __init__(self, verbose_name=None, name=None, width_field=None,
                 height_field=None,
                 thumb_upload_to=None,
                 thumb_size=None,
                 exif_date_field=None,
                 **kwargs):

        super(ImageThumbField, self).__init__(verbose_name, name, width_field,
            height_field, **kwargs)
        
        self.thumb_upload_to = thumb_upload_to
        self.thumb_size = thumb_size
        
        #self.contribute_to_class("thumb", "thumb_val")

    '''    из-за этой опции поле в БД не создаётся
    def get_internal_type(self):
        return 'ImageField'
    ''' 

    
        