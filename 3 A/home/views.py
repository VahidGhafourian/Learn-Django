from django.shortcuts import render, get_object_or_404, redirect
from rest_framework.response import Response
from django.views import View
from .models import Product, Category
from . import tasks
from django.contrib import messages
from utils import IsAdminUserMixin
from rest_framework.views import APIView
from .serializers import ProductSerializer, CategorySerializer
from rest_framework import status

class HomeView(APIView):
    """
        Method: Get \n
            Get all list of products (for a category)
        input: \n
            optional: category_slug
        return: \n
            list of products (for a category)

    """
    def get(self, request, category_slug=None):
        products = Product.objects.filter(available=True)
        categories = Category.objects.filter(is_sub=False)
        if category_slug:
            categories = Category.objects.get(slug=category_slug)
            products = products.filter(category=categories)
        # return render(request, 'home/home.html', {'products': products, 'categories': categories})
        categories = CategorySerializer(instance=categories, many=True)
        products = ProductSerializer(instance=products, many=True)
        return Response(data={'products': products.data,
                              'category': categories.data,}, status=status.HTTP_200_OK)

class ProductDetailView(APIView):
    """
        Method: Get \n

        input: \n

        return: \n


    """
    def get(self, request, slug):
        product = get_object_or_404(Product, slug=slug)
        # form = CartAddForm()
        # return render(request, 'home/detail.html', {'product': product, 'form': form})
        print(type(product))
        product = ProductSerializer(instance=product)
        return Response(data={'product': product.data}, status=status.HTTP_200_OK)

class BucketHome(IsAdminUserMixin, View):
    """
        Method: Get \n

        input: \n

        return: \n

    """
    template_name = 'home/bucket.html'

    def get(self, request):
        objects = tasks.all_bucket_objects_task()
        # TODO: serialize buckets
        return render(request, self.template_name, {'objects': objects})

class DeleteBucketObjectView(IsAdminUserMixin, View):
    """
        Method: Get \n

        input: \n

        return: \n

    """
    def get(self, request, key):
        print(key)
        tasks.delete_object_task.delay(key)
        messages.success(request, 'your object will be delete soon.', 'info')
        return redirect('home:bucket')

class DownloadBucketObjectView(IsAdminUserMixin, View):
    """
        Method: Get \n

        input: \n

        return: \n

    """
    def get(self, request, key):
        tasks.download_object_task.delay(key)
        messages.success(request, 'your donwload will start soon', 'info')
        return redirect('home:bucket')
