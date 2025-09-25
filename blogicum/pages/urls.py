from django.urls import path, include

from .views import about, rules

app_name = 'pages'


urlpatterns = [
    path('about/', about, name='about'),
    path('rules/', rules, name='rules'),

]
