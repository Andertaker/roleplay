# -*- coding: utf-8 -*-

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
from django.conf.urls import patterns, include, url

import views
import settings


"/game/....."
game_patterns = patterns('',
    #url(r'^$', views.GameIndexView.as_view(), name='games'),
      
    url(r'^(?P<game_slug>[\-\d\w]+)/$',
                            views.GameView.as_view(), name='game_detail'),
    url(r'^(?P<game_slug>[\-\d\w]+)/(?P<location_slug>[\-\d\w]+)/$',
                            views.gl_detail, name='gl_detail'),
    url(r'^(?P<game_slug>[\-\d\w]+)/(?P<location_slug>[\-\d\w]+)/(?P<event_slug>[\-\d\w]+)/$',
                            views.gle_detail, name='gle_detail'),      
    url(r'^(?P<game_slug>[\-\d\w]+)/(?P<location_slug>[\-\d\w]+)/(?P<event_slug>[\-\d\w]+)/chars/$',
                            views.gle_chars, name='gle_chars'),   
)


urlpatterns = patterns('',
    url(r'^$', views.GameIndexView.as_view(), name='games'),                     
    url(r'^game/', include(game_patterns, app_name='games')),
        
                       
    url(r'^rp_admin/', include('roleplay_admin.urls', namespace='rp_admin')),
            
    url(r'^admin/', include(admin.site.urls)),     #Django-admin
    url(r'^', include('cms.urls')),     #Django-CMS
    
)








if settings.DEBUG:
    urlpatterns = patterns('',
                           
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),

    url(r'^static/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.STATIC_ROOT, 'show_indexes': True}),     
                                  
    url(r'', include('django.contrib.staticfiles.urls')),
    
) + urlpatterns