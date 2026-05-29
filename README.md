# ╔══════════════════════════════════════════════════════════╗
# ║         PURE WEAVES - COMPLETE SETUP GUIDE               ║
# ║         For BCA Students - Step by Step                  ║
# ╚══════════════════════════════════════════════════════════╝

Shop Name  : Pure Weaves
Owner      : Latha & Gangadhar
Location   : Shivamogga, Karnataka
WhatsApp   : +91 8123 981877
Built By   : Claude AI + You!

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 📁 FILES IN THIS PROJECT

```
PureWeaves/
├── index.html          ← Main website (open this in browser!)
├── app.py              ← Python Flask backend
├── database.sql        ← MySQL database setup
├── requirements.txt    ← Python packages to install
└── README.md           ← This guide
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 🚀 STEP 1 — INSTALL VS CODE EXTENSIONS

Open VS Code → Extensions (Ctrl+Shift+X) → Search and install:

1. ✅ Python          (by Microsoft)
2. ✅ Pylance         (by Microsoft)
3. ✅ MySQL           (by cweijan)
4. ✅ GitLens         (for GitHub)
5. ✅ Prettier        (code formatter)
6. ✅ Live Server     (preview HTML instantly)
7. ✅ REST Client     (test your API)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 🐍 STEP 2 — INSTALL PYTHON & PACKAGES

1. Download Python from https://python.org (version 3.11+)
2. Open VS Code Terminal (Ctrl+`) and run:

   pip install -r requirements.txt

Packages installed:
- flask         → Web server framework
- flask-sqlalchemy → Connect Python to database
- flask-bcrypt  → Encrypt passwords securely
- flask-cors    → Allow website to talk to backend
- pymysql       → Connect to MySQL database
- pyjwt         → Create secure login tokens
- python-dotenv → Load secret keys safely

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 🗄️ STEP 3 — SETUP MYSQL DATABASE

Option A — MySQL Workbench (Recommended for beginners):
1. Download MySQL Community Server from mysql.com
2. Download MySQL Workbench
3. Open Workbench → Connect to localhost
4. Open database.sql file
5. Click Execute (lightning bolt icon)
6. Database "pureweaves_db" is created!

Option B — Command Line:
   mysql -u root -p < database.sql

Tables created:
- users       → Stores customer accounts
- otps        → Temporary login codes
- products    → All kuchu designs
- cart_items  → Shopping cart
- orders      → Customer orders
- order_items → Items in each order
- coupons     → Discount codes

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## ▶️ STEP 4 — RUN THE WEBSITE

### Option A — Just HTML (Quick Start, No Server Needed):
1. Open index.html in Chrome browser
2. Website is LIVE immediately!
3. All features work: login, catalog, cart, orders, admin

### Option B — With Python Backend (Full Features):
1. Open terminal in VS Code
2. Run: python app.py
3. Open browser: http://localhost:5000
4. Full backend with MySQL database running!

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 🔑 STEP 5 — HOW LOGIN WORKS

### Mobile OTP Login:
1. Customer enters 10-digit mobile number
2. Server generates random 6-digit OTP
3. OTP sent via SMS (use MSG91 or Twilio service)
4. Customer enters OTP → verified → logged in!
5. JWT token created → stored securely in browser
6. Token expires after 24 hours (auto logout)

### Google Login:
1. Customer clicks "Continue with Google"
2. Google OAuth popup opens
3. Customer selects their Gmail account
4. Google sends back: name, email, google_id
5. We store in database → JWT token created → logged in!

To enable real Google Login:
1. Go to console.cloud.google.com
2. Create project → Enable Google+ API
3. Create OAuth credentials → Copy Client ID
4. Add to your app.py configuration
5. It's completely FREE!

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 🛒 STEP 6 — HOW CART & ORDERS WORK

Cart Flow:
1. Customer browses catalog → clicks "Add to Cart"
2. Item stored in cart (localStorage for HTML version)
3. Customer goes to Cart page
4. Can change quantity, remove items
5. Enters coupon code (optional)
6. Clicks "Place Order via WhatsApp"
7. WhatsApp opens with pre-filled order message
8. Order sent directly to your number!

