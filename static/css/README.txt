# Meesha Clothing - Mini Meesho-like Website

This is a simple clothing e-commerce website built using Flask and MySQL. Users can view and purchase clothes (Cash on Delivery only). Admin can upload product details via the admin panel.

## Features

- Admin (Shruti Tyagi) can upload product photos and details
- Customers can view all clothes
- Customers can buy clothes with Cash on Delivery (COD)
- Image upload supported
- All products shown on homepage
- Clean UI using basic HTML + CSS

## Folder Structure

meesha/
│
├── app.py                    # Main Flask app
├── db_config.py              # MySQL connection settings
├── requirements.txt          # Required Python libraries
├── README.txt                # This file

├── static/
│   ├── uploads/              # Uploaded product images
│   └── css/
│       └── style.css         # Custom CSS styles

├── templates/
│   ├── index.html            # Homepage with all products
│   ├── admin_panel.html      # Admin product upload page
│   ├── buy.html              # Buy form for COD
│   └── success.html          # Success message after purchase

## Database Setup (MySQL)

Run the following queries in your MySQL:

```sql
CREATE DATABASE meesha;
USE meesha;

CREATE TABLE products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(100),
    description TEXT,
    price DECIMAL(10,2),
    category VARCHAR(50),
    image_path VARCHAR(255)
);

CREATE TABLE orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT,
    customer_name VARCHAR(100),
    address TEXT,
    phone VARCHAR(20),
    payment_mode VARCHAR(20) DEFAULT 'COD',
    order_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES products(id)
);
