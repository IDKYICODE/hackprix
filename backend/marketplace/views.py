from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions, generics
from rest_framework import filters # Import filters
from django.shortcuts import get_object_or_404
from django.db import transaction

from utils.blockchain import execute_marketplace_purchase, get_live_balance
from .models import ProductCategory, Product, Redemption, PointTransaction, Cart, CartItem
from .serializers import (
    ProductCategorySerializer,
    ProductSerializer,
    RedemptionSerializer,
    CartSerializer,
    CartItemSerializer,
)
class BuyItemView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user
        # In a real app, you'd get this from request.data
        item_id = request.data.get('item_id')
        item_cost = 100 # Fixed cost for demo
        
        if not user.wallet_address:
            return Response({"error": "No wallet linked"}, status=400)

        # 1. Check Blockchain balance before trying to buy
        current_balance = get_live_balance(user.wallet_address)
        if current_balance < item_cost:
            return Response({"error": "Insufficient EDU balance"}, status=400)

        # 2. Execute Admin-Mediated Purchase
        tx_hash, error = execute_marketplace_purchase(user.wallet_address, item_cost)

        if not error:
            # Here you would typically create a 'PurchaseHistory' record in Django
            return Response({
                "message": "Item purchased successfully!",
                "tx_hash": tx_hash
            }, status=status.HTTP_200_OK)
        else:
            return Response({"error": f"Purchase failed: {error}"}, status=500)


# --- Product Categories ---
class ProductCategoryListAPIView(generics.ListAPIView):
    queryset = ProductCategory.objects.filter(is_active=True)
    serializer_class = ProductCategorySerializer
    permission_classes = [permissions.AllowAny]


# --- Products ---
class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name", "description", "category__name"]
    ordering_fields = ["name", "points_price", "created_at"]


class ProductDetailAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]


# --- Cart Management ---
class CartDetailView(generics.RetrieveAPIView):
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        return cart

class AddToCartView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        product_id = request.data.get("product_id")
        quantity = int(request.data.get("quantity", 1))

        if not product_id:
            return Response({"error": "Product ID is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        product = get_object_or_404(Product, id=product_id, is_active=True)
        cart, _ = Cart.objects.get_or_create(user=request.user)

        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

        if not created:
            cart_item.quantity += quantity
        else:
            cart_item.quantity = quantity

        # Check stock
        if product.stock is not None and cart_item.quantity > product.stock:
            return Response({"error": "Not enough stock"}, status=status.HTTP_400_BAD_REQUEST)
        
        cart_item.save()
        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RemoveFromCartView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        cart_item_id = request.data.get("cart_item_id")
        if not cart_item_id:
            return Response({"error": "Cart Item ID is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        cart_item = get_object_or_404(CartItem, id=cart_item_id, cart__user=request.user)
        cart_item.delete()

        cart = Cart.objects.get(user=request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ClearCartView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart.items.all().delete()
        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)


# --- Redemption (Purchase from Cart) ---
class RedeemCartView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user
        cart, _ = Cart.objects.get_or_create(user=user)
        cart_items = cart.items.all()

        if not cart_items:
            return Response({"error": "Your cart is empty."}, status=status.HTTP_400_BAD_REQUEST)

        if not user.wallet_address:
            return Response({"error": "No blockchain wallet linked."}, status=status.HTTP_400_BAD_REQUEST)

        total_points_cost = 0
        with transaction.atomic():
            # First pass: check stock and calculate total cost
            for item in cart_items:
                if item.product.stock is not None and item.product.stock < item.quantity:
                    return Response({"error": f"Not enough stock for {item.product.name}"}, status=status.HTTP_400_BAD_REQUEST)
                total_points_cost += item.product.points_price * item.quantity

            # Check Blockchain Balance
            current_balance = get_live_balance(user.wallet_address)
            if current_balance < total_points_cost:
                return Response({"error": "Insufficient EDU balance."}, status=status.HTTP_400_BAD_REQUEST)
            print("NOt upto here")
            # Execute single Blockchain Purchase for the total amount
            tx_hash, error = execute_marketplace_purchase(user.wallet_address, total_points_cost)

            if error:
                print("Error occured here")
                return Response({"error": f"Blockchain transaction failed: {error}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            

            # Second pass: Create redemption records and update stock
            for item in cart_items:
                Redemption.objects.create(
                    user=user,
                    product=item.product,
                    quantity=item.quantity,
                    points_spent=item.product.points_price * item.quantity,
                    status="completed",
                    tx_hash=tx_hash, # Use the same hash for all redemptions in this batch
                    shipping_address=user.address,
                )
                if item.product.stock is not None:
                    item.product.stock -= item.quantity
                    item.product.save(update_fields=["stock"])

            # Record a single PointTransaction for the whole cart
            PointTransaction.objects.create(
                user=user,
                tx_type="spend",
                source="redemption",
                amount=total_points_cost,
                description=f"Redeemed {cart_items.count()} items from cart.",
                on_chain_tx_hash=tx_hash,
            )

            # Clear the cart
            cart_items.delete()

        return Response({"message": "Cart redeemed successfully!", "tx_hash": tx_hash}, status=status.HTTP_200_OK)


# --- User Redemption History ---
class UserRedemptionHistoryAPIView(generics.ListAPIView):
    serializer_class = RedemptionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Redemption.objects.filter(user=self.request.user).order_by("-created_at")