# ============================================================
#  Pure Weaves - Backend (Python Flask)
#  File: app.py
#  Description: Complete e-commerce backend with:
#    - User Authentication (OTP + Google)
#    - Product Management
#    - Cart & Orders
#    - Admin Panel
#    - Coupon System
#    - Security Features
# ============================================================

from flask import Flask, request, jsonify, session, render_template_string
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from functools import wraps
import random, string, datetime, os, jwt

app = Flask(__name__)

# ─── SECURITY CONFIG ─────────────────────────────────────────
app.config['SECRET_KEY']           = os.environ.get('SECRET_KEY', 'PureWeaves@Shivamogga#2024!SecureKey')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'mysql+pymysql://root:password@localhost/pureweaves_db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_EXPIRY_HOURS']     = 24
app.config['OTP_EXPIRY_MINUTES']   = 5
app.config['MAX_LOGIN_ATTEMPTS']   = 5

db    = SQLAlchemy(app)
bcrypt = Bcrypt(app)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# ─── DATABASE MODELS ──────────────────────────────────────────

class User(db.Model):
    """User table - stores all customer information"""
    __tablename__ = 'users'
    id            = db.Column(db.Integer, primary_key=True)
    name          = db.Column(db.String(100), nullable=False)
    mobile        = db.Column(db.String(15), unique=True, nullable=True)
    email         = db.Column(db.String(120), unique=True, nullable=True)
    google_id     = db.Column(db.String(200), unique=True, nullable=True)
    is_admin      = db.Column(db.Boolean, default=False)
    is_active     = db.Column(db.Boolean, default=True)
    login_attempts = db.Column(db.Integer, default=0)
    created_at    = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    orders        = db.relationship('Order', backref='user', lazy=True)
    cart_items    = db.relationship('CartItem', backref='user', lazy=True)

class OTP(db.Model):
    """OTP table - stores temporary login codes"""
    __tablename__ = 'otps'
    id         = db.Column(db.Integer, primary_key=True)
    mobile     = db.Column(db.String(15), nullable=False)
    otp_code   = db.Column(db.String(6), nullable=False)
    is_used    = db.Column(db.Boolean, default=False)
    expires_at = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

class Product(db.Model):
    """Product table - stores all kuchu/bunch designs"""
    __tablename__ = 'products'
    id          = db.Column(db.Integer, primary_key=True)
    name        = db.Column(db.String(200), nullable=False)
    category    = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price_min   = db.Column(db.Float, nullable=False)
    price_max   = db.Column(db.Float, nullable=False)
    image_path  = db.Column(db.String(500), nullable=True)
    is_active   = db.Column(db.Boolean, default=True)
    stock       = db.Column(db.Integer, default=100)
    created_at  = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    cart_items  = db.relationship('CartItem', backref='product', lazy=True)
    order_items = db.relationship('OrderItem', backref='product', lazy=True)

class CartItem(db.Model):
    """Cart table - stores items in customer cart"""
    __tablename__ = 'cart_items'
    id         = db.Column(db.Integer, primary_key=True)
    user_id    = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity   = db.Column(db.Integer, default=1)
    added_at   = db.Column(db.DateTime, default=datetime.datetime.utcnow)

class Order(db.Model):
    """Order table - stores all customer orders"""
    __tablename__ = 'orders'
    id           = db.Column(db.Integer, primary_key=True)
    user_id      = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    coupon_code  = db.Column(db.String(50), nullable=True)
    discount     = db.Column(db.Float, default=0)
    status       = db.Column(db.String(50), default='pending')
    whatsapp_sent = db.Column(db.Boolean, default=False)
    created_at   = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    items        = db.relationship('OrderItem', backref='order', lazy=True)

class OrderItem(db.Model):
    """Order items - each product in an order"""
    __tablename__ = 'order_items'
    id         = db.Column(db.Integer, primary_key=True)
    order_id   = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity   = db.Column(db.Integer, nullable=False)
    price      = db.Column(db.Float, nullable=False)

class Coupon(db.Model):
    """Coupon table - discount codes created by admin"""
    __tablename__ = 'coupons'
    id              = db.Column(db.Integer, primary_key=True)
    code            = db.Column(db.String(50), unique=True, nullable=False)
    discount_percent = db.Column(db.Float, nullable=False)
    max_uses        = db.Column(db.Integer, default=100)
    used_count      = db.Column(db.Integer, default=0)
    expires_at      = db.Column(db.DateTime, nullable=False)
    is_active       = db.Column(db.Boolean, default=True)
    created_at      = db.Column(db.DateTime, default=datetime.datetime.utcnow)

# ─── HELPER FUNCTIONS ─────────────────────────────────────────

def generate_otp():
    """Generate a secure 6-digit OTP"""
    return ''.join(random.choices(string.digits, k=6))

def generate_token(user_id):
    """Generate JWT token for authenticated user"""
    payload = {
        'user_id': user_id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=app.config['JWT_EXPIRY_HOURS'])
    }
    return jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')

