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
    return render_template("index.html", _mtg_prices=data)

if __name__ == '__main__':
    app.run(debug=True)