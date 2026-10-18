from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def format_pkr(value):
    """Format numeric value as Pakistani Rupee string (e.g. Rs. 4,950)."""
    try:
        val = float(value or 0)
        return f"Rs. {val:,.0f}"
    except (ValueError, TypeError):
        return "Rs. 0"

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(30), nullable=True)
    is_admin = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    orders = db.relationship('Order', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    addresses = db.relationship('Address', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    wishlist_items = db.relationship('WishlistItem', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    reviews = db.relationship('Review', backref='user', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            'id': self.id,
            'full_name': self.full_name,
            'email': self.email,
            'phone': self.phone,
            'is_admin': self.is_admin,
            'created_at': self.created_at.strftime('%Y-%m-%d')
        }


class Address(db.Model):
    __tablename__ = 'addresses'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    label = db.Column(db.String(50), default='Home') # Home, Office
    recipient_name = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(30), nullable=False)
    address_line = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    province = db.Column(db.String(100), default='Sindh')
    postal_code = db.Column(db.String(20), nullable=True)
    is_default = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    slug = db.Column(db.String(120), unique=True, nullable=False, index=True)
    description = db.Column(db.Text, nullable=True)
    image_url = db.Column(db.String(500), nullable=True)
    banner_url = db.Column(db.String(500), nullable=True)
    is_featured = db.Column(db.Boolean, default=True)
    display_order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    products = db.relationship('Product', backref='category', lazy='dynamic')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'slug': self.slug,
            'description': self.description,
            'image_url': self.image_url,
            'banner_url': self.banner_url,
            'products_count': self.products.filter_by(is_active=True).count()
        }


class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(250), unique=True, nullable=False, index=True)
    sku = db.Column(db.String(50), unique=True, nullable=False, index=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    
    # Pricing
    original_price = db.Column(db.Float, nullable=False)
    discount_price = db.Column(db.Float, nullable=True) # If set, this is the sale price
    
    # Description & Specification
    short_description = db.Column(db.String(300), nullable=True)
    description = db.Column(db.Text, nullable=False)
    fabric = db.Column(db.String(100), nullable=True) # Lawn, Chiffon, Jacquard, Silk, Organza, Cambric
    pieces = db.Column(db.String(50), default='1-Piece') # 1-Piece, 2-Piece, 3-Piece
    fit = db.Column(db.String(50), default='Regular Fit') # Regular, Loose, Kalidar, Straight
    care_instructions = db.Column(db.Text, nullable=True)
    
    # Flags & Stats
    stock_quantity = db.Column(db.Integer, default=50)
    is_active = db.Column(db.Boolean, default=True)
    is_featured = db.Column(db.Boolean, default=False)
    is_new_arrival = db.Column(db.Boolean, default=False)
    is_best_seller = db.Column(db.Boolean, default=False)
    is_sale = db.Column(db.Boolean, default=False)
    
    rating_avg = db.Column(db.Float, default=5.0)
    reviews_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    images = db.relationship('ProductImage', backref='product', lazy='joined', cascade='all, delete-orphan', order_by='ProductImage.display_order')
    variants = db.relationship('ProductVariant', backref='product', lazy='joined', cascade='all, delete-orphan')
    reviews = db.relationship('Review', backref='product', lazy='dynamic', cascade='all, delete-orphan')

    @property
    def effective_price(self):
        """Current payable price (discount price if present, else original price)."""
        if self.discount_price and self.discount_price > 0 and self.discount_price < self.original_price:
            return self.discount_price
        return self.original_price

    @property
    def discount_percentage(self):
        """Calculate discount % if on sale."""
        if self.discount_price and self.discount_price < self.original_price:
            pct = round(((self.original_price - self.discount_price) / self.original_price) * 100)
            return pct
        return 0

    @property
    def primary_image_url(self):
        """Get primary product image or fallback."""
        for img in self.images:
            if img.is_primary:
                return img.image_url
        if self.images:
            return self.images[0].image_url
        return "https://images.unsplash.com/photo-1539109136881-3be0616acf4b?auto=format&fit=crop&w=800&q=80"

    @property
    def secondary_image_url(self):
        """Get secondary image for hover switch or fallback."""
        if len(self.images) > 1:
            return self.images[1].image_url
        return self.primary_image_url

    @property
    def available_sizes(self):
        """List of sizes currently available for this product."""
        sizes = [v.size for v in self.variants if v.stock_quantity > 0]
        return list(dict.fromkeys(sizes)) if sizes else ['Standard']

    @property
    def available_colors(self):
        """List of distinct colors for this product."""
        colors = []
        seen = set()
        for v in self.variants:
            if v.color_name and v.color_name not in seen:
                seen.add(v.color_name)
                colors.append({'name': v.color_name, 'hex': v.color_hex})
        return colors

    @property
    def in_stock(self):
        return self.stock_quantity > 0

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'slug': self.slug,
            'sku': self.sku,
            'category_name': self.category.name if self.category else '',
            'category_slug': self.category.slug if self.category else '',
            'original_price': self.original_price,
            'discount_price': self.discount_price,
            'effective_price': self.effective_price,
            'discount_percentage': self.discount_percentage,
            'formatted_price': format_pkr(self.effective_price),
            'formatted_original_price': format_pkr(self.original_price),
            'primary_image': self.primary_image_url,
            'secondary_image': self.secondary_image_url,
            'images': [img.image_url for img in self.images],
            'fabric': self.fabric,
            'pieces': self.pieces,
            'in_stock': self.in_stock,
            'stock_quantity': self.stock_quantity,
            'available_sizes': self.available_sizes,
            'available_colors': self.available_colors,
            'rating_avg': self.rating_avg,
            'reviews_count': self.reviews_count,
            'is_sale': self.is_sale or (self.discount_percentage > 0),
            'is_new_arrival': self.is_new_arrival,
            'is_best_seller': self.is_best_seller
        }


