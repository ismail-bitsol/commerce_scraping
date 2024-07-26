from . import views
from django.urls import include, path
from rest_framework import routers
# from .views import ProductViewSet, WebsiteViewSet, scrape_and_store
from .views import  scrape_and_store
from .views import get_keyword_data, scrape_and_store, search_products, current_time, product_list

urlpatterns = [
    path('api/get_keyword_data/', get_keyword_data, name='get_keyword_data'),
    path('api/scrape_and_store/', scrape_and_store, name='scrape_and_store'),
    path('product_hunt/api/search/', search_products, name='api_search_products'),
    # Add other paths here
]


urlpatterns = [
    path("",views.index,name="index"),
    path('product_hunt/time/', views.current_time, name='current_time'),
    path('product_hunt/products/', views.product_list, name='product_list'),
    path('product_hunt/api/search/', views.search_products, name='search_products'),
    # path('api/products/', views.ProductViewSet.as_view({'get': 'list', 'post': 'create'}), name='api_product_list'),
    path('product_hunt/api/search/', search_products, name='api_search_products'),
    path('product_hunt/api/get_keyword_data/', views.get_keyword_data, name='get_keyword_data'),
    path('product_hunt/api/scrape_and_store/', views.scrape_and_store, name='scrape_and_store'),
]