from django.urls import path
from .views import (
    BuyItemView,
    ProductCategoryListAPIView,
    ProductListAPIView,
    ProductDetailAPIView,
    UserRedemptionHistoryAPIView,
    CartDetailView,
    AddToCartView,
    RemoveFromCartView,
    ClearCartView,
    RedeemCartView,
)

urlpatterns = [
  path('buy/', BuyItemView.as_view(), name='market-buy'),
  path('categories/', ProductCategoryListAPIView.as_view(), name='product-category-list'),
  path('products/', ProductListAPIView.as_view(), name='product-list'),
  path('products/<int:pk>/', ProductDetailAPIView.as_view(), name='product-detail'),
  
  # Cart
  path('cart/', CartDetailView.as_view(), name='cart-detail'),
  path('cart/add/', AddToCartView.as_view(), name='cart-add'),
  path('cart/remove/', RemoveFromCartView.as_view(), name='cart-remove'),
  path('cart/clear/', ClearCartView.as_view(), name='cart-clear'),
  path('cart/redeem/', RedeemCartView.as_view(), name='cart-redeem'),
  
  # History
  path('redemption/history/', UserRedemptionHistoryAPIView.as_view(), name='redemption-history'),
]
