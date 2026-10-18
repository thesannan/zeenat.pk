import datetime
from models import db, User, Category, Product, ProductImage, ProductVariant, Coupon, Review, Banner, Address

def seed_database(app):
    with app.app_context():
        db.create_all()

        # Check if already seeded
        if User.query.filter_by(email='admin@zeenat.pk').first():
            print("Database already contains seed data.")
            return

        print("Seeding Zeenat Pakistan database...")

        # 1. Create Users
        admin_user = User(
            full_name="Admin Zeenat",
            email="admin@zeenat.pk",
            phone="+92 300 0000000",
            is_admin=True,
            is_active=True
        )
        admin_user.set_password("admin123")

        customer_user = User(
            full_name="Ayesha Khan",
            email="ayesha@example.com",
            phone="+92 321 8899221",
            is_admin=False,
            is_active=True
        )
        customer_user.set_password("customer123")

        db.session.add_all([admin_user, customer_user])
        db.session.commit()

        # Add customer saved address
        customer_address = Address(
            user_id=customer_user.id,
            label="Home",
            recipient_name="Ayesha Khan",
            phone="+92 321 8899221",
            address_line="House 42-B, Block 4, Clifton",
            city="Karachi",
            province="Sindh",
            postal_code="75600",
            is_default=True
        )
        db.session.add(customer_address)

        # 2. Categories
        categories_data = [
            {
                "name": "Ready to Wear",
                "slug": "ready-to-wear",
                "description": "Exquisite ready-to-wear kurtis, 2-piece and 3-piece tailored ensembles.",
                "image_url": "https://images.unsplash.com/photo-1583391733956-3750e0ff4e8b?auto=format&fit=crop&w=800&q=80",
                "banner_url": "https://images.unsplash.com/photo-1490481651871-ab68de25d43d?auto=format&fit=crop&w=1600&q=80",
                "is_featured": True,
                "display_order": 1
            },
            {
                "name": "Unstitched",
                "slug": "unstitched",
                "description": "Premium 3-piece and 2-piece unstitched luxury lawn, jacquard and chiffon collections.",
                "image_url": "https://images.unsplash.com/photo-1617627143750-d86bc21e42bb?auto=format&fit=crop&w=800&q=80",
                "banner_url": "https://images.unsplash.com/photo-1469334031218-e382a71b716b?auto=format&fit=crop&w=1600&q=80",
                "is_featured": True,
                "display_order": 2
            },
            {
                "name": "Casual Wear",
                "slug": "casual-wear",
                "description": "Breathable daily lawn, printed shirts, and effortless solid cotton tunics.",
                "image_url": "https://images.unsplash.com/photo-1515886657613-9f3515b0c78f?auto=format&fit=crop&w=800&q=80",
                "banner_url": "https://images.unsplash.com/photo-1445205170230-053b83016050?auto=format&fit=crop&w=1600&q=80",
                "is_featured": True,
                "display_order": 3
            },
            {
                "name": "Formal Wear",
                "slug": "formal-wear",
                "description": "Festive couture, zari embroideries, opulent organza, and ceremonial silks.",
                "image_url": "https://images.unsplash.com/photo-1566174053879-31528523f8ae?auto=format&fit=crop&w=800&q=80",
                "banner_url": "https://images.unsplash.com/photo-1483985988355-763728e1935b?auto=format&fit=crop&w=1600&q=80",
                "is_featured": True,
                "display_order": 4
            },
            {
                "name": "Accessories",
                "slug": "accessories",
                "description": "Handcrafted dupattas, pure velvet shawls, clutches, and traditional footwear.",
                "image_url": "https://images.unsplash.com/photo-1548036328-c9fa89d128fa?auto=format&fit=crop&w=800&q=80",
                "banner_url": "https://images.unsplash.com/photo-1509631179647-0177331693ae?auto=format&fit=crop&w=1600&q=80",
                "is_featured": True,
                "display_order": 5
            },
            {
                "name": "Sale",
                "slug": "sale",
                "description": "Special clearance and seasonal markdowns with up to 40% OFF.",
                "image_url": "https://images.unsplash.com/photo-1472851294608-062f824d29cc?auto=format&fit=crop&w=800&q=80",
                "banner_url": "https://images.unsplash.com/photo-1472851294608-062f824d29cc?auto=format&fit=crop&w=1600&q=80",
                "is_featured": True,
                "display_order": 6
            }
        ]

        cat_objs = {}
        for cdata in categories_data:
            cat = Category(**cdata)
            db.session.add(cat)
            cat_objs[cat.slug] = cat
        db.session.commit()

        # 3. Homepage Banners
        banners_data = [
            {
                "title": "FESTIVE PRET '26",
                "subtitle": "Discover intricate threadwork, gilded accents, and hand-tailored luxury silhouettes.",
                "badge_text": "NEW COLLECTION",
                "button_text": "SHOP PRET",
                "button_link": "/category/ready-to-wear",
                "image_url": "https://images.unsplash.com/photo-1490481651871-ab68de25d43d?auto=format&fit=crop&w=1600&q=80",
                "position": "hero",
                "display_order": 1
            },
            {
                "title": "UNSTITCHED LUXURY LAWN",
                "subtitle": "Pure Swiss voile, digital prints, and organza embroidered dupattas for timeless grace.",
                "badge_text": "SUMMER EDIT",
                "button_text": "EXPLORE UNSTITCHED",
                "button_link": "/category/unstitched",
                "image_url": "https://images.unsplash.com/photo-1469334031218-e382a71b716b?auto=format&fit=crop&w=1600&q=80",
                "position": "hero",
                "display_order": 2
            },
            {
                "title": "MID-SEASON CLEARANCE",
                "subtitle": "Enjoy flat discounts on selected kurtis, 2-piece suits, and unstitched fabrics.",
                "badge_text": "UP TO 40% OFF",
                "button_text": "SHOP SALE",
                "button_link": "/category/sale",
                "image_url": "https://images.unsplash.com/photo-1483985988355-763728e1935b?auto=format&fit=crop&w=1600&q=80",
                "position": "hero",
                "display_order": 3
            }
        ]

        for bdata in banners_data:
            b = Banner(**bdata)
            db.session.add(b)

        # 4. Products Data
        products_data = [
            # Ready to Wear
            {
                "title": "Embroidered Lawn 3-Piece Suit - Mah-e-Noor",
                "slug": "embroidered-lawn-3pc-mah-e-noor",
                "sku": "ZN-RTW-001",
                "category_slug": "ready-to-wear",
                "original_price": 7990.0,
                "discount_price": 6490.0,
                "short_description": "Graceful teal embroidered 3-piece lawn shirt paired with cambric trousers and printed chiffon dupatta.",
                "description": "Crafted from super-fine breathable lawn, this 3-piece suit features delicate resham floral embroidery along the neckline and hemline. Paired with a featherlight digital printed chiffon dupatta and tailored dyed trousers. Perfect for festive daytime gatherings and smart semi-formal wear.",
                "fabric": "Superfine Lawn & Pure Chiffon",
                "pieces": "3-Piece",
                "fit": "Straight Silhouette",
                "care_instructions": "Dry clean recommended. Hand wash in cold water with mild detergent. Do not bleach. Iron on medium reverse.",
                "stock_quantity": 45,
                "is_featured": True,
                "is_new_arrival": True,
                "is_best_seller": True,
                "is_sale": True,
                "rating_avg": 4.9,
                "reviews_count": 18,
                "images": [
                    "https://images.unsplash.com/photo-1583391733956-3750e0ff4e8b?auto=format&fit=crop&w=800&q=80",
                    "https://images.unsplash.com/photo-1566174053879-31528523f8ae?auto=format&fit=crop&w=800&q=80",
                    "https://images.unsplash.com/photo-1509631179647-0177331693ae?auto=format&fit=crop&w=800&q=80"
                ],
                "variants": [
                    {"size": "XS", "color_name": "Teal Breeze", "color_hex": "#005F73", "stock": 10},
                    {"size": "S", "color_name": "Teal Breeze", "color_hex": "#005F73", "stock": 15},
                    {"size": "M", "color_name": "Teal Breeze", "color_hex": "#005F73", "stock": 12},
                    {"size": "L", "color_name": "Teal Breeze", "color_hex": "#005F73", "stock": 8}
                ]
            },
            {
                "title": "Raw Silk Matching Co-Ord Set - Onyx Noir",
                "slug": "raw-silk-matching-coord-set-onyx",
                "sku": "ZN-RTW-002",
                "category_slug": "ready-to-wear",
                "original_price": 5990.0,
                "discount_price": None,
                "short_description": "Contemporary solid 2-piece co-ord set in Korean raw silk with band collar and mother-of-pearl buttons.",
                "description": "An epitome of understated luxury. Tailored in high-grade Korean raw silk with a relaxed drop-shoulder cut, delicate sleeve buttoning, and matching straight culottes. Style with bold gold jewelry or mules for an elevated minimalist presence.",
                "fabric": "Korean Raw Silk Blend",
                "pieces": "2-Piece",
                "fit": "Relaxed Contemporary Fit",
                "care_instructions": "Machine wash on delicate cycle or dry clean. Low iron with protective cloth.",
                "stock_quantity": 60,
                "is_featured": True,
                "is_new_arrival": True,
                "is_best_seller": True,
                "is_sale": False,
                "rating_avg": 4.8,
                "reviews_count": 12,
                "images": [
                    "https://images.unsplash.com/photo-1539109136881-3be0616acf4b?auto=format&fit=crop&w=800&q=80",
                    "https://images.unsplash.com/photo-1515886657613-9f3515b0c78f?auto=format&fit=crop&w=800&q=80"
                ],
                "variants": [
                    {"size": "S", "color_name": "Onyx Black", "color_hex": "#111111", "stock": 20},
                    {"size": "M", "color_name": "Onyx Black", "color_hex": "#111111", "stock": 25},
                    {"size": "L", "color_name": "Onyx Black", "color_hex": "#111111", "stock": 15}
                ]
            },
            {
                "title": "Jacquard 2-Piece Shirt & Dupatta - Royal Emerald",
                "slug": "jacquard-2pc-royal-emerald",
                "sku": "ZN-RTW-003",
                "category_slug": "ready-to-wear",
                "original_price": 5490.0,
                "discount_price": 4690.0,
                "short_description": "Woven gold jacquard shirt with laced sleeve cuffs accompanied by a self-weave jacquard dupatta.",
                "description": "Rich jewel tones meet traditional Pakistani craftsmanship. The woven metallic gold yarn forms subtle geometric motifs over deep emerald fabric. Detailed with scalloped organza laces on sleeve cuffs and hem.",
                "fabric": "Zari Weave Jacquard",
                "pieces": "2-Piece",
                "fit": "A-Line Flared Kurta",
                "care_instructions": "Dry clean only to maintain gold zari luster.",
                "stock_quantity": 35,
                "is_featured": False,
                "is_new_arrival": True,
                "is_best_seller": False,
                "is_sale": True,
                "rating_avg": 5.0,
                "reviews_count": 9,
                "images": [
                    "https://images.unsplash.com/photo-1558769132-cb1aea458c5e?auto=format&fit=crop&w=800&q=80",
                    "https://images.unsplash.com/photo-1583391733956-3750e0ff4e8b?auto=format&fit=crop&w=800&q=80"
                ],
                "variants": [
                    {"size": "S", "color_name": "Emerald Green", "color_hex": "#0A5C36", "stock": 10},
                    {"size": "M", "color_name": "Emerald Green", "color_hex": "#0A5C36", "stock": 15},
                    {"size": "L", "color_name": "Emerald Green", "color_hex": "#0A5C36", "stock": 10}
                ]
            },
            {
                "title": "Digital Printed Cambric Kurti - Saffron Bloom",
                "slug": "digital-printed-cambric-kurti-saffron",
                "sku": "ZN-RTW-004",
                "category_slug": "ready-to-wear",
                "original_price": 2790.0,
                "discount_price": 2290.0,
                "short_description": "Vibrant floral printed cambric kurti with slit neckline and contrast bead embellishments.",
                "description": "Brighten your everyday look with this eye-catching digital printed cambric tunic. Tailored in an effortless straight silhouette with notched mandarin collar and wooden button accents.",
                "fabric": "100% Cotton Cambric",
                "pieces": "1-Piece",
                "fit": "Straight Kurti",
                "care_instructions": "Gentle machine wash with like colors.",
                "stock_quantity": 70,
                "is_featured": False,
                "is_new_arrival": False,
                "is_best_seller": True,
                "is_sale": True,
                "rating_avg": 4.7,
                "reviews_count": 22,
                "images": [
                    "https://images.unsplash.com/photo-1572804013309-59a88b7e92f1?auto=format&fit=crop&w=800&q=80",
                    "https://images.unsplash.com/photo-1515886657613-9f3515b0c78f?auto=format&fit=crop&w=800&q=80"
                ],
                "variants": [
                    {"size": "XS", "color_name": "Saffron Ochre", "color_hex": "#E3A857", "stock": 15},
                    {"size": "S", "color_name": "Saffron Ochre", "color_hex": "#E3A857", "stock": 25},
                    {"size": "M", "color_name": "Saffron Ochre", "color_hex": "#E3A857", "stock": 20},
                    {"size": "L", "color_name": "Saffron Ochre", "color_hex": "#E3A857", "stock": 10}
                ]
            },

            # Unstitched Collection
            {
                "title": "Unstitched 3-Piece Luxury Lawn with Chiffon Dupatta - Gul-e-Daudi",
                "slug": "unstitched-3pc-luxury-lawn-gul-e-daudi",
                "sku": "ZN-UST-101",
                "category_slug": "unstitched",
                "original_price": 5490.0,
                "discount_price": 4690.0,
                "short_description": "Unstitched embroidered lawn shirt front, digital back and sleeves, dyed cambric trousers and embroidered chiffon dupatta.",
                "description": "A celebration of classic floral blooms. Includes 3.25m printed & embroidered lawn shirt fabric, 2.5m pure crinkle chiffon printed dupatta, 2.5m dyed cotton cambric trouser fabric, and embroidered organza neckline patch.",
                "fabric": "Premium Swiss Lawn & Crinkle Chiffon",
                "pieces": "3-Piece",
                "fit": "Customizable Unstitched",
                "care_instructions": "Soak fabrics in cold water before stitching. Dry in shade.",
                "stock_quantity": 80,
                "is_featured": True,
                "is_new_arrival": True,
                "is_best_seller": True,
                "is_sale": True,
                "rating_avg": 4.9,
                "reviews_count": 31,
                "images": [
                    "https://images.unsplash.com/photo-1617627143750-d86bc21e42bb?auto=format&fit=crop&w=800&q=80",
                    "https://images.unsplash.com/photo-1490481651871-ab68de25d43d?auto=format&fit=crop&w=800&q=80"
                ],
                "variants": [
                    {"size": "Unstitched", "color_name": "Ivory Floral", "color_hex": "#FFFDD0", "stock": 80}
                ]
            },
            {
                "title": "Unstitched 2-Piece Embroidered Chikankari - Cloud White",
                "slug": "unstitched-2pc-chikankari-cloud-white",
                "sku": "ZN-UST-102",
                "category_slug": "unstitched",
                "original_price": 3890.0,
                "discount_price": None,
                "short_description": "Bespoke all-over chikankari schiffli embroidery on lawn shirt paired with fine cambric dyed bottom.",
                "description": "Timeless Pakistani chikankari in pure pearl white. Detailed with all-over schiffli cutwork motifs across the entire shirt front. Comes with dyed premium lawn sleeves and solid lawn back with matching trousers.",
                "fabric": "Schiffli Embroidered Lawn",
                "pieces": "2-Piece",
                "fit": "Customizable Unstitched",
                "care_instructions": "Hand wash gently. Medium steam iron.",
                "stock_quantity": 40,
                "is_featured": False,
                "is_new_arrival": True,
                "is_best_seller": False,
                "is_sale": False,
                "rating_avg": 5.0,
                "reviews_count": 8,
                "images": [
                    "https://images.unsplash.com/photo-1609357605129-26f69add5d6e?auto=format&fit=crop&w=800&q=80",
                    "https://images.unsplash.com/photo-1583391733956-3750e0ff4e8b?auto=format&fit=crop&w=800&q=80"
                ],
                "variants": [
                    {"size": "Unstitched", "color_name": "Cloud White", "color_hex": "#F8F9FA", "stock": 40}
                ]
            },
            {
                "title": "Unstitched 3-Piece Jacquard Embroidered - Crimson Velvet Touch",
                "slug": "unstitched-3pc-jacquard-crimson",
                "sku": "ZN-UST-103",
                "category_slug": "unstitched",
                "original_price": 6490.0,
                "discount_price": 5190.0,
                "short_description": "Self-weave gold jacquard shirt with heavy tilla embroidered border and rich organza jacquard dupatta.",
                "description": "Intricately woven crimson jacquard featuring heritage tilla thread embroidery. Accompanied by a 2.5m matching jacquard dupatta with zari woven pallus and dyed cambric bottom fabric.",
                "fabric": "Gold Jacquard & Organza Zari",
                "pieces": "3-Piece",
                "fit": "Customizable Unstitched",
                "care_instructions": "Dry clean recommended.",
                "stock_quantity": 55,
                "is_featured": True,
                "is_new_arrival": False,
                "is_best_seller": True,
                "is_sale": True,
                "rating_avg": 4.9,
                "reviews_count": 14,
                "images": [
                    "https://images.unsplash.com/photo-1548036328-c9fa89d128fa?auto=format&fit=crop&w=800&q=80",
                    "https://images.unsplash.com/photo-1566174053879-31528523f8ae?auto=format&fit=crop&w=800&q=80"
                ],
                "variants": [
                    {"size": "Unstitched", "color_name": "Royal Crimson", "color_hex": "#990000", "stock": 55}
                ]
            },

            # Casual Wear
            {
                "title": "Solid Cotton A-Line Kurta - Terracotta Earth",
                "slug": "solid-cotton-a-line-kurta-terracotta",
                "sku": "ZN-CSL-201",
                "category_slug": "casual-wear",
                "original_price": 3290.0,
                "discount_price": 2790.0,
                "short_description": "Minimalist breathable cotton A-line kurta with pleated front yoke and tonal piping.",
                "description": "Essential everyday elegance. This lightweight Pakistani cotton kurta features a flattering flared cut, side slit pockets, and delicate pleating across the chest. Ideal for university, office, or casual weekend outings.",
                "fabric": "100% Breathable Cotton",
                "pieces": "1-Piece",
                "fit": "Flared A-Line",
                "care_instructions": "Machine wash cold with like colors. Line dry.",
                "stock_quantity": 65,
                "is_featured": False,
                "is_new_arrival": False,
                "is_best_seller": True,
                "is_sale": True,
                "rating_avg": 4.8,
                "reviews_count": 19,
                "images": [
                    "https://images.unsplash.com/photo-1509631179647-0177331693ae?auto=format&fit=crop&w=800&q=80",
                    "https://images.unsplash.com/photo-1515886657613-9f3515b0c78f?auto=format&fit=crop&w=800&q=80"
                ],
                "variants": [
                    {"size": "S", "color_name": "Terracotta", "color_hex": "#E2725B", "stock": 20},
                    {"size": "M", "color_name": "Terracotta", "color_hex": "#E2725B", "stock": 25},
                    {"size": "L", "color_name": "Terracotta", "color_hex": "#E2725B", "stock": 20}
                ]
            },
            {
                "title": "Printed Lawn Daily Kurti - Indigo Mosaic",
                "slug": "printed-lawn-daily-kurti-indigo-mosaic",
                "sku": "ZN-CSL-202",
                "category_slug": "casual-wear",
                "original_price": 2290.0,
                "discount_price": None,
                "short_description": "Everyday lawn shirt with geometric block-print inspired patterns and cuff detail.",
                "description": "Crisp lawn printed with indigo blue ethnic motifs. Features a notched round neckline with contrast binding and straight sleeves. Pairs effortlessly with white cigarette pants or denim.",
                "fabric": "Daily Combed Lawn",
                "pieces": "1-Piece",
                "fit": "Straight Everyday Fit",
                "care_instructions": "Machine wash warm.",
                "stock_quantity": 90,
                "is_featured": False,
                "is_new_arrival": True,
                "is_best_seller": False,
                "is_sale": False,
                "rating_avg": 4.6,
                "reviews_count": 7,
                "images": [
                    "https://images.unsplash.com/photo-1515886657613-9f3515b0c78f?auto=format&fit=crop&w=800&q=80",
                    "https://images.unsplash.com/photo-1572804013309-59a88b7e92f1?auto=format&fit=crop&w=800&q=80"
                ],
                "variants": [
                    {"size": "XS", "color_name": "Indigo Blue", "color_hex": "#1E3F66", "stock": 15},
                    {"size": "S", "color_name": "Indigo Blue", "color_hex": "#1E3F66", "stock": 30},
                    {"size": "M", "color_name": "Indigo Blue", "color_hex": "#1E3F66", "stock": 30},
                    {"size": "L", "color_name": "Indigo Blue", "color_hex": "#1E3F66", "stock": 15}
                ]
            },

            # Formal Wear
            {
                "title": "Hand-Embroidered Chiffon Formal Suit - Koh-i-Noor",
                "slug": "hand-embroidered-chiffon-formal-suit-kohinoor",
                "sku": "ZN-FRM-301",
                "category_slug": "formal-wear",
                "original_price": 16990.0,
                "discount_price": 13990.0,
                "short_description": "Opulent 3-piece pure chiffon gown with hand-encrusted zardozi, kora dabka and sequin embellishments.",
                "description": "An imperial heirloom masterpiece. Crafted on sheer midnight chiffon with handcrafted silver and champagne zardozi along the bodice, daman, and sleeves. Accompanied by silk lining, flared palazzo pants, and a scalloped 4-sided embroidered dupatta.",
                "fabric": "Pure Chiffon, Raw Silk & Organza",
                "pieces": "3-Piece",
                "fit": "Festive Kalidar Anarkali",
                "care_instructions": "Strictly dry clean only. Store in protective cotton bag.",
                "stock_quantity": 25,
                "is_featured": True,
                "is_new_arrival": True,
                "is_best_seller": True,
                "is_sale": True,
                "rating_avg": 5.0,
                "reviews_count": 27,
                "images": [
                    "https://images.unsplash.com/photo-1566174053879-31528523f8ae?auto=format&fit=crop&w=800&q=80",
                    "https://images.unsplash.com/photo-1490481651871-ab68de25d43d?auto=format&fit=crop&w=800&q=80",
                    "https://images.unsplash.com/photo-1583391733956-3750e0ff4e8b?auto=format&fit=crop&w=800&q=80"
                ],
                "variants": [
                    {"size": "S", "color_name": "Champagne Silver", "color_hex": "#D8D8D8", "stock": 8},
                    {"size": "M", "color_name": "Champagne Silver", "color_hex": "#D8D8D8", "stock": 10},
                    {"size": "L", "color_name": "Champagne Silver", "color_hex": "#D8D8D8", "stock": 7}
                ]
            },
            {
                "title": "Sequined Festive 3-Piece Gharara Suit - Ivory Pearl",
                "slug": "sequined-festive-3pc-gharara-ivory-pearl",
                "sku": "ZN-FRM-302",
                "category_slug": "formal-wear",
                "original_price": 18990.0,
                "discount_price": 15990.0,
                "short_description": "Exquisite short peplum kurti with heavy pearl embellishments and voluminous pleated festive gharara.",
                "description": "Bridal festive glam at its finest. The short flared kurti is fully laden with iridescent micro-sequins, pearls, and gota patti. The two-tier layered gharara cascades gracefully, topped with a heavy borders organza dupatta.",
                "fabric": "Organza, Tissue & Shimmer Silk",
                "pieces": "3-Piece",
                "fit": "Peplum Kurti with Flared Gharara",
                "care_instructions": "Specialist dry clean only.",
                "stock_quantity": 20,
                "is_featured": True,
                "is_new_arrival": False,
                "is_best_seller": True,
                "is_sale": True,
                "rating_avg": 5.0,
                "reviews_count": 16,
                "images": [
                    "https://images.unsplash.com/photo-1609357605129-26f69add5d6e?auto=format&fit=crop&w=800&q=80",
                    "https://images.unsplash.com/photo-1566174053879-31528523f8ae?auto=format&fit=crop&w=800&q=80"
                ],
                "variants": [
                    {"size": "S", "color_name": "Ivory Pearl", "color_hex": "#FFFFF0", "stock": 6},
                    {"size": "M", "color_name": "Ivory Pearl", "color_hex": "#FFFFF0", "stock": 8},
                    {"size": "L", "color_name": "Ivory Pearl", "color_hex": "#FFFFF0", "stock": 6}
                ]
            },

            # Accessories
            {
                "title": "Pure Pashmina Velvet Shawl - Kashmiri Tilla",
                "slug": "pure-velvet-shawl-kashmiri-tilla",
                "sku": "ZN-ACC-401",
                "category_slug": "accessories",
                "original_price": 9990.0,
                "discount_price": 8490.0,
                "short_description": "Micro-velvet black shawl with four-sided Kashmiri antique gold tilla thread border.",
                "description": "Wrap yourself in pure regal warmth. Made with 9000-grade micro velvet that drapes fluidly without heaviness. Embellished with 4-inch deep intricate Kashmiri tilla floral vines and corner medallions.",
                "fabric": "9000 Micro Velvet",
                "pieces": "1-Piece",
                "fit": "Standard 2.5m x 1m Shawl",
                "care_instructions": "Dry clean only.",
                "stock_quantity": 30,
                "is_featured": True,
                "is_new_arrival": False,
                "is_best_seller": True,
                "is_sale": True,
                "rating_avg": 5.0,
                "reviews_count": 35,
                "images": [
                    "https://images.unsplash.com/photo-1548036328-c9fa89d128fa?auto=format&fit=crop&w=800&q=80",
                    "https://images.unsplash.com/photo-1539109136881-3be0616acf4b?auto=format&fit=crop&w=800&q=80"
                ],
                "variants": [
                    {"size": "Standard", "color_name": "Jet Velvet Black", "color_hex": "#0D0D0D", "stock": 30}
                ]
            },
            {
                "title": "Handcrafted Embellished Traditional Khussa - Gota Gold",
                "slug": "traditional-khussa-gota-gold",
                "sku": "ZN-ACC-402",
                "category_slug": "accessories",
                "original_price": 3490.0,
                "discount_price": 2990.0,
                "short_description": "Genuine leather sole khussa with hand-stitched dabka, pearls, and gold gota artwork.",
                "description": "Traditional Punjabi artisanal leather footwear with padded insoles for all-day comfort. Features hand-worked gold metallic dabka and crystal stones that complement both casual and formal eastern attire.",
                "fabric": "Genuine Cow Leather & Velvet Upper",
                "pieces": "Footwear",
                "fit": "True to Pakistani Shoe Size",
                "care_instructions": "Wipe with dry clean cloth. Keep away from water.",
                "stock_quantity": 40,
                "is_featured": False,
                "is_new_arrival": True,
                "is_best_seller": False,
                "is_sale": True,
                "rating_avg": 4.8,
                "reviews_count": 11,
                "images": [
                    "https://images.unsplash.com/photo-1543163521-1bf539c55dd2?auto=format&fit=crop&w=800&q=80",
                    "https://images.unsplash.com/photo-1548036328-c9fa89d128fa?auto=format&fit=crop&w=800&q=80"
                ],
                "variants": [
                    {"size": "36 (6)", "color_name": "Antique Gold", "color_hex": "#CFB53B", "stock": 8},
                    {"size": "37 (7)", "color_name": "Antique Gold", "color_hex": "#CFB53B", "stock": 12},
                    {"size": "38 (8)", "color_name": "Antique Gold", "color_hex": "#CFB53B", "stock": 10},
                    {"size": "39 (9)", "color_name": "Antique Gold", "color_hex": "#CFB53B", "stock": 10}
                ]
            },
            {
                "title": "Embroidered Velvet Box Clutch - Midnight Emerald",
                "slug": "embroidered-velvet-box-clutch-emerald",
                "sku": "ZN-ACC-403",
                "category_slug": "accessories",
                "original_price": 2990.0,
                "discount_price": None,
                "short_description": "Structured evening hard-case clutch with floral tilla embroidery and detachable gold chain strap.",
                "description": "The ultimate party accessory. Velvet exterior lined with soft satin and finished with a crystal clasp lock. Roomy enough to hold phone, cards, and makeup essentials.",
                "fabric": "Plush Velvet & Metal Alloy",
                "pieces": "Clutch Bag",
                "fit": "Standard Minaudière",
                "care_instructions": "Store in dust bag.",
                "stock_quantity": 50,
                "is_featured": False,
                "is_new_arrival": True,
                "is_best_seller": False,
                "is_sale": False,
                "rating_avg": 4.9,
                "reviews_count": 6,
                "images": [
                    "https://images.unsplash.com/photo-1584917865442-de89df76afd3?auto=format&fit=crop&w=800&q=80",
                    "https://images.unsplash.com/photo-1548036328-c9fa89d128fa?auto=format&fit=crop&w=800&q=80"
                ],
                "variants": [
                    {"size": "One Size", "color_name": "Deep Emerald", "color_hex": "#094F29", "stock": 50}
                ]
            },
            {
                "title": "Printed Pure Silk Dupatta - Mughal Garden",
                "slug": "printed-pure-silk-dupatta-mughal-garden",
                "sku": "ZN-ACC-404",
                "category_slug": "accessories",
                "original_price": 2490.0,
                "discount_price": 1990.0,
                "short_description": "2.5m lustrous habotai silk dupatta with digital Mughal miniature floral prints.",
                "description": "Elevate plain kurtas with this vibrant digital printed silk dupatta. Silky, lightweight, and vibrant, finished with pico edging.",
                "fabric": "100% Habotai Silk",
                "pieces": "1-Piece Dupatta",
                "fit": "2.5 Meter Length",
                "care_instructions": "Hand wash cold. Low steam iron.",
                "stock_quantity": 60,
                "is_featured": False,
                "is_new_arrival": False,
                "is_best_seller": True,
                "is_sale": True,
                "rating_avg": 4.7,
                "reviews_count": 15,
                "images": [
                    "https://images.unsplash.com/photo-1617627143750-d86bc21e42bb?auto=format&fit=crop&w=800&q=80",
                    "https://images.unsplash.com/photo-1583391733956-3750e0ff4e8b?auto=format&fit=crop&w=800&q=80"
                ],
                "variants": [
                    {"size": "Standard", "color_name": "Multi Flora", "color_hex": "#D47A6A", "stock": 60}
                ]
            }
        ]

        # Insert products, images, and variants
        for pdata in products_data:
            cat = cat_objs.get(pdata["category_slug"])
            product = Product(
                title=pdata["title"],
                slug=pdata["slug"],
                sku=pdata["sku"],
                category_id=cat.id if cat else 1,
                original_price=pdata["original_price"],
                discount_price=pdata["discount_price"],
                short_description=pdata["short_description"],
                description=pdata["description"],
                fabric=pdata["fabric"],
                pieces=pdata["pieces"],
                fit=pdata["fit"],
                care_instructions=pdata["care_instructions"],
                stock_quantity=pdata["stock_quantity"],
                is_featured=pdata["is_featured"],
                is_new_arrival=pdata["is_new_arrival"],
                is_best_seller=pdata["is_best_seller"],
                is_sale=pdata["is_sale"],
                rating_avg=pdata["rating_avg"],
                reviews_count=pdata["reviews_count"]
            )
            db.session.add(product)
            db.session.flush() # obtain product.id

            # Add images
            for idx, img_url in enumerate(pdata["images"]):
                img = ProductImage(
                    product_id=product.id,
                    image_url=img_url,
                    alt_text=f"{product.title} - View {idx+1}",
                    display_order=idx,
                    is_primary=(idx == 0)
                )
                db.session.add(img)

            # Add variants
            for vdata in pdata["variants"]:
                variant = ProductVariant(
                    product_id=product.id,
                    size=vdata["size"],
                    color_name=vdata["color_name"],
                    color_hex=vdata["color_hex"],
                    stock_quantity=vdata["stock"]
                )
                db.session.add(variant)

            # Add verified customer reviews
            if pdata.get("reviews_count", 0) > 0:
                rev1 = Review(
                    product_id=product.id,
                    customer_name="Fatima Zahra",
                    customer_city="Lahore",
                    rating=5,
                    title="Exceeded my expectations!",
                    comment="The fabric quality and embroidery finishing is as pristine as portrayed in the photos. Very fast delivery to Lahore within 2 days. Zeenat is now my go-to pret brand!",
                    is_verified_buyer=True,
                    is_approved=True
                )
                rev2 = Review(
                    product_id=product.id,
                    customer_name="Maryam Tariq",
                    customer_city="Islamabad",
                    rating=5,
                    title="Stunning cut and stitching",
                    comment="The size medium fits like a dream! Super comfortable and got so many compliments at family dinner.",
                    is_verified_buyer=True,
                    is_approved=True
                )
                db.session.add_all([rev1, rev2])

        db.session.commit()

        # 5. Coupons
        coupons_data = [
            {
                "code": "WELCOME10",
                "description": "Flat 10% off for new shoppers on orders over Rs. 2,000",
                "discount_type": "percentage",
                "discount_value": 10.0,
                "min_order_value": 2000.0,
                "max_discount_amount": 1500.0,
                "is_active": True
            },
            {
                "code": "FESTIVE20",
                "description": "Save 20% on orders over Rs. 5,000",
                "discount_type": "percentage",
                "discount_value": 20.0,
                "min_order_value": 5000.0,
                "max_discount_amount": 3000.0,
                "is_active": True
            },
            {
                "code": "ZEENAT500",
                "description": "Flat Rs. 500 discount on orders above Rs. 3,500",
                "discount_type": "fixed",
                "discount_value": 500.0,
                "min_order_value": 3500.0,
                "is_active": True
            },
            {
                "code": "FREESHIP",
                "description": "Free nationwide shipping coupon",
                "discount_type": "fixed",
                "discount_value": 200.0,
                "min_order_value": 1000.0,
                "is_active": True
            }
        ]

        for cdata in coupons_data:
            c = Coupon(**cdata)
            db.session.add(c)

        db.session.commit()
        print("Zeenat Pakistan database seeded successfully with luxury catalog!")

if __name__ == '__main__':
    from app import create_app
    app = create_app()
    seed_database(app)
