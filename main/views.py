import requests
from django.shortcuts import render
import random
from django.http import JsonResponse
from django.core.cache import cache
HERB_NAMES = [
    "Tulsi", "Aloe Vera", "Sweet Basil", "Spearmint", "Neem", "Ginger", "Rosemary", "Sage", "Thyme", "Lavender",
    "Parsley", "Oregano", "Cilantro", "Dill", "Chives", "Bay Leaf", "Lemongrass", "Marjoram", "Fennel", "Tarragon",
    "Chamomile", "Echinacea", "Ginseng", "Peppermint", "Lemon Balm", "St. John's Wort", "Valerian", "Calendula", "Hibiscus", "Anise",
    "Caraway", "Cumin", "Coriander (seeds)", "Fenugreek", "Lovage", "Saffron", "Sorrel", "Borage", "Chervil", "Horseradish",
    "Mugwort", "Mullein", "Myrtle", "Nettle", "Summer Savory", "Stevia", "Yarrow", "Angelica", "Winter Savory", "Salad Burnet",
    "Sweet Cicely", "Comfrey", "Feverfew", "Garlic Chives", "Lemon Verbena", "Epazote", "Hyssop", "Boldo", "Black Cohosh", "Catnip",
    "Coltsfoot", "Dandelion", "Eucalyptus", "Gotu Kola", "Horehound", "Kava", "Licorice", "Meadowsweet", "Motherwort", "Osha",
    "Pennyroyal", "Red Clover", "Rue", "Skullcap", "Solomon's Seal", "Suma", "Tea Plant", "Turmeric", "Uva Ursi", "Vervain",
    "White Horehound", "Wild Yam", "Wood Betony", "Wormwood", "Zedoary", "Marshmallow", "Goldenseal", "American Ginseng", "Prickly Ash", "Sarsaparilla",
    "Shiso", "Vietnamese Coriander", "Ajwain", "Curry Leaf", "Indian Pennywort", "Moringa", "Barberry", "Jatamansi", "Brahmi", "Ashwagandha"
]
def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')
def login(request):
    return render(request, 'login.html')
def herb_search(request):
    herb_data = None  # Will store the fetched herb details
    query = request.GET.get('q')  # 'q' will be the query parameter from the search form

    # If a query exists, call the Wikipedia API
    if query:
        # Construct the API URL. Replace spaces with underscores if needed.
        formatted_query = query.replace(" ", "_")
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{formatted_query}"
        response = requests.get(url)
        
        # Check if the API call was successful
        if response.status_code == 200:
            herb_data = response.json()
        else:
            herb_data = {"error": "Herb not found or API error."}

    return render(request, 'herb_search.html', {'herb': herb_data, 'query': query})

def load_more_herbs(request):
    offset = int(request.GET.get('offset', 0))
    limit = int(request.GET.get('limit', 6))
    
    herbs = HERB_NAMES.copy()
    random.shuffle(herbs)
    
    selected = herbs[offset:offset + limit]
    if not selected:
        selected = herbs[:limit]
    
    herb_data = []
    for herb in selected:
        # Use the herb name as the cache key
        cache_key = f"wiki_{herb.replace(' ', '_')}"
        data = cache.get(cache_key)
        
        if not data:
            formatted_herb = herb.replace(" ", "_")
            url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{formatted_herb}"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                # Cache the data for 24 hours (86400 seconds)
                cache.set(cache_key, data, 86400)
            else:
                data = {
                    "title": herb,
                    "extract": "No information available.",
                    "thumbnail": None,
                }
        herb_data.append(data)
    
    return JsonResponse({'herbs': herb_data})
