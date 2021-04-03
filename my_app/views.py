import json

from django.core.paginator import Paginator
from django.core.serializers import serialize
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View

from .models import TopSongPoularity

def index(request):
    return render(request, "index.html", {})

class ListTopSongs(View):
    # set default page limit as 10
    page_limit = 10 # default
    
    '''
    Helper method to get the pagination context
    out of queryset of given page number with limit.
    Args: 
        queryset: Filtered queryset object
        page: a number representing the page number
        limit: the result count, per page.
        
    Returns the JSON of queryset for given page, 
        with pagination meta info.
    '''
    def get_paginated_context(self, queryset, page, limit):
        if not page:    page = 1 #if no page provided, set 1
        
        # if limit specified, set the page limit
        if limit:   
            self.page_limit = limit  

        # instantiate the paginator object with queryset and page limit
        paginator = Paginator(queryset, self.page_limit)
        # get the page object
        page_obj = paginator.get_page(page)
        # serialize the objects to json
        serialized_page = serialize("json", page_obj.object_list)
        # get only required fields from the serialized_page json.
        serialized_page = [obj["fields"] for obj in json.loads(serialized_page)]

        # return the context.
        return {
            "data": serialized_page,
            "pagination": {
                "page": page,
                "limit": limit,
                "has_next": page_obj.has_next(),
                "has_prev": page_obj.has_previous(),
                "total": queryset.count()
            }
        }
    
    '''
    GET method for this View.
    '''
    def get(self, request, *args, **kwargs):
        # fetch the query params
        page = request.GET.get('page')
        limit = request.GET.get('limit')
        country = request.GET.get('country')
        start = request.GET.get('start')
        end = request.GET.get('end')
        
        sort_by = request.GET.get('sort_by')
        # get all results from DB.
        queryset = TopSongPoularity.objects.all()
        
        '''filter the queryset object based on query params'''
        # 1. on basis of country
        if country and country != "all":
            queryset = queryset.filter(country=country)
        # 2. On basis of date (start and end date)
        if start and end:
            if start != "0" and end != "0":
                queryset = queryset.filter(
                    year__gte = start, 
                    year__lte = end
                )
        
        # 3. Sorting the filtered queryset
        if sort_by and sort_by != "0":
            queryset = queryset.order_by(sort_by)

        # return the serialized output by 
        # calling method 'get_paginated_context'
        to_return = self.get_paginated_context(queryset, page, limit)
        return JsonResponse(to_return, status = 200)
    
def getCountries(request):
    # get Countries from the database 
    # excluding null and blank values
    if request.method == "GET" and request.is_ajax():
        country = TopSongPoularity.objects.all().\
            	values_list('country').distinct()
        country = [c[0] for c in list(country)]
        
        return JsonResponse({
            "country": country, 
        }, status = 200)

