from django.shortcuts import render, redirect, get_object_or_404
from .models import Category, Product, Comment
from cart.forms import CartAddProductForm
from django.contrib.auth.decorators import login_required
import redis
from .forms import CommentForm, SearchForm, ContactForm
from django.conf import settings
from .recommender import Recommender
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.urls import reverse
from .view import View
# from .services import search
from django.views.decorators.cache import cache_page
from django.core.cache.backends.base import DEFAULT_TIMEOUT

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

# connect to redis
redis_r = redis.Redis(host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                db=settings.REDIS_DB)


# Create your views here.
# @cache_page(CACHE_TTL)
def product_list(request, category_slug=None, filter_slug=None):
    language = request.LANGUAGE_CODE
    count=6
    category = None
    selected=None
    # categories = Category.objects.all()
    products = Product.objects.filter(available=True, translations__language_code=language,)
    total_category_products = None
    template='shop/product/index.html'
    max_price_products = None
    min_price_products = None
    latest_products = None

    
    if category_slug:
        category = get_object_or_404(Category,
                                    translations__language_code=language,
                                    translations__slug=category_slug)
        products = products.filter(category=category)
        total_category_products=products.count()
        template='shop/product/list.html'
        
    if not category_slug:
        max_price_products = products.order_by('-price')[:count]
        min_price_products = products.order_by('price')[:count]
        latest_products = products.order_by('-created')[:count]

    # most viewed
    product_ranking = redis_r.zrange('product_ranking', 0, -1, desc=True)[:10]
    product_ranking_ids=[int(id) for id in product_ranking]

    # get the most viewed products
    most_viewed = list(products.filter(id__in=product_ranking_ids))
    most_viewed.sort(key=lambda x: product_ranking_ids.index(x.id))


    # filtering products
    if filter_slug:
        if filter_slug=='default':
            selected='Default'
            pass
            
        elif filter_slug=='min_price':
            products= products.order_by('price')
            selected='The cheapest'
        elif filter_slug=='max_price':
            products= products.order_by('-price')
            selected='The most expensive'
        elif filter_slug=='latest':
            products= products.order_by('-created')
            selected='Latest products'




    # Paginator
    paginator = Paginator(products, 3) # 3 posts in each page
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        # If page not an integer deliver the first page
        products = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver the last page of results
        products = paginator.page(paginator.num_pages)


    # search
    search_form = SearchForm()        

    # add to cart 
    cart_product_form = CartAddProductForm()

    return render(request,
                template,
                {'page':page,
                'category':category,
                'products':products, 
                'min_price_products':min_price_products,
                'max_price_products':max_price_products,
                'latest_products':latest_products,
                'total_category_products':total_category_products,
                'search_form':search_form,
                'most_viewed':most_viewed,
                'cart_product_form':cart_product_form,
                'selected':selected,
                })  
                

# @cache_page(CACHE_TTL)
def product_detail(request, id, slug):
    language=request.LANGUAGE_CODE
    product= get_object_or_404(Product, 
                                id=id,
                                translations__language_code=language,
                                translations__slug=slug,
                                amount__gte=1,
                                available=True)
    cart_product_form = CartAddProductForm(initial={
            'quantity': 1,
            'override': True})

    # List of active comments for this post 
    comments = product.comments.filter(active=True)

    new_comment = None

    if request.method == 'POST':
    # A comment was posted
        comment_form = CommentForm(data=request.POST)
        if request.user.is_authenticated():
            if comment_form.is_valid():
            # Create Comment object but don't save to database yet
                new_comment = comment_form.save(commit=False)
                # Assign the current post to the comment
                new_comment.product = product
                new_comment.user = request.user
                # Save the comment to the database
                new_comment.save()
        else:
            return redirect('login')
    else:
        comment_form = CommentForm()


    # view
    # product_id=str(product.id)
    total_views=None

    view = View(request)
    view.add(product)
    total_views = redis_r.get(f'product:{product.id}:views')
    total_views = int(total_views)
    # print(view)
    # if product_id not in view:
    #     redis_r.zincrby('product_ranking', 1, product.id)
    #     total_views = redis_r.incr(f'product:{product.id}:views')
    #     view[product_id] = {}
    # else:
    #     total_views = redis_r.get(f'product:{product.id}:views')
    #     total_views = int(total_views)
    
    images=product.images.all()

        
    r=Recommender()
    recommended_products = r.suggest_products_for([product], 4)
    return render(request, 'shop/product/detail.html', {'product':product,
                                    'cart_product_form':cart_product_form,
                                    'total_views':total_views,
                                    'recommended_products': recommended_products,
                                    'comments': comments,
                                    'new_comment': new_comment,
                                    'comment_form': comment_form,
                                    'images':images,
                                    'media_url':settings.MEDIA_URL})




