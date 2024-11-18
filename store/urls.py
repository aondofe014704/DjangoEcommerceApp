from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter
from . import views

router = DefaultRouter()
router.register("collections", views.CollectionViewSet, basename="collections")
router.register("products", views.ProductListViewSet, basename="products")
router.register("carts", views.CartViewSet, basename="carts")
router.register("orders", views.OrderViewSet)

product_router = NestedDefaultRouter(router, 'products', lookup='product')
product_router.register('reviews', views.ReviewViewSet, basename="product_review")

cart_item_router = NestedDefaultRouter(router, 'carts', lookup='cart')
cart_item_router.register('cart_item', views.CartItemViewSet, basename="cart_item")

urlpatterns = router.urls + product_router.urls + cart_item_router.urls

# print(router.urls)
#
# urlpatterns = router.urls

# urlpatterns = [
#     path('', include(router.urls)),
#
#     path('products', views.ProductList.as_view()),
#
#     path('products/<int:pk>', views.ProductDetailAPIView.as_view()),
#
#     #     path('collections', views.CollectionListApiView.as_view()),
#     #
#     #     path('collections/<int:pk>', views.CollectionDetailAPIView.as_view()),
# ]
