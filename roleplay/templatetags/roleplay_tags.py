# -*- coding: utf-8 -*-
from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()




@stringfilter
def startswith(_str, _sub_str):
    return _str.startswith(_sub_str)

register.filter('startswith', startswith)


'''
@stringfilter
def url_is_active(url):
    

register.filter('url_is_active', url_is_active)
'''



'''
class TestNode(template.Node):
    def render(self, context):
        return "test"


@register.tag
def test(parser, token):
    print token
    print dir(token)
    
    #tag_name, value = token.split_contents()
    #print tag_name
    #print value
    
    return TestNode()
'''

#register.filter('test', test)








menu_items = [
    {"url": '/rp_admin', 'name': "Админка"},
    {"url": '/admin', 'name': "Админка(Django)"},          
              
]


class Menu():
    menu_items = [
        {"url": '/rp_admin', 'name': "Админка"},
        {"url": '/admin', 'name': "Админка(Django)"},          
                  
    ]
    
    def menu_items(self):
        return self.menu_items
    
    class Meta:
        abstract = True

