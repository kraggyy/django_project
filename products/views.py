from django.shortcuts import render


def products(requests, *args, **kwargs):
    return render(requests, 'products/index.html')
