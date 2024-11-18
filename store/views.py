from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import api_view
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.mixins import CreateModelMixin
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
# from rest_framework.viewsets import ModelViewSet
# from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet

from .filter import ProductFilter
from .pagination import DefaultPageNumberPagination
from .serializer import (ProductSerializer, CollectionSerializer,
                         CreateProductSerializer, CartSerializer,
                         ReviewSerializer, CartItemSerializer, AddToCartSerializer, CreateCartSerializer,
                         OrderSerializer)
from .models import Product, Collection, Review, Cart, CartItem, Order
from rest_framework import status
from .permission import IsAdminOrReadOnly

#
# class ProductList(ListCreateAPIView):
#     queryset = Product.objects.all()


class ProductListViewSet(ModelViewSet):
    queryset = Product.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter
    pagination_class = DefaultPageNumberPagination
    permission_classes = [IsAdminOrReadOnly]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ProductSerializer
        elif self.request.method == 'POST':
            return CreateProductSerializer
        return ProductSerializer


class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer
    permission_classes = [IsAuthenticated]


class ReviewViewSet(ModelViewSet):
    def get_queryset(self):
        product_pk = self.request.query_params.get('product_pk')
        return Review.objects.get(product_pk=product_pk)

    serializer_class = ReviewSerializer


class CartViewSet(ModelViewSet):
    queryset = Cart.objects.prefetch_related('items__product').all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return CartSerializer
        elif self.request.method == 'POST':
            return CreateCartSerializer
        return CartSerializer


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    permission_class = [IsAuthenticated]

# class CartItemViewSet(ModelViewSet):
#     queryset = CartItem.objects.all()
#     serializer_class = CartSerializer


class CartItemViewSet(ModelViewSet):
    queryset = CartItem.objects.all()

    # serializer_class = CartItemSerializer
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddToCartSerializer
        return CartItemSerializer

    def get_serializer_context(self):
        return {"cart_id": self.kwargs["cart_pk"]}

# class CollectionListApiView(ListCreateAPIView):
#     queryset = Collection.objects.all()
#     serializer_class = CollectionSerializer
#
#
# class CollectionDetailAPIView(RetrieveUpdateDestroyAPIView):
#     queryset = Collection.objects.all()
#     serializer_class = CollectionSerializer

#     def get_queryset(self):
#         return Product.objects.all()
#
#     def get_serializer_class(self):
#         return ListCreateAPIView
#
#
# @api_view(['GET', 'POST'])
# def product_list(request):
#     if request.method == 'GET':
#         products = Product.objects.all()
#         serializer = ProductSerializer(products, many=True, context={'request': request})
#         return Response(serializer.data, status=status.HTTP_200_OK)
#     elif request.method == 'POST':
#         serializer = CreateProductSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#
#
# @api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
# def product_details(request, pk):
#     product = get_object_or_404(Product, pk=pk)
#     if request.method == 'GET':
#         serializer = ProductSerializer(product, data=request.data)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#
#     if request.method == 'PUT':
#         serializer = CreateProductSerializer(product, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_200_OK)
#
#     if request.method == 'DELETE':
#         product.delete()
#         return Response(data={"message": f"Product with {pk} deleted"}, status=status.HTTP_204_NO_CONTENT)
#
#
# @api_view()
# def collection_list(request):
#     collections = Collection.objects.all()
#     serializer = CollectionSerializer(collections, many=True)
#     return Response(serializer.data, status=status.HTTP_200_OK)
#
#
# @api_view()
# def collection_details(request, ):
#     collection = get_object_or_404(Collection, pk=pk)
#     serializer = CollectionSerializer(collection)
#     return Response(serializer.data, status=status.HTTP_200_OK)

# Create your views here.