Coupon System:
- Admin creates coupon code in Admin Panel
- Customer enters code in cart
- System validates: valid? not expired? uses remaining?
- Discount applied automatically to total

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## ⚙️ STEP 7 — HOW ADMIN PANEL WORKS

Access: Press Ctrl+Shift+A on any page

Features:
1. Dashboard  → See total designs, orders, customers, coupons
2. Add Design → Upload photo + fill details → appears in catalog
3. Coupons    → Create discount codes with expiry dates
4. Orders     → View all customer orders

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 📤 STEP 8 — UPLOAD TO GITHUB

1. Install Git from git-scm.com
2. Open VS Code Terminal:

   git init
   git add .
   git commit -m "Pure Weaves website - first version"

3. Go to github.com → Create new repository "pure-weaves"
4. Copy the repository URL
5. Back in terminal:

   git remote add origin YOUR_GITHUB_URL
   git push -u origin main

6. Your code is now saved on GitHub!
7. Share the link with anyone!

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## ☁️ STEP 9 — HOST ON FREE CLOUD SERVER

Option A — Netlify (Best for HTML only, Free):
1. Go to netlify.com → Sign up free
2. Drag and drop your index.html file
3. Website is LIVE in 30 seconds!
4. You get a free URL like: pureweaves.netlify.app

Option B — Railway (For Python backend, Free):
1. Go to railway.app → Sign up free
2. Connect your GitHub repository
3. Add MySQL database
4. Set environment variables
5. Deploy → Live in minutes!

Option C — Render (Free with Python):
1. Go to render.com → Sign up free
2. Create new Web Service
3. Connect GitHub → Deploy
4. Free PostgreSQL database included

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 🧪 STEP 10 — SOFTWARE TESTING

### Unit Testing (Test each function separately):
   python -m pytest test_app.py -v

### Manual Testing Checklist:
□ Login with mobile OTP → works?
□ Login with Google → works?
□ Browse catalog → all 19 designs show?
□ Search designs → results filtered?
□ Add to cart → badge updates?
□ Apply coupon → discount applied?
□ Place order → WhatsApp opens?
□ Admin panel → can add design?
□ Admin coupons → can create coupon?
□ Logout → redirects to login?

### Performance Testing:
- Open Chrome → F12 → Network tab
- Reload page → check loading time
- Should load under 3 seconds

### Security Testing:
□ OTP expires after 5 minutes
□ JWT token expires after 24 hours
□ Wrong OTP rejected
□ Admin panel requires Ctrl+Shift+A

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 📚 HTML TAGS USED (For BCA Studies)

<!DOCTYPE html>  → Tells browser this is HTML5
<html>           → Root element
<head>           → Contains metadata, styles, title
<meta>           → Page information (charset, viewport)
<title>          → Browser tab title
<link>           → External CSS/fonts
<style>          → Internal CSS styles
<body>           → Visible page content
<nav>            → Navigation bar
<div>            → Container/section
<header>         → Page header section
<footer>         → Page footer section
<h1> to <h6>    → Headings (h1 = largest)
<p>              → Paragraph text
<span>           → Inline text container
<a>              → Link (href attribute)
<img>            → Image (src, alt attributes)
<button>         → Clickable button
<input>          → Text/number/file input
<select>         → Dropdown menu
<option>         → Items in dropdown
<textarea>       → Multi-line text input
<label>          → Label for input field
<script>         → JavaScript code

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 🎨 CSS PROPERTIES USED (For BCA Studies)

