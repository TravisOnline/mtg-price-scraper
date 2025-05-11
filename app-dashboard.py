from collections import defaultdict

from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

@app.route('/')
def _mtg_prices():
    connect = sqlite3.connect('mtg-database.db')
    connect.row_factory = sqlite3.Row  # Enables access by column name
    cursor = connect.cursor()
    cursor.execute('SELECT * FROM CARDPRICES')
    data = cursor.fetchall()

    # Sort products by type
    grouped = defaultdict(list)
    for row in data:
        grouped[row['product_type']].append(row)

    # Build a product list with image and prices
    products = []
    for product_type, rows in grouped.items():
        # Convert string prices to floats for sorting and handle "NONE"
        def sort_key(row):
            price = row["price"]
            return float(price) if price != "Non" and price != "None" else float('inf')
        sorted_rows = sorted(rows, key=sort_key, reverse=False)
        products.append({
            "product_type": product_type,
            "image_path": f"images/{product_type}.jpg",
            "prices": sorted_rows
        })

    return render_template("index.html", products=products)

if __name__ == '__main__':
    app.run(debug=True)