# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url

import views
from roleplay import settings


game_patterns = patterns('',
    url(r'^add$', views.game_add, name='game_add'),
    url(r'^(?P<pk>\d+)/$', views.GameView.as_view(), name='game_detail'),
    #url(r'^game/(?P<slug>[\-\d\w]+)$', views.GameView.as_view(), name='game_detail'),
    url(r'^(?P<pk>\d+)/edit$', views.game_edit, name='game_edit'),
    url(r'^(?P<game_id>\d+)/location/(?P<pk>\d+)/edit', views.gl_edit, name='gl_edit'),
    
    url(r'^event/(?P<pk>\d+)/$', views.gle_view, name='gle_view'),
    url(r'^event/(?P<pk>\d+)/chars', views.gle_chars_edit, name='gle_chars_edit'),
    #url(r'^game/file_upload_event/(?P<gle_id>\d+)', views.gle_file_upload, name='gle_file_upload'),
    url(r'^file_upload/', views.file_upload, name='file_upload'),
)

user_patterns = patterns('',
    url(r'^user/$', views.UserIndexView.as_view(), name='users'),
    url(r'^user/add', views.UserAddView.as_view(), name='user_add'),
    url(r'^user/(?P<pk>\d+)/edit', views.UserEditView.as_view(), name='user_edit'),
    url(r'^user/(?P<pk>\d+)', views.UserView.as_view(), name='user_detail'),
)


urlpatterns = patterns('',
    url(r'^$', views.GameIndexView.as_view(), name='games'),
    url(r'^game/', include(game_patterns, app_name='rp_admin_games')),

    url(r'^', include(user_patterns, app_name='users')),
)






if settings.DEBUG:
    test_patterns = patterns('',
        #url(r'^$', views.GameIndexView.as_view(), name='games'),
        url(r'^sdfsdf', views.test),
        url(r'^', views.test, name='test_detail'),
    
    )
    
    urlpatterns = patterns('',
    url(r'^test1', views.test, name='test'),
    url(r'^test/', include(test_patterns, namespace='test_menu_ns'), name='include_name'),

    
) + urlpatterns








