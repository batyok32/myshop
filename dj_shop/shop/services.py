from .models import Product
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from .forms import CommentForm, SearchForm, ContactForm

def search(request, form):
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid:
            form=form
            language=request.LANGUAGE_CODE
            query = form.cleaned_data['query']
            search_vector = SearchVector('translations__name', 'category__translations__name', 'brand__name' )
            search_query = SearchQuery(query)
            search_products= Product.objects.filter(translations__language_code=language)
            results = search_products.annotate(
                search=search_vector,
                rank=SearchRank(search_vector, search_query)
            ).filter(search=search_query).order_by('-rank')     
            return results             


def most_viewed_ranking(request, products):
    # most viewed
    product_ranking = redis_r.zrange('product_ranking', 0, -1, desc=True)[:10]
    product_ranking_ids=[int(id) for id in product_ranking]

    # get the most viewed products
    most_viewed = list(products.filter(id__in=product_ranking_ids))
    most_viewed.sort(key=lambda x: product_ranking_ids.index(x.id))