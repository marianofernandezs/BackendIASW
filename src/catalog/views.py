from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.core.paginator import Paginator
from .models import Category, Product
from .services import product_service


def product_list(request):
    category = request.GET.get('category')
    search_term = request.GET.get('search_term')

    products = product_service.get_all_products(
        category_id=category,
        search_term=search_term
    )

    paginator = Paginator(products, 10)
    page_number = request.GET.get('page')
    products_page = paginator.get_page(page_number)

    categories = Category.objects.all()

    return render(request, "catalog/product_list.html", {
        "products_page": products_page,
        "categories": categories,
        "current_category": category,
        "current_search_term": search_term,
    })


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, "catalog/product_detail.html", {
        "product": product
    })


def product_stock(request, product_id):
    stock_info = product_service.get_stock_info(product_id)
    return JsonResponse(stock_info)
