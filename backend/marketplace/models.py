# marketplace/models.py

from django.conf import settings
from django.db import models


# -------------------
# Product Category
# -------------------

class ProductCategory(models.Model):
    """
    Category for grouping products.
    e.g. 'E-Books', 'Mock Tests', 'Courses', 'Stationery'
    """
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(
        max_length=120,
        unique=True,
        help_text="URL-friendly identifier, e.g. 'ebooks', 'mock-tests'",
    )
    description = models.TextField(blank=True)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Product categories"
        ordering = ["name"]

    def __str__(self):
        return self.name


# -------------------
# Product
# -------------------

class Product(models.Model):
    """
    Item that can be redeemed using points.
    Can be digital (ebooks, PDFs, course access) or physical.
    """
    PRODUCT_TYPE_CHOICES = [
        ("ebook", "E-Book"),
        ("pdf", "PDF / Notes"),
        ("course", "Course Access"),
        ("mock_test", "Mock Test / Practice Pack"),
        ("voucher", "Voucher / Coupon"),
        ("physical", "Physical Item"),
        ("other", "Other"),
    ]

    category = models.ForeignKey(
        ProductCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="products",
    )

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    product_type = models.CharField(
        max_length=20,
        choices=PRODUCT_TYPE_CHOICES,
        default="ebook",
    )

    # points cost to redeem this product
    points_price = models.PositiveIntegerField(
        help_text="How many points are required to redeem one unit of this product."
    )

    # If None for stock, treat as unlimited (for digital items)
    stock = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Leave blank for unlimited (digital) items.",
    )

    is_digital = models.BooleanField(
        default=True,
        help_text="If false, assume this is a physical item.",
    )

    # Digital delivery
    digital_file = models.FileField(
        upload_to="marketplace/digital_products/",
        blank=True,
        null=True,
        help_text="Upload file for e-books/notes if applicable.",
    )
    external_url = models.URLField(
        blank=True,
        null=True,
        help_text="External link (LMS, course platform, etc.) if applicable.",
    )

    # Visuals
    thumbnail = models.ImageField(
        upload_to="marketplace/product_thumbnails/",
        blank=True,
        null=True,
    )

    # Optional metadata (for integration, extra attributes)
    metadata = models.JSONField(
        blank=True,
        null=True,
        help_text="Optional extra data (e.g. 'publisher', 'subject', etc.).",
    )

    is_active = models.BooleanField(default=True)
    featured = models.BooleanField(
        default=False,
        help_text="If true, can be highlighted in the marketplace UI.",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.name

    @property
    def is_unlimited(self) -> bool:
        return self.stock is None


# -------------------
# Redemption (Order)
# -------------------

class Redemption(models.Model):
    """
    Represents a user redeeming a product using points.
    """
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("completed", "Completed"),
        ("failed", "Failed"),
        ("cancelled", "Cancelled"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="redemptions",
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name="redemptions",
    )

    quantity = models.PositiveIntegerField(default=1)

    points_spent = models.PositiveIntegerField(
        help_text="Total points spent for this redemption (quantity * product.points_price)."
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending",
    )

    # Blockchain transaction hash for spending points
    tx_hash = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="On-chain transaction hash for this redemption.",
    )

    # Delivery details
    delivery_email = models.EmailField(
        blank=True,
        null=True,
        help_text="Where digital items / codes may be sent.",
    )
    delivery_notes = models.TextField(
        blank=True,
        null=True,
        help_text="Optional notes related to delivery or fulfilment.",
    )

    # For physical items (optional)
    shipping_address = models.TextField(
        blank=True,
        null=True,
        help_text="Optional: address for physical items.",
    )
    contact_phone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user} -> {self.product} ({self.points_spent} pts)"


# -------------------
# Point Transaction Log (Optional but useful)
# -------------------

class PointTransaction(models.Model):
    """
    Generic log of points movement for a user.
    This helps with audit/history:
    - quiz reward
    - attendance reward
    - marketplace spend
    - manual adjustment
    """
    TRANSACTION_TYPE_CHOICES = [
        ("earn", "Earn"),
        ("spend", "Spend"),
        ("adjust", "Adjust"),
    ]

    SOURCE_CHOICES = [
        ("quiz", "Quiz"),
        ("attendance", "Attendance"),
        ("redemption", "Redemption"),
        ("manual", "Manual"),
        ("other", "Other"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="point_transactions",
    )

    tx_type = models.CharField(
        max_length=10,
        choices=TRANSACTION_TYPE_CHOICES,
    )

    source = models.CharField(
        max_length=20,
        choices=SOURCE_CHOICES,
        default="other",
    )

    amount = models.PositiveIntegerField(
        help_text="Number of points earned/spent/adjusted."
    )

    description = models.TextField(
        blank=True,
        null=True,
        help_text="Short explanation, e.g. 'Quiz 1 reward', 'Redeemed E-book X'.",
    )

    # Optional on-chain hash (can also be used for quiz/attendance tx)
    on_chain_tx_hash = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Blockchain hash for this points operation, if applicable.",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        sign = "+" if self.tx_type == "earn" else "-"
        return f"{self.user} {sign}{self.amount} ({self.source})"


# -------------------
# Cart
# -------------------

class Cart(models.Model):
    """
    A user's shopping cart.
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="cart",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart for {self.user.username}"


class CartItem(models.Model):
    """
    An item in a user's shopping cart.
    """
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name="items",
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="cart_items",
    )
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ("cart", "product")

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in {self.cart}"