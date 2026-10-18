import os
import uuid
from functools import wraps
from flask import session, redirect, url_for, flash, request, current_app
from werkzeug.utils import secure_filename
from models import db, User, Product, ProductVariant, Coupon, format_pkr

def get_current_user():
    """Retrieve logged-in user or None."""
    user_id = session.get('user_id')
    if user_id:
        return User.query.get(user_id)
    return None

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('user_id'):
            flash('Please log in to access this page.', 'info')
            return redirect(url_for('auth.login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_id = session.get('user_id')
        if not user_id:
            flash('Admin authentication required.', 'warning')
            return redirect(url_for('auth.login', next=request.url))
        user = User.query.get(user_id)
        if not user or not user.is_admin:
            flash('Access denied. Administrator privileges required.', 'danger')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function

def get_cart_data():
    """Calculate and return full enriched cart data from session."""
    raw_cart = session.get('cart', {})
    items = []
    subtotal = 0.0
    total_qty = 0

    # Ensure items exist in db and calculate subtotal
    # Structure of key: f"{product_id}_{variant_id}" or f"{product_id}_{size}"
    keys_to_remove = []
    for key, item in list(raw_cart.items()):
        product_id = item.get('product_id')
        product = Product.query.get(product_id)
        if not product or not product.is_active:
            keys_to_remove.append(key)
            continue

        unit_price = product.effective_price
        quantity = int(item.get('quantity', 1))
        
        # Check variant stock if available
        variant_id = item.get('variant_id')
        variant = ProductVariant.query.get(variant_id) if variant_id else None
        
        max_stock = variant.stock_quantity if variant else product.stock_quantity
        if quantity > max_stock:
            quantity = max(1, max_stock)
            item['quantity'] = quantity

        item_total = unit_price * quantity
        subtotal += item_total
        total_qty += quantity

        items.append({
            'key': key,
            'product_id': product.id,
            'variant_id': variant.id if variant else None,
            'title': product.title,
            'slug': product.slug,
            'sku': product.sku,
            'image': product.primary_image_url,
            'size': item.get('size', 'Standard'),
            'color': item.get('color', ''),
            'unit_price': unit_price,
            'formatted_unit_price': format_pkr(unit_price),
            'quantity': quantity,
            'max_stock': max_stock,
            'item_total': item_total,
            'formatted_item_total': format_pkr(item_total)
        })

    # Cleanup invalid items
    if keys_to_remove:
        for k in keys_to_remove:
            raw_cart.pop(k, None)
        session['cart'] = raw_cart
        session.modified = True

    # Coupon handling
    coupon_code = session.get('coupon_code')
    coupon = None
    discount_amount = 0.0
    coupon_message = None

    if coupon_code and subtotal > 0:
        coupon = Coupon.query.filter_by(code=coupon_code.upper()).first()
        if coupon:
            discount_amount, coupon_message = coupon.calculate_discount(subtotal)
            if discount_amount == 0.0 and coupon_message:
                session.pop('coupon_code', None)
                session.modified = True
                coupon = None
        else:
            session.pop('coupon_code', None)
            session.modified = True

    # Shipping calculation: Free over threshold
    threshold = current_app.config.get('FREE_SHIPPING_THRESHOLD', 3500.0)
    default_shipping = current_app.config.get('DEFAULT_SHIPPING_FEE', 200.0)
    
    if subtotal >= threshold or (coupon and coupon.code == 'FREESHIP') or subtotal == 0:
        shipping_fee = 0.0
    else:
        shipping_fee = default_shipping

    total_amount = max(0.0, subtotal - discount_amount + shipping_fee)

    # Free shipping progress
    amount_needed_for_free_shipping = max(0.0, threshold - subtotal)
    free_shipping_progress = min(100, int((subtotal / threshold) * 100)) if threshold > 0 else 100

    return {
        'items': items,
        'cart_items': items,
        'count': total_qty,
        'subtotal': subtotal,
        'formatted_subtotal': format_pkr(subtotal),
        'discount_amount': discount_amount,
        'formatted_discount': format_pkr(discount_amount),
        'coupon': coupon.to_dict() if coupon else None,
        'coupon_code': coupon.code if coupon else None,
        'coupon_message': coupon_message,
        'shipping_fee': shipping_fee,
        'formatted_shipping': "FREE" if shipping_fee == 0 and subtotal > 0 else format_pkr(shipping_fee),
        'total_amount': total_amount,
        'formatted_total': format_pkr(total_amount),
        'free_shipping_threshold': threshold,
        'amount_needed_for_free_shipping': amount_needed_for_free_shipping,
        'formatted_amount_needed': format_pkr(amount_needed_for_free_shipping),
        'free_shipping_progress': free_shipping_progress,
        'qualifies_for_free_shipping': subtotal >= threshold
    }

def save_upload_file(file_storage):
    """Save uploaded image to static/images/uploads and return relative URL path."""
    if not file_storage or file_storage.filename == '':
        return None
        
    ext = file_storage.filename.rsplit('.', 1)[-1].lower()
    allowed = current_app.config.get('ALLOWED_EXTENSIONS', {'png', 'jpg', 'jpeg', 'webp'})
    if ext not in allowed:
        return None

    filename = f"{uuid.uuid4().hex[:12]}_{secure_filename(file_storage.filename)}"
    upload_dir = current_app.config.get('UPLOAD_FOLDER')
    os.makedirs(upload_dir, exist_ok=True)
    filepath = os.path.join(upload_dir, filename)
    file_storage.save(filepath)
    return f"/static/images/uploads/{filename}"
