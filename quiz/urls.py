from django.urls import path
from .views import *

urlpatterns = [
    path('index-page', index_page, name='index_page'),
    path('show-results', result, name='result')

]