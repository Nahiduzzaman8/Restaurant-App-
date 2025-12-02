# Restaurant Web Application

A fully functional restaurant web application built with Django. The system includes JWT-based authentication stored in cookies, a dynamic cart system, item management, home-page content sections, and modal-based cart display features.

This project is designed for production-ready backend practices and clean UI/UX integration.

---

## Features

### **Authentication (JWT Cookie Based)**
- Login and signup system using Django.
- JWT issued on login and stored securely inside HTTP cookies.
- Token verification before accessing protected views.
- Auto-redirect to home page after successful login.

### **Menu & Item Management**
- Displays categories, items, offers, and sliders dynamically.
- Items shown with images, descriptions, and add-to-cart functionality.

### **Shopping Cart System**
- Add items to cart using AJAX.
- Fetch cart items with JWT-cookie verification.
- Cart stored in database (per-user).
- Modal display with item image, price, quantity, and total.

### **User Interface Components**
- Dynamic modal for cart.
- Fully responsive HTML/CSS templates.
- Bootstrap 4 and FontAwesome integration.

### **General Features**
- About page and contact information.
- Feedback section in the homepage.
- Category-based filtering.

### **Admin Panel**

This project extensively uses Django’s built-in Admin Panel for backend management.
Through the admin interface, you can easily manage:

Categories

Items (with images)

Offers and discounts

Slider images

Feedback entries

Table bookings

Contact information

About section content

Admin panel provides full CRUD operations and media file handling.

---

## Technology Stack

### Backend
- Python 3
- Django
- SQLite / PostgreSQL

### Frontend
- HTML5, CSS3
- Bootstrap 4
- JavaScript (Fetch API)

### Others
- JWT Authentication
- Pillow for image handling

---

## Installation and Setup

### **1. Clone the repository**
```
git clone <repo-url>
cd restaurent
```

### **2. Create and activate virtual environment**
```
python3 -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
```

### **3. Install dependencies**
```
pip install -r requirements.txt
```

### **4. Apply migrations**
```
python manage.py migrate
```

### **5. Start server**
```
python manage.py runserver
```

Your application will run at:
```
http://127.0.0.1:8000/
```

---

## Project Structure
```
project/
│
├── restaurent/
│   ├── settings.py
│   ├── urls.py
│   └── ...
│
├── baseapp/
│   ├── views.py
│   ├── models.py
│   ├── templates/
│   │   ├── home.html
│   │   ├── about.html
│   │   └── base.html
│   └── static/
│
└── media/
```

---

## API Endpoints

### **Add to Cart**
```
POST /add_to_cart/
```
Body:
```
{
  "item_id": <id>
}
```

### **Get Cart Items**
```
GET /get_cart_items/
```
Response:
```
{
  "items": [
    {
      "name": "Pizza",
      "price": 400,
      "quantity": 2,
      "total": 800,
      "image": "/media/..."
    }
  ]
}
```

---

## Authentication Flow
1. User logs in.
2. Server returns a JWT and stores it inside a cookie.
3. For every protected route, JWT is extracted and validated.
4. If token is invalid or missing, return 401.

---

## Screenshots
Add your UI screenshots here.

---

## Future Improvements
- Order checkout system
- Payment gateway integration
- Admin dashboard for managing items
- Real-time order updates

---

## License
This project is for learning purposes and can be freely modified.

---

## Author
Developed by Nahid.

