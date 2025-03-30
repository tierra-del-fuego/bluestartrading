from flask import Flask, render_template, request, redirect, url_for
import json
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
PRODUCTS_FILE = 'products.json'

# Ana admin formu
@app.route('/', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        title = request.form['title']
        price = request.form['price']
        link = request.form['link']

        images = []
        for i in range(1, 11):
            image_file = request.files.get(f'image{i}')
            if image_file and image_file.filename:
                filename = secure_filename(image_file.filename)
                save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                image_file.save(save_path)
                images.append(f'/{save_path}')

        new_product = {
            'title': title,
            'price': price,
            'link': link,
            'images': images
        }

        if os.path.exists(PRODUCTS_FILE):
            with open(PRODUCTS_FILE, 'r', encoding='utf-8') as f:
                try:
                    products = json.load(f)
                except json.JSONDecodeError:
                    products = []
        else:
            products = []

        products.append(new_product)
        with open(PRODUCTS_FILE, 'w', encoding='utf-8') as f:
            json.dump(products, f, ensure_ascii=False, indent=2)

        return redirect(url_for('admin'))

    return render_template('admin.html')

# Ürün listeleme sayfası
@app.route('/products')
def product_list():
    if os.path.exists(PRODUCTS_FILE):
        with open(PRODUCTS_FILE, 'r', encoding='utf-8') as f:
            try:
                products = json.load(f)
            except json.JSONDecodeError:
                products = []
    else:
        products = []

    return render_template('products.html', products=products)

# Ürün detay sayfası
@app.route('/product/<int:product_id>')
def product_detail(product_id):
    if os.path.exists(PRODUCTS_FILE):
        with open(PRODUCTS_FILE, 'r', encoding='utf-8') as f:
            try:
                products = json.load(f)
            except json.JSONDecodeError:
                products = []
    else:
        products = []

    if 0 <= product_id < len(products):
        return render_template('product_detail.html', product=products[product_id])
    else:
        return "Ürün bulunamadı", 404

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)
