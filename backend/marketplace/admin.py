# marketplace/admin.py

from django.contrib import admin
from .models import (
    ProductCategory,
    Product,
    Redemption,
    PointTransaction,
)


# -------------------
# Inlines
# -------------------

class RedemptionInline(admin.TabularInline):
    model = Redemption
    extra = 0
    readonly_fields = (
        "user",
        "product",
        "quantity",
        "points_spent",
        "status",
        "tx_hash",
        "created_at",
        "updated_at",
    )
    can_delete = False


# -------------------
# Product Category
# -------------------

@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "is_active", "created_at")
    list_filter = ("is_active",)
    search_fields = ("name", "description")
    prepopulated_fields = {
        "slug": ("name",),
    }


# -------------------
# Product
# -------------------

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "product_type",
        "points_price",
        "stock",
        "is_digital",
        "featured",
        "is_active",
        "created_at",
    )
    list_filter = (
        "product_type",
        "is_active",
        "featured",
        "is_digital",
    )
    search_fields = ("name", "description", "category__name")

    autocomplete_fields = ("category",)

    inlines = [RedemptionInline]

    fieldsets = (
        (None, {
            "fields": (
                "name",
                "description",
                "product_type",
                "category",
            )
        }),
        ("Pricing & Stock", {
            "fields": (
                "points_price",
                "stock",
                "is_digital",
            )
        }),
        ("Delivery Options", {
            "fields": (
                "digital_file",
                "external_url",
            ),
            "classes": ("collapse",),
        }),
        ("Visuals", {
            "fields": ("thumbnail",),
        }),
        ("Meta", {
            "fields": (
                "metadata",
                "featured",
                "is_active",
            ),
        }),
    )


# -------------------
# Redemption
# -------------------

@admin.register(Redemption)
class RedemptionAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "product",
        "quantity",
        "points_spent",
        "status",
        "tx_hash",
        "created_at",
    )
    list_filter = ("status", "product__product_type", "user__institution")
    search_fields = ("user__username", "product__name")
    readonly_fields = (
        "user",
        "product",
        "quantity",
        "points_spent",
        "status",
        "tx_hash",
        "delivery_email",
        "delivery_notes",
        "shipping_address",
        "contact_phone",
    )


# -------------------
# PointTransaction
# -------------------

@admin.register(PointTransaction)
class PointTransactionAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "tx_type",
        "source",
        "amount",
        "on_chain_tx_hash",
        "created_at",
    )
    list_filter = ("tx_type", "source", "user__institution")
    search_fields = ("user__username", "description")
    readonly_fields = (
        "user",
        "tx_type",
        "source",
        "amount",
        "description",
        "on_chain_tx_hash",
        "created_at",
    )
