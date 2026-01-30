from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions, generics
from rest_framework import filters # Import filters
from django.shortcuts import get_object_or_404
from django.db import transaction
from web3 import Web3

from utils.blockchain import (
    get_live_balance, 
    execute_marketplace_purchase, 
    get_token_contract, 
    w3, 
    MARKET_ADDR,
    ensure_checksum,
)

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
        # Convert address to checksum immediately to satisfy web3.py
        safe_wallet = ensure_checksum(user.wallet_address)
        
        item_id = request.data.get('item_id')
        item_cost = 100 # Fixed cost for demo
        
        if not safe_wallet:
            return Response({"error": "Invalid or missing wallet address"}, status=400)

        # 1. Check Blockchain balance
        current_balance = get_live_balance(safe_wallet)
        if current_balance < item_cost:
            return Response({"error": "Insufficient EDU balance"}, status=400)

        # 2. Execute Admin-Mediated Purchase
        tx_hash, error = execute_marketplace_purchase(safe_wallet, item_cost)

        if not error:
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
        
        # 1. Validation and Address Preparation
        db_address = user.wallet_address
        db_pvt_key = user.private_key # Consider moving this to a secure vault

        if not db_address or not db_pvt_key:
            return Response({"error": "Wallet configuration incomplete."}, status=400)

        try:
            student_address = Web3.to_checksum_address(db_address)
            market_address = Web3.to_checksum_address(MARKET_ADDR)
        except Exception as e:
            return Response({"error": f"Invalid Address: {str(e)}"}, status=400)

        cart, _ = Cart.objects.get_or_create(user=user)
        cart_items = cart.items.select_related('product').all()
        
        if not cart_items:
            return Response({"error": "Your cart is empty."}, status=400)

        total_points_cost = sum(item.product.points_price * item.quantity for item in cart_items)
        amount_in_wei = int(total_points_cost * 10**18)

        # 2. Blockchain Pre-check
        current_balance = get_live_balance(student_address)
        if current_balance < total_points_cost:
            return Response({"error": f"Insufficient balance. Need {total_points_cost} EDU."}, status=400)

        try:
            with transaction.atomic():
                # --- Step A: Approval (Student Signs) ---
                token_contract = get_token_contract()
                allowance = token_contract.functions.allowance(student_address, market_address).call()
                
                if allowance < amount_in_wei:
                    approve_tx = token_contract.functions.approve(
                        market_address, amount_in_wei
                    ).build_transaction({
                        'from': student_address, 
                        'nonce': w3.eth.get_transaction_count(student_address),
                        'gas': 100000,
                        'gasPrice': w3.eth.gas_price
                    })
                    
                    signed_approve = w3.eth.account.sign_transaction(approve_tx, db_pvt_key)
                    tx_app_hash = w3.eth.send_raw_transaction(signed_approve.raw_transaction)
                    # Note: In production, use Celery to wait for this instead of blocking
                    w3.eth.wait_for_transaction_receipt(tx_app_hash)

                # --- Step B: Purchase Execution ---
                tx_hash, error = execute_marketplace_purchase(student_address, total_points_cost)
                if error:
                    raise Exception(f"Blockchain execution error: {error}")

                # --- Step C: DB Inventory and Logs ---
                for item in cart_items:
                    # Use select_for_update to prevent race conditions on stock
                    product = Product.objects.select_for_update().get(id=item.product.id)
                    
                    if product.stock is not None:
                        if product.stock < item.quantity:
                            raise Exception(f"Insufficient stock for {product.name}")
                        product.stock -= item.quantity
                        product.save(update_fields=["stock"])

                    # Create Redemption Record
                    Redemption.objects.create(
                        user=user,
                        product=product,
                        quantity=item.quantity,
                        points_spent=product.points_price * item.quantity,
                        status="completed",
                        tx_hash=tx_hash,
                    )

                # Create Audit Log entry
                PointTransaction.objects.create(
                    user=user,
                    tx_type="spend",
                    source="redemption",
                    amount=total_points_cost,
                    description=f"Marketplace purchase: {len(cart_items)} items",
                    on_chain_tx_hash=tx_hash
                )

                # Clear Cart
                cart_items.delete()

            return Response({"message": "Redemption successful!", "tx_hash": tx_hash}, status=200)

        except Exception as e:
            return Response({"error": str(e)}, status=500)
# --- User Redemption History ---
class UserRedemptionHistoryAPIView(generics.ListAPIView):
    serializer_class = RedemptionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Redemption.objects.filter(user=self.request.user).order_by("-created_at")