def token_required(f):
    """Decorator to protect routes that need login"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        if not token:
            return jsonify({'error': 'Login required'}), 401
        try:
            data    = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = User.query.get(data['user_id'])
            if not current_user or not current_user.is_active:
                return jsonify({'error': 'Invalid user'}), 401
        except:
            return jsonify({'error': 'Invalid or expired token'}), 401
        return f(current_user, *args, **kwargs)
    return decorated

def admin_required(f):
    """Decorator to protect admin-only routes"""
    @wraps(f)
    @token_required
    def decorated(current_user, *args, **kwargs):
        if not current_user.is_admin:
            return jsonify({'error': 'Admin access required'}), 403
        return f(current_user, *args, **kwargs)
    return decorated

# ─── AUTH ROUTES ─────────────────────────────────────────────

@app.route('/api/auth/send-otp', methods=['POST'])
def send_otp():
    """
    Send OTP to mobile number
    POST /api/auth/send-otp
    Body: { "mobile": "9812398177" }
    """
    mobile = request.json.get('mobile', '').strip()
    if not mobile or len(mobile) != 10:
        return jsonify({'error': 'Enter valid 10-digit mobile number'}), 400
    otp_code   = generate_otp()
    expires_at = datetime.datetime.utcnow() + datetime.timedelta(minutes=app.config['OTP_EXPIRY_MINUTES'])
    # Delete old OTPs for this number
    OTP.query.filter_by(mobile=mobile).delete()
    new_otp = OTP(mobile=mobile, otp_code=otp_code, expires_at=expires_at)
    db.session.add(new_otp)
    db.session.commit()
    # TODO: Connect SMS service (e.g. Twilio, MSG91) to actually send OTP
    # For now, print to console for testing:
    print(f"OTP for {mobile}: {otp_code}")
    return jsonify({'message': f'OTP sent to {mobile}', 'dev_otp': otp_code}), 200

@app.route('/api/auth/verify-otp', methods=['POST'])
def verify_otp():
    """
    Verify OTP and login user
    POST /api/auth/verify-otp
    Body: { "mobile": "9812398177", "otp": "123456" }
    """
    mobile   = request.json.get('mobile', '').strip()
    otp_code = request.json.get('otp', '').strip()
    record   = OTP.query.filter_by(mobile=mobile, otp_code=otp_code, is_used=False).first()
    if not record:
        return jsonify({'error': 'Invalid OTP'}), 400
    if datetime.datetime.utcnow() > record.expires_at:
        return jsonify({'error': 'OTP expired. Please request a new one'}), 400
    record.is_used = True
    user = User.query.filter_by(mobile=mobile).first()
    if not user:
        user = User(name=f'Customer_{mobile[-4:]}', mobile=mobile)
        db.session.add(user)
    db.session.commit()
    token = generate_token(user.id)
    return jsonify({'token': token, 'user': {'id': user.id, 'name': user.name, 'mobile': user.mobile}}), 200

@app.route('/api/auth/google', methods=['POST'])
def google_login():
    """
    Google OAuth login
    POST /api/auth/google
    Body: { "google_id": "...", "email": "...", "name": "..." }
    """
    google_id = request.json.get('google_id')
    email     = request.json.get('email')
    name      = request.json.get('name')
    if not google_id or not email:
        return jsonify({'error': 'Invalid Google account data'}), 400
    user = User.query.filter_by(google_id=google_id).first()
    if not user:
        user = User(name=name, email=email, google_id=google_id)
        db.session.add(user)
        db.session.commit()
    token = generate_token(user.id)
    return jsonify({'token': token, 'user': {'id': user.id, 'name': user.name, 'email': user.email}}), 200

# ─── PRODUCT ROUTES ──────────────────────────────────────────

@app.route('/api/products', methods=['GET'])
def get_products():
    """Get all active products, optionally filter by category"""
    category = request.args.get('category')
    query    = Product.query.filter_by(is_active=True)
    if category and category != 'All':
        query = query.filter_by(category=category)
    products = query.all()
    return jsonify([{
        'id': p.id, 'name': p.name, 'category': p.category,
        'description': p.description, 'price_min': p.price_min,
        'price_max': p.price_max, 'image_path': p.image_path, 'stock': p.stock
    } for p in products]), 200

# ─── CART ROUTES ─────────────────────────────────────────────

@app.route('/api/cart', methods=['GET'])
@token_required
def get_cart(current_user):
    """Get current user's cart items"""
    items = CartItem.query.filter_by(user_id=current_user.id).all()
    return jsonify([{
        'id': i.id, 'product_id': i.product_id,
        'name': i.product.name, 'price_min': i.product.price_min,
        'quantity': i.quantity, 'image_path': i.product.image_path
    } for i in items]), 200

@app.route('/api/cart/add', methods=['POST'])
@token_required
def add_to_cart(current_user):
    """Add item to cart"""
    product_id = request.json.get('product_id')
    quantity   = request.json.get('quantity', 1)
    product    = Product.query.get(product_id)
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    existing = CartItem.query.filter_by(user_id=current_user.id, product_id=product_id).first()
    if existing:
        existing.quantity += quantity
    else:
        item = CartItem(user_id=current_user.id, product_id=product_id, quantity=quantity)
        db.session.add(item)
    db.session.commit()
    return jsonify({'message': 'Added to cart'}), 200

