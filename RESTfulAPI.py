from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///store.db'
db = SQLAlchemy(app)

# Модель для товара
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    description = db.Column(db.String(200))
    price = db.Column(db.Float)

    def __repr__(self):
        return f"Product {self.name}"

# Добавление нового товара
@app.route('/products', methods=['POST'])
def add_product():
    data = request.get_json()
    new_product = Product(name=data['name'], description=data['description'], price=data['price'])
    db.session.add(new_product)
    db.session.commit()
    return jsonify({'message': 'Product added successfully!'})

# Получение списка всех товаров
@app.route('/products', methods=['GET'])
def get_all_products():
    products = Product.query.all()
    output = []
    for product in products:
        product_data = {'id': product.id, 'name': product.name, 'description': product.description, 'price': product.price}
        output.append(product_data)
    return jsonify({'products': output})

# Получение информации о конкретном товаре
@app.route('/products/<product_id>', methods=['GET'])
def get_product(product_id):
    product = Product.query.get_or_404(product_id)
    product_data = {'id': product.id, 'name': product.name, 'description': product.description, 'price': product.price}
    return jsonify(product_data)

# Редактирование информации о товаре
@app.route('/products/<product_id>', methods=['PUT'])
def update_product(product_id):
    product = Product.query.get_or_404(product_id)
    data = request.get_json()
    product.name = data['name']
    product.description = data['description']
    product.price = data['price']
    db.session.commit()
    return jsonify({'message': 'Product updated successfully!'})

# Поиск товаров по запросу
@app.route('/products/search/<query>', methods=['GET'])
def search_products(query):
    products = Product.query.filter(Product.name.contains(query) | Product.description.contains(query)).all()
    if products:
        output = []
        for product in products:
            product_data = {'id': product.id, 'name': product.name, 'description': product.description, 'price': product.price}
            output.append(product_data)
        return jsonify({'products': output})
    else:
        return jsonify({'message': 'No products found for the query!'})

# Удаление товара
@app.route('/products/<product_id>', methods=['DELETE'])
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    return jsonify({'message': 'Product deleted successfully!'})

if __name__ == '__main__':
    app.run(debug=True)
