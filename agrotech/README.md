# AgroTech – Farmer Buyer Marketplace

A full-stack Django web application that connects farmers and buyers directly.

---

## Project Structure

```
agrotech/
├── manage.py
├── requirements.txt
├── db.sqlite3              (created on first run)
├── agrotech_project/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── accounts/               (user auth, profile, KYC)
├── farmers/                (crops, orders, earnings, reviews)
├── buyers/                 (browse, cart, orders, wishlist)
├── admin_panel/            (KYC review, user manage, disputes)
├── templates/              (base.html)
├── static/
│   ├── css/main.css
│   └── js/main.js
└── media/                  (uploaded images)
```

---

## Setup Instructions

### 1. Install dependencies

```bash
pip install django pillow
```

### 2. Run migrations

```bash
python manage.py makemigrations accounts
python manage.py makemigrations farmers
python manage.py makemigrations buyers
python manage.py makemigrations
python manage.py migrate
```

### 3. Create admin superuser

```bash
python manage.py createsuperuser
```
Use an email address as your username (e.g. admin@agrotech.in).

### 4. Run the server

```bash
python manage.py runserver
```

Open http://127.0.0.1:8000 in your browser.

---

## User Roles

| Role    | What they can do |
|---------|-----------------|
| Farmer  | List crops, manage orders, view earnings, see reviews |
| Buyer   | Browse & search crops, cart, place orders, track, review |
| Admin   | Approve KYC, block users, manage reviews, view disputes |

---

## Key Pages

### Public
- `/buyers/` — Browse all crops (search + filter)
- `/buyers/crop/<id>/` — Crop detail

### Farmers
- `/farmers/dashboard/` — Stats overview
- `/farmers/my-crops/` — List, add, edit, delete crops
- `/farmers/orders/` — Incoming orders + status update
- `/farmers/earnings/` — Earnings table
- `/farmers/reviews/` — Buyer reviews

### Buyers
- `/buyers/cart/` — Cart
- `/buyers/order/place/<id>/` — Place order (live total calculator)
- `/buyers/orders/` — My orders
- `/buyers/orders/track/<id>/` — Order timeline
- `/buyers/wishlist/` — Saved crops

### Admin
- `/admin-panel/dashboard/` — Platform overview
- `/admin-panel/kyc/` — KYC approval queue
- `/admin-panel/users/` — Block/Activate users
- `/admin-panel/reviews/` — Remove flagged reviews
- `/admin-panel/orders/` — All orders
- `/admin-panel/disputes/` — Cancelled order disputes

### Accounts
- `/accounts/register/` — Register as Farmer or Buyer
- `/accounts/login/` — Login
- `/accounts/profile/` — View & edit profile
- `/accounts/kyc/` — Submit KYC documents
- `/accounts/forgot-password/` — Reset password

---

## Design Decisions

- **Simple class names** — `.crop-card`, `.stat-box`, `.form-group` — no BEM complexity
- **Human-readable code** — comments explain each section clearly
- **Medium JS** — only what's needed: mobile menu, flash auto-dismiss, image preview, role picker highlight, live order total
- **No chart libraries** — all stats shown as text boxes and tables
- **Role-based routing** — login redirects to farmer dashboard or buyer home automatically
- **KYC flow** — submit → admin reviews → approve/reject → verified badge appears
