from django.shortcuts import render, redirect
from phones.models import Phone

def index(request):
    return redirect('catalog')


def show_catalog(request):
    template = 'catalog.html'
    sort =  request.GET.get('sort')
    product = Phone.objects.all()
    
    if sort == 'name':
        product = product.order_by('name')
    elif sort == 'min_price':
        product = product = product.order_by('price')
    elif sort == 'max_price':
        product = product.order_by('price').reverse()
    else:
        product = product
        
    context = {'phones' : product}
    return render(request, template, context)


def show_product(request, slug):
    template = 'product.html'
    phone = Phone.objects.get(slug=slug)
    context = {'phone': phone}
    return render(request, template, context=context)