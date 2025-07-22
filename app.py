from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
from db_config import get_db_connection

app = Flask(__name__)
app.secret_key = 'shruti-secret'

@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    conn.close()
    return render_template('index.html', products=products)

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM products WHERE id = %s", (product_id,))
    product = cursor.fetchone()
    conn.close()
    return render_template('product_detail.html', product=product)

@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    if 'cart' not in session:
        session['cart'] = []
    if product_id not in session['cart']:
        session['cart'].append(product_id)
        session.modified = True
    return redirect(url_for('cart'))

@app.route('/remove_from_cart/<int:product_id>')
def remove_from_cart(product_id):
    if 'cart' in session and product_id in session['cart']:
        session['cart'].remove(product_id)
        session.modified = True
    return redirect(url_for('cart'))

@app.route('/cart')
def cart():
    if 'cart' not in session or not session['cart']:
        return render_template('cart.html', products=[], total=0)

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    placeholders = ','.join(['%s'] * len(session['cart']))
    cursor.execute(f"SELECT * FROM products WHERE id IN ({placeholders})", tuple(session['cart']))
    products = cursor.fetchall()
    conn.close()

    total = sum(product['price'] for product in products)
    return render_template('cart.html', products=products, total=total)

@app.route('/place_order', methods=['POST'])
def place_order():
    product_id = request.form['product_id']
    name = request.form['name']
    address = request.form['address']
    phone = request.form['phone']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO orders (product_id, customer_name, address, phone_number, status) VALUES (%s, %s, %s, %s, %s)",
        (product_id, name, address, phone, 'Pending')
    )
    conn.commit()
    conn.close()

    return render_template('order_success.html', name=name)

if __name__ == '__main__':
    app.run(debug=True)