@app.route('/api/cart/remove/<int:item_id>', methods=['DELETE'])
@token_required
def remove_from_cart(current_user, item_id):
    """Remove item from cart"""
    item = CartItem.query.filter_by(id=item_id, user_id=current_user.id).first()
    if not item:
        return jsonify({'error': 'Item not found'}), 404
    db.session.delete(item)
    db.session.commit()
    return jsonify({'message': 'Removed from cart'}), 200

# ─── COUPON ROUTES ───────────────────────────────────────────

@app.route('/api/coupon/validate', methods=['POST'])
@token_required
def validate_coupon(current_user):
    """Validate a coupon code"""
    code   = request.json.get('code', '').upper().strip()
    coupon = Coupon.query.filter_by(code=code, is_active=True).first()
    if not coupon:
        return jsonify({'error': 'Invalid coupon code'}), 400
    if datetime.datetime.utcnow() > coupon.expires_at:
        return jsonify({'error': 'Coupon has expired'}), 400
    if coupon.used_count >= coupon.max_uses:
        return jsonify({'error': 'Coupon usage limit reached'}), 400
    return jsonify({'discount_percent': coupon.discount_percent, 'code': coupon.code}), 200

# ─── ORDER ROUTES ────────────────────────────────────────────

@app.route('/api/order/place', methods=['POST'])
@token_required
def place_order(current_user):
    """Place an order"""
    coupon_code = request.json.get('coupon_code', '')
    cart_items  = CartItem.query.filter_by(user_id=current_user.id).all()
    if not cart_items:
        return jsonify({'error': 'Cart is empty'}), 400
    total    = sum(i.product.price_min * i.quantity for i in cart_items)
    discount = 0
    if coupon_code:
        coupon = Coupon.query.filter_by(code=coupon_code.upper(), is_active=True).first()
        if coupon:
            discount = total * (coupon.discount_percent / 100)
            coupon.used_count += 1
    order = Order(user_id=current_user.id, total_amount=total - discount,
                  coupon_code=coupon_code, discount=discount)
    db.session.add(order)
    db.session.flush()
    for item in cart_items:
        order_item = OrderItem(order_id=order.id, product_id=item.product_id,
                               quantity=item.quantity, price=item.product.price_min)
        db.session.add(order_item)
    CartItem.query.filter_by(user_id=current_user.id).delete()
    db.session.commit()
    return jsonify({'message': 'Order placed!', 'order_id': order.id, 'total': total - discount}), 200

# ─── ADMIN ROUTES ────────────────────────────────────────────

@app.route('/api/admin/product/add', methods=['POST'])
@admin_required
def add_product(current_user):
    """Admin: Add new design/product"""
    data    = request.json
    product = Product(
        name=data['name'], category=data['category'],
        description=data['description'], price_min=data['price_min'],
        price_max=data['price_max'], image_path=data.get('image_path', ''),
        stock=data.get('stock', 100)
    )
    db.session.add(product)
    db.session.commit()
    return jsonify({'message': 'Design added!', 'id': product.id}), 201

@app.route('/api/admin/coupon/create', methods=['POST'])
@admin_required
def create_coupon(current_user):
    """Admin: Create new coupon code"""
    data   = request.json
    coupon = Coupon(
        code=data['code'].upper(), discount_percent=data['discount_percent'],
        max_uses=data.get('max_uses', 100),
        expires_at=datetime.datetime.strptime(data['expires_at'], '%Y-%m-%d')
    )
    db.session.add(coupon)
    db.session.commit()
    return jsonify({'message': f'Coupon {coupon.code} created!'}), 201

@app.route('/api/admin/orders', methods=['GET'])
@admin_required
def get_all_orders(current_user):
    """Admin: View all orders"""
    orders = Order.query.order_by(Order.created_at.desc()).all()
    return jsonify([{
        'id': o.id, 'user': o.user.name, 'mobile': o.user.mobile,
        'total': o.total_amount, 'status': o.status,
        'coupon': o.coupon_code, 'discount': o.discount,
        'created_at': o.created_at.strftime('%d-%m-%Y %H:%M')
    } for o in orders]), 200

@app.route('/api/admin/stats', methods=['GET'])
@admin_required
def get_stats(current_user):
    """Admin: Dashboard statistics"""
    return jsonify({
        'total_users':    User.query.count(),
        'total_orders':   Order.query.count(),
        'total_products': Product.query.filter_by(is_active=True).count(),
        'total_revenue':  db.session.query(db.func.sum(Order.total_amount)).scalar() or 0,
        'active_coupons': Coupon.query.filter_by(is_active=True).count()
    }), 200

# ─── RUN ─────────────────────────────────────────────────────

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("✅ Database tables created successfully!")
        print("✅ Pure Weaves backend running at http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
