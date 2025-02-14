from django.urls import path
from .views import home,herb_search,load_more_herbs,about,login

urlpatterns = [
    path('', home, name='home'),
    path('search/', herb_search, name='herb_search'),
    path('api/herbs/', load_more_herbs, name='load_more_herbs'),
    path('about/', about, name='about'),
    path('login/', login, name='login'),
]
