from django.shortcuts import render
from rest_framework import status
from django.http import HttpResponse
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.urls import reverse
from rest_framework import viewsets
from .models import Product, Website
from .serializers import ProductSerializer, WebsiteSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .scrapers import AmazonScraper, EbayScraper, NeweggScraper,utils  # Add other scrapers here
from textblob import TextBlob
import logging
import requests
import threading

logger = logging.getLogger(__name__)

def index(request):
    return render(request,"product_hunt/index.html")



@api_view(['GET'])
def get_keyword_data(request):
    keyword = request.query_params.get('keyword', None)
    if not keyword:
        return Response({"message": "Keyword is not given"}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        logger.info(f"Searching for products with keyword: {keyword}")
        products = Product.objects.filter(keyword__icontains=keyword)
        # if not products.exists():
        #     logger.info(f"No products found for keyword: {keyword}")
        #     return Response({"message": "No products found for the given keyword"}, status=status.HTTP_404_NOT_FOUND)
        
        products_data = ProductSerializer(products, many=True).data
        logger.info(f"Found {len(products_data)} products for keyword: {keyword}")
        return Response(products_data, status=status.HTTP_200_OK)
    
    except Exception as e:
        logger.error(f"An error occurred while fetching products: {str(e)}")
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def scrape_and_store(request):
    keyword = request.data.get('keyword')
    if not keyword:
        return Response({'error': 'Keyword not provided'}, status=status.HTTP_400_BAD_REQUEST)

    # Check if the keyword already exists in the database
    existing_products = Product.objects.filter(keyword__icontains=keyword)
    if existing_products.exists():
        products_data = ProductSerializer(existing_products, many=True).data
        return Response(products_data, status=status.HTTP_200_OK)

    urls = [
        f'https://www.amazon.com/s?k={keyword}',
        f'https://www.ebay.com/sch/i.html?_nkw={keyword}',
        f'https://www.newegg.com/p/pl?d={keyword}'
    ]

    scrapers = [AmazonScraper.AmazonScraper, EbayScraper.EbayScraper, NeweggScraper.NeweggScraper]

    def run_scraper(Scraper, url):
        try:
            scraper = Scraper(url)
            scraper.scrape(keyword)  # Pass the keyword to the scrape method
        except requests.exceptions.RequestException as e:
            logging.error(f'Network error occurred while scraping {url}: {str(e)}')
        except Exception as e:
            logging.error(f'An unexpected error occurred while scraping {url}: {str(e)}')

    threads = []
    for url, Scraper in zip(urls, scrapers):
        thread = threading.Thread(target=run_scraper, args=(Scraper, url))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    # Fetch the newly scraped data
    try:
        new_products = Product.objects.filter(keyword__icontains=keyword)
        if not new_products.exists():
            return Response({'error': 'Failed to scrape data'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        products_data = ProductSerializer(new_products, many=True).data
        return Response(products_data, status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response({'error': f'An unexpected error occurred: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def current_time(request):
    now = timezone.now()
    html = f"<html><body>Current time: {now}</body></html>"
    return HttpResponse(html)

def product_list(request):
    products = Product.objects.all()
    if not products:
        message = "No products found."
        return render(request, 'product_hunt/no_products.html', {'message': message})
    return render(request, 'product_hunt/product_list.html', {'products': products})


@api_view(['GET'])
def search_products(request):
    query = request.GET.get('query', '')
    
    if not query:
        return Response({'error': 'Query parameter is required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        products = Product.objects.filter(name__icontains=query)
        if not products.exists():
            return Response({'message': 'No products found'}, status=status.HTTP_404_NOT_FOUND)

        product_serializer = ProductSerializer(products, many=True)
        
        for product in products:
            product.sentiment_score = utils.sentiment_score(product.reviews)
            product.save()

        best_product = find_best_product(products)

        return Response({
            'products': product_serializer.data,
            'best_product': ProductSerializer(best_product).data if best_product else None
        }, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def find_best_product(products):
    """
    Finds the best product based on price and sentiment score.
    """
    best_product = None
    highest_score = float('-inf')
    
    for product in products:
        score = product.sentiment_score - product.price  # Example scoring formula
        if score > highest_score:
            highest_score = score
            best_product = product
    return best_product
