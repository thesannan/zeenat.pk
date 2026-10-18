import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'zeenat-luxury-pakistan-secret-key-2026-fashion')
    
    # Database config (defaults to SQLite, easily migrated to PostgreSQL via DATABASE_URL)
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL', 
        f"sqlite:///{BASE_DIR / 'zeenat.db'}"
    )
    # Fix for Heroku/Render postgres:// -> postgresql://
    if SQLALCHEMY_DATABASE_URI and SQLALCHEMY_DATABASE_URI.startswith("postgres://"):
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace("postgres://", "postgresql://", 1)
        
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Upload folder
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'images', 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max upload
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp', 'gif'}
    
    # Store settings
    CURRENCY = 'PKR'
    CURRENCY_SYMBOL = 'Rs.'
    FREE_SHIPPING_THRESHOLD = 3500.0  # Free shipping nationwide for orders >= PKR 3,500
    DEFAULT_SHIPPING_FEE = 200.0       # Standard delivery PKR 200
    
    # Payment gateway configurations (Stripe / Bank / COD)
    STRIPE_PUBLIC_KEY = os.environ.get('STRIPE_PUBLIC_KEY', '')
    STRIPE_SECRET_KEY = os.environ.get('STRIPE_SECRET_KEY', '')
    ENABLE_ONLINE_PAYMENTS = bool(os.environ.get('STRIPE_SECRET_KEY'))
    
    # Brand details
    BRAND_NAME = "ZEENAT"
    BRAND_TAGLINE = "Luxury Pret & Unstitched Couture"
    BRAND_PHONE = "+92 (21) 3587-9921"
    BRAND_WHATSAPP = "+92 300 1234567"
    BRAND_EMAIL = "care@zeenatpakistan.com"
    BRAND_ADDRESS = "Plot 14-C, 7th Zamzama Commercial Lane, Phase 5, D.H.A, Karachi, Pakistan"