display          → flex, grid, block, none
flex             → flexbox layout
grid             → grid layout
position         → sticky, fixed, relative, absolute
background       → color, gradient, image
color            → text color
font-family      → font name
font-size        → text size (px, rem, clamp)
font-weight      → bold level (400=normal, 700=bold)
padding          → inner spacing
margin           → outer spacing
border           → border width, style, color
border-radius    → rounded corners
box-shadow       → shadow effect
transition       → animation on hover
transform        → move/scale/rotate element
overflow         → hidden, scroll, visible
z-index          → layer order
cursor           → pointer on hover
opacity          → transparency (0=hidden, 1=visible)
@media           → responsive design breakpoints
:root            → CSS variables
:hover           → mouse over effect
@keyframes       → animation definition

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 💻 JAVASCRIPT CONCEPTS USED (For BCA Studies)

Variables     : const, let
Functions     : function name() {}, arrow =>
Arrays        : [], .map(), .filter(), .find(), .push()
Objects       : {key: value}, APP.user.name
DOM           : document.getElementById(), .innerHTML
Events        : onclick, oninput, onchange
Conditions    : if/else, ternary ? :
Loops         : .forEach(), .map(), for loop
localStorage  : .setItem(), .getItem(), .removeItem()
JSON          : JSON.parse(), JSON.stringify()
Fetch API     : fetch(url).then().catch()
Template str  : `Hello ${name}`
Spread        : [...array]
Async/Await   : async function, await fetch()
RegEx         : /^\d{10}$/.test(mobile)
setTimeout    : delay code execution
encodeURI     : encode WhatsApp message text
Math.random   : generate random OTP number

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 🐍 PYTHON CONCEPTS USED (For BCA Studies)

Functions     : def function_name():
Decorators    : @app.route(), @wraps
Classes       : class User(db.Model):
Imports       : from flask import Flask
Variables     : app = Flask(__name__)
Conditionals  : if/elif/else
Loops         : for item in list:
Lists         : [], list.append()
Dictionaries  : {key: value}
String format : f"Hello {name}"
Exception     : try/except
Return        : return jsonify({})
ORM queries   : User.query.filter_by().first()
Environment   : os.environ.get()
DateTime      : datetime.datetime.utcnow()
Random        : random.choices(string.digits, k=6)
JWT           : jwt.encode(), jwt.decode()
Hashing       : bcrypt.generate_password_hash()

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 🗄️ SQL QUERIES USED (For BCA Studies)

CREATE DATABASE  → Create new database
USE              → Select database to use
CREATE TABLE     → Create new table
PRIMARY KEY      → Unique identifier for each row
AUTO_INCREMENT   → Automatically increase ID number
NOT NULL         → Field cannot be empty
UNIQUE           → No duplicate values allowed
DEFAULT          → Value if nothing is provided
FOREIGN KEY      → Link one table to another
INSERT INTO      → Add new data
SELECT           → Read/get data
WHERE            → Filter condition
UPDATE           → Change existing data
DELETE           → Remove data
JOIN             → Combine data from two tables
INDEX            → Speed up searching

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 🔒 SECURITY FEATURES EXPLAINED

1. JWT Tokens      → Like a secure ID card, expires in 24 hours
2. OTP Login       → One-time password, valid only 5 minutes
3. Bcrypt Hashing  → Passwords stored encrypted, never plain text
4. CORS Policy     → Only allowed websites can access backend
5. Input Validation → Check mobile is 10 digits before processing
6. SQL Injection    → SQLAlchemy ORM prevents SQL injection attacks
7. Rate Limiting    → Max 5 login attempts, then blocked
8. HTTPS           → Encrypt all data between browser and server
9. Env Variables   → Secret keys not stored in code
10. Token Auth     → Every API call requires valid token

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 📱 TECHNOLOGIES SUMMARY

Frontend  : HTML5 + CSS3 + JavaScript (ES6+)
Backend   : Python 3.11 + Flask Framework
Database  : MySQL 8.0
Auth      : JWT + OTP + Google OAuth 2.0
Hosting   : Netlify (free) / Railway (free)
Version   : Git + GitHub
IDE       : VS Code

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Good luck, Sanju! 🎓
This project is perfect for your BCA portfolio.
Built with ❤️ for Pure Weaves, Shivamogga.

