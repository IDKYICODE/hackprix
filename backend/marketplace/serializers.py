from rest_framework import serializers
from .models import ProductCategory, Product, Redemption, Cart, CartItem

class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ["id", "name", "slug", "description", "is_active"]
        read_only_fields = ["id", "slug", "created_at"]

class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="category.name", read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "category",
            "category_name",
            "name",
            "description",
            "product_type",
            "points_price",
            "stock",
            "is_digital",
            "digital_file",
            "external_url",
            "thumbnail",
            "metadata",
            "is_active",
            "featured",
            "created_at",
            "updated_at",
            "is_unlimited",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
            "is_unlimited",
            "category_name",
        ]

class RedemptionSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.name", read_only=True)
    user_username = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = Redemption
        fields = [
            "id",
            "user",
            "user_username",
            "product",
            "product_name",
            "quantity",
            "points_spent",
            "status",
            "tx_hash",
            "delivery_email",
            "delivery_notes",
            "shipping_address",
            "contact_phone",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "user",
            "user_username",
            "points_spent",
            "status",
            "tx_hash",
            "created_at",
            "updated_at",
        ]

class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    total_points = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ["id", "product", "quantity", "total_points"]
    
    def get_total_points(self, obj):
        return obj.quantity * obj.product.points_price

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_cart_points = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ["id", "user", "items", "total_cart_points", "created_at"]
    
    def get_total_cart_points(self, obj):
        return sum(item.quantity * item.product.points_price for item in obj.items.all())