class ProductImage(db.Model):
    __tablename__ = 'product_images'

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id', ondelete='CASCADE'), nullable=False)
    image_url = db.Column(db.String(600), nullable=False)
    alt_text = db.Column(db.String(200), nullable=True)
    display_order = db.Column(db.Integer, default=0)
    is_primary = db.Column(db.Boolean, default=False)


class ProductVariant(db.Model):
    __tablename__ = 'product_variants'

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id', ondelete='CASCADE'), nullable=False)
    size = db.Column(db.String(30), nullable=False, default='Standard') # XS, S, M, L, XL, Unstitched
    color_name = db.Column(db.String(50), nullable=True) # Teal, Maroon, Ivory, Jet Black
    color_hex = db.Column(db.String(20), nullable=True) # #1A3636, #800000, #FFFFF0
    stock_quantity = db.Column(db.Integer, default=15)
    sku_suffix = db.Column(db.String(20), nullable=True)


class Coupon(db.Model):
    __tablename__ = 'coupons'

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50), unique=True, nullable=False, index=True)
    description = db.Column(db.String(255), nullable=True)
    discount_type = db.Column(db.String(20), default='percentage') # percentage or fixed
    discount_value = db.Column(db.Float, nullable=False) # e.g. 15 for 15%, or 500 for Rs. 500
    min_order_value = db.Column(db.Float, default=0.0)
    max_discount_amount = db.Column(db.Float, nullable=True) # Cap for percentage discounts
    is_active = db.Column(db.Boolean, default=True)
    valid_from = db.Column(db.DateTime, default=datetime.utcnow)
    valid_until = db.Column(db.DateTime, nullable=True)
    usage_limit = db.Column(db.Integer, default=1000)
    usage_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def calculate_discount(self, subtotal):
        """Calculate discount amount in PKR given cart subtotal."""
        if not self.is_active:
            return 0.0, "Coupon is no longer active."
        if self.valid_until and datetime.utcnow() > self.valid_until:
            return 0.0, "Coupon has expired."
        if self.usage_count >= self.usage_limit:
            return 0.0, "Coupon usage limit reached."
        if subtotal < self.min_order_value:
            return 0.0, f"Minimum order amount of {format_pkr(self.min_order_value)} required."

        if self.discount_type == 'percentage':
            disc = (subtotal * self.discount_value) / 100.0
            if self.max_discount_amount and disc > self.max_discount_amount:
                disc = self.max_discount_amount
            return round(disc, 2), "Discount applied successfully!"
        else:
            disc = min(self.discount_value, subtotal)
            return round(disc, 2), "Discount applied successfully!"

    def to_dict(self):
        return {
            'id': self.id,
            'code': self.code,
            'description': self.description,
            'discount_type': self.discount_type,
            'discount_value': self.discount_value,
            'min_order_value': self.min_order_value
        }


class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    order_number = db.Column(db.String(50), unique=True, nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
    
    # Customer Details
    customer_name = db.Column(db.String(120), nullable=False)
    customer_email = db.Column(db.String(120), nullable=False)
    customer_phone = db.Column(db.String(30), nullable=False)
    
    # Shipping Address
    shipping_address = db.Column(db.String(255), nullable=False)
    shipping_city = db.Column(db.String(100), nullable=False)
    shipping_province = db.Column(db.String(100), default='Pakistan')
    shipping_postal_code = db.Column(db.String(20), nullable=True)
    order_notes = db.Column(db.Text, nullable=True)
    
    # Financials
    subtotal = db.Column(db.Float, nullable=False)
    discount_amount = db.Column(db.Float, default=0.0)
    coupon_code = db.Column(db.String(50), nullable=True)
    shipping_fee = db.Column(db.Float, default=200.0)
    total_amount = db.Column(db.Float, nullable=False)
    
    # Payment & Fulfillment
    payment_method = db.Column(db.String(30), default='cod') # cod, card, bank_transfer
    payment_status = db.Column(db.String(30), default='pending') # pending, paid, refunded, failed
    order_status = db.Column(db.String(30), default='pending') # pending, processing, shipped, delivered, cancelled
    
    # Logistics Tracking
    courier_name = db.Column(db.String(100), default='TCS Express')
    tracking_number = db.Column(db.String(100), nullable=True)
    admin_notes = db.Column(db.Text, nullable=True)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    items = db.relationship('OrderItem', backref='order', lazy='joined', cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'order_number': self.order_number,
            'customer_name': self.customer_name,
            'customer_email': self.customer_email,
            'customer_phone': self.customer_phone,
            'shipping_address': f"{self.shipping_address}, {self.shipping_city}",
            'subtotal': self.subtotal,
            'discount_amount': self.discount_amount,
            'shipping_fee': self.shipping_fee,
            'total_amount': self.total_amount,
            'formatted_total': format_pkr(self.total_amount),
            'payment_method': self.payment_method.upper(),
            'payment_status': self.payment_status.title(),
            'order_status': self.order_status.title(),
            'tracking_number': self.tracking_number,
            'courier_name': self.courier_name,
            'items_count': sum(i.quantity for i in self.items),
            'created_at': self.created_at.strftime('%d %b %Y, %I:%M %p')
        }


class OrderItem(db.Model):
    __tablename__ = 'order_items'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id', ondelete='CASCADE'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id', ondelete='SET NULL'), nullable=True)
    
    product_title = db.Column(db.String(200), nullable=False)
    product_sku = db.Column(db.String(50), nullable=True)
    product_image = db.Column(db.String(500), nullable=True)
    size = db.Column(db.String(30), default='Standard')
    color = db.Column(db.String(50), nullable=True)
    unit_price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, default=1)
    total_price = db.Column(db.Float, nullable=False)

    @property
    def formatted_unit_price(self):
        return format_pkr(self.unit_price)

    @property
    def formatted_total_price(self):
        return format_pkr(self.total_price)


class Review(db.Model):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id', ondelete='CASCADE'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
    customer_name = db.Column(db.String(120), nullable=False)
    customer_city = db.Column(db.String(100), default='Karachi')
    rating = db.Column(db.Integer, default=5) # 1 - 5 stars
    title = db.Column(db.String(200), nullable=True)
    comment = db.Column(db.Text, nullable=False)
    is_verified_buyer = db.Column(db.Boolean, default=True)
    is_approved = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class WishlistItem(db.Model):
    __tablename__ = 'wishlist_items'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id', ondelete='CASCADE'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    product = db.relationship('Product', lazy='joined')


class Banner(db.Model):
    __tablename__ = 'banners'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    subtitle = db.Column(db.String(250), nullable=True)
    badge_text = db.Column(db.String(100), nullable=True) # e.g. "NEW ARRIVALS 2026"
    button_text = db.Column(db.String(50), default='Shop Now')
    button_link = db.Column(db.String(250), default='/shop')
    image_url = db.Column(db.String(600), nullable=False)
    position = db.Column(db.String(50), default='hero') # hero, promo_strip, featured_grid
    is_active = db.Column(db.Boolean, default=True)
    display_order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