# def product_search(request, filter_slug=None):
#     categories = Category.objects.all()
#     form = SearchForm()
#     page=None
#     selected='Default'
#     if 'query' in request.GET:
#         form = SearchForm(request.GET)
#         if form.is_valid():
#             language=request.LANGUAGE_CODE
#             query = form.cleaned_data['query']
#             search_vector = SearchVector('translations__name', 'category__translations__name', 'brand__name' )
#             search_query = SearchQuery(query)
#             search_products= Product.objects.filter(translations__language_code=language)
#             results = search_products.annotate(
#                 search=search_vector,
#                 rank=SearchRank(search_vector, search_query)
#             ).filter(search=search_query).order_by('-rank')
    
#     count=len(results)
#     if filter_slug:
#         if filter_slug=='default':
#             selected='Default'
        
#             results= results.order_by('-rank')
#         elif filter_slug=='min_price':
#             results= results.order_by('price')
#             selected='Min price'
#         elif filter_slug=='max_price':
#             results= results.order_by('-price')
#             selected='Max price'
#         elif filter_slug=='latest':
#             results= results.order_by('-created')
#             selected='Latest'

#             # Paginator
#     paginator = Paginator(results, 3) # 3 posts in each page
#     page = request.GET.get('page')
#     try:
#         results = paginator.page(page)
#     except PageNotAnInteger:
#         # If page not an integer deliver the first page
#         results = paginator.page(1)
#     except EmptyPage:
#             # If page is out of range deliver the last page of results
#         results = paginator.page(paginator.num_pages)


#     return render(request,
#                 'shop/product/search.html',
#                 {'page':page,
#                 'form':form,
#                 'query':query,
#                 'results':results,
#                 'categories':categories,
#                 'selected':selected,
#                 'count':count})
# TODO:DUzetmeli
# @cache_page(CACHE_TTL)
def product_search(request):
    categories = Category.objects.all()
    form = SearchForm()
    page=None
    query=None
    count=None
    results=None
    

    if 'query' in request.GET:
        form = SearchForm(request.GET)
        products=[]
        if form.is_valid():
            # language=request.LANGUAGE_CODE
            query = form.cleaned_data['query']
            search_vector = SearchVector('translations__name', 'category__translations__name', 'translations__description', 'brand__name' )
            search_query = SearchQuery(query)
            search_products= Product.objects.filter(translations__language_code=request.LANGUAGE_CODE)
            results = search_products.annotate(
                search=search_vector,
                rank=SearchRank(search_vector, search_query)
            ).filter(search=search_query).order_by('-rank')
            
            results=results.filter(translations__language_code=request.LANGUAGE_CODE)
            for result in results:
       
                if result not in products:
                    products.append(result) 
             
            results = products
            print(results)
            count=len(results)

        # if filter_slug:
        #     if filter_slug=='default':
        #         selected='Default'
        #         results= results.order_by('-rank')
        #     elif filter_slug=='min_price':
        #         results= results.order_by('price')
        #         selected='Min price'
        #     elif filter_slug=='max_price':
        #         results= results.order_by('-price')
        #         selected='Max price'
        #     elif filter_slug=='latest':
        #         results= results.order_by('-created')
        #         selected='Latest'

            # Paginator
            paginator = Paginator(results, 3) # 3 posts in each page
            page = request.GET.get('page')
            try:
                results = paginator.page(page)
            except PageNotAnInteger:
                # If page not an integer deliver the first page
                results = paginator.page(1)
            except EmptyPage:
                # If page is out of range deliver the last page of results
                results = paginator.page(paginator.num_pages)

    return render(request,
                'shop/product/search.html',
                {'page':page,
                'form':form,
                'query':query,
                'count':count,
                'results':results,
                'categories':categories,})
                # 'selected':selected,


# @cache_page(CACHE_TTL)
@login_required
def contact(request):
    sent=False
    if request.method == 'POST':
        contact_form = ContactForm(request.POST)
        if contact_form.is_valid():
            contact_form.save(commit=False)
            contact_form.user=request.user
            contact_form.save()
            messages.success(request, "Successfully sent")
            sent=True
            
        # else:
        #     messages.error(request, 'Form filled incorrect')
    else:
        contact_form = ContactForm()

    return render(request, 'shop/product/contact.html', 
                {'form':contact_form,
                'sent':sent,
            })