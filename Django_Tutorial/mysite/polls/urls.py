#urls.py

from django.urls import path

from . import views

#kwarg stands for keyword argument

#path function is passed 4 arguments, two are required: 'route' and 'view'. Two are optional: 'kwargs' and 'name'
#path(route, view, kwargs, name)
#path() route: string that contains a url pattern. 
#path() view: when Django finds a matching pattern it calls the specified view function with an HttpRequest object as the first argument (see example)
#path() kwargs: arbitrary keyword arguments can be passed in a dictionary to the target 'view'
#path() name: name for the URl, lets you refer to it unambiguously from elsewhere in django, lets you make global changes to url patterns from single point




urlpatterns = [
    path('', views.index, name='index'),
]

