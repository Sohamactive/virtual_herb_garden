from django.urls import path
from .views import home,herb_search,load_more_herbs,about

urlpatterns = [
    path('', home, name='home'),
    path('search/', herb_search, name='herb_search'),
    path('api/herbs/', load_more_herbs, name='load_more_herbs'),
    path('about/', about, name='about'),
]
