import os
from flask import Flask, render_template, session
from config import Config
from models import db, Category, WishlistItem, format_pkr
from utils import get_current_user, get_cart_data

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)

    # Register Blueprints
    from routes.main import main_bp
    from routes.cart import cart_bp
    from routes.checkout import checkout_bp
    from routes.auth import auth_bp
    from routes.admin import admin_bp
    from routes.api import api_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(cart_bp)
    app.register_blueprint(checkout_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(api_bp)

    # Custom Template Filters
    @app.template_filter('pkr')
    def pkr_filter(value):
        return format_pkr(value)

    # Global Context Processor
    @app.context_processor
    def inject_global_data():
        current_user = get_current_user()
        cart_info = get_cart_data()

        # Wishlist count
        if current_user:
            wishlist_count = WishlistItem.query.filter_by(user_id=current_user.id).count()
        else:
            wishlist_count = len(session.get('guest_wishlist', []))

        # Categories for navigation mega menu
        nav_categories = Category.query.order_by(Category.display_order).all()

        return {
            'current_user': current_user,
            'cart': cart_info,
            'wishlist_count': wishlist_count,
            'nav_categories': nav_categories,
            'brand_name': app.config.get('BRAND_NAME', 'ZEENAT'),
            'brand_tagline': app.config.get('BRAND_TAGLINE', 'Luxury Pret & Unstitched Couture'),
            'brand_phone': app.config.get('BRAND_PHONE'),
            'brand_whatsapp': app.config.get('BRAND_WHATSAPP'),
            'brand_email': app.config.get('BRAND_EMAIL'),
            'brand_address': app.config.get('BRAND_ADDRESS')
        }

    # Error handlers
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def server_error(e):
        return render_template('500.html'), 500

    # CLI command for seeding
    @app.cli.command('seed')
    def seed_cmd():
        """Seed the database with Pakistani fashion collections and admin."""
        from seed_data import seed_database
        seed_database(app)

    return app

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # Auto seed if empty
        from seed_data import seed_database
        seed_database(app)
    
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
