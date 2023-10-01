# E-Commerce Website

This is a simple e-commerce website built using Django, a powerful Python web framework. The project allows you to create an online store where users can browse products, add them to their cart, and make purchases.

## Features

- **Product Catalog:** Display a list of products with details.
- **Product Categories:** Organize products into different categories.
- **User Authentication:** Allow users to register, log in, and manage their accounts.
- **Shopping Cart:** Enable users to add products to their cart.
- **Checkout:** Process orders and payments.
- **Admin Dashboard:** Manage products, orders, and user accounts.
- **Search Functionality:** Implement product search functionality.
- **Product Reviews:** Allow users to leave reviews and ratings for products.

## Technologies Used

- **Django:** A high-level Python web framework for building robust web applications.
- **Django REST Framework:** Used for building APIs and managing product data.
- **SQLite:** A lightweight database for storing product information.
- **HTML/CSS:** Used for front-end design and layout.
- **JavaScript:** Used for interactive features.
- **Bootstrap:** A front-end framework for responsive design.
- **Stripe:** A payment processing platform for handling payments.

## Installation

1. Clone the repository:

   ```bash
   git clone <url>
   ```

2. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:

   - On Windows:

     ```bash
     venv\Scripts\activate
     ```

   - On macOS and Linux:

     ```bash
     source venv/bin/activate
     ```

4. Install Python dependencies:

   ```bash
   pip install -r requirements.txt
   ```

5. Migrate the database:

   ```bash
   python manage.py migrate
   ```

6. Create a superuser (admin) account:

   ```bash
   python manage.py createsuperuser
   ```

7. Start the development server:

   ```bash
   python manage.py runserver
   ```

8. Access the website at `http://localhost:8000` in your web browser.

## Usage

- Browse and search for products.
- Add products to your shopping cart.
- Register or log in to your user account.
- Complete the checkout process to place an order.
- Admins can access the admin dashboard at `http://localhost:8000/admin` to manage products, orders, and users.
