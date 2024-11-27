from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from password import my_password
from flask_marshmallow import Marshmallow
from marshmallow import ValidationError, fields
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+mysqlconnector://root:{my_password}@localhost/e_commerce_db'
db = SQLAlchemy(app)
ma = Marshmallow(app)

class Customers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    phone = db.Column(db.String(255))
    email = db.Column(db.String(255))

class Customer_Accounts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    email = db.Column(db.String(255))

class Products(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    price = db.Column(db.Float)

class Orders(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))

class Order_Products(db.Model):
    order_id = db.Column(db.Integer,db.ForeignKey('orders.id'), nullable=False, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    
class Stock(db.Model):
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), primary_key=True)
    quantity = db.Column(db.Integer)
    
#Marshmallow Schemas
class CustomerSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True)
    phone = fields.String(required=True)
    email = fields.String(required=True)

class CustomerAccountSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    username = fields.String(required=True)
    password = fields.String(required=True)
    email = fields.String(required=True)

class ProductSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True)
    price = fields.Float(required=True)

class OrderSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    date = fields.Date()
    customer_id = fields.Integer(required=True)

class OrderProductSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    product_id = fields.Integer(required=True)
    quantity = fields.Integer(required=True)

class StockSchema(ma.Schema):
    product_id = fields.Integer(required=True)
    quantity = fields.Integer(required=True)

customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True)
customer_account_schema = CustomerAccountSchema()
customer_accounts_schema = CustomerAccountSchema(many=True)
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)
order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)
order_product_schema = OrderProductSchema()
order_products_schema = OrderProductSchema(many=True)
stock_schema = StockSchema()
stocks_schema = StockSchema(many=True)

#CRUD Endpoints for Customers
@app.route('/customers', methods=['GET'])
def list_customers():
    customers = Customers.query.all()
    return customers_schema.jsonify(customers)

@app.route('/customers', methods=['POST'])
def create_customer():
    try:
        customer_data = customer_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400
    new_customer = Customers(name=customer_data['name'], phone=customer_data['phone'], email=customer_data['email'])
    db.session.add(new_customer)
    db.session.commit()
    return jsonify({'message': 'Customer added successfully.'}), 201

@app.route('/customers/<int:id>', methods=['GET'])
def read_customer(id):
        customer = Customers.query.get_or_404(id)
        return customer_schema.jsonify(customer)

@app.route('/customers/<int:id>', methods=['PUT'])
def update_customer(id):
    customer = Customers.query.get_or_404(id)
    try:
        customer_data = customer_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400
    customer.name = customer_data['name']
    customer.phone = customer_data['phone']
    customer.email = customer_data['email']
    db.session.commit()
    return jsonify({'message': 'Customer updated successfully.'})
    

@app.route('/customers/<int:id>', methods=['DELETE'])
def delete_customer(id):
    customer = Customers.query.get_or_404(id)
    db.session.delete(customer)
    db.session.commit()
    return jsonify({'message': 'Customer deleted successfully.'})
    

#CRUD Endpoints for Customer Accounts
@app.route('/customer_accounts', methods=['GET'])
def list_customer_accounts():
    customer_accounts = Customer_Accounts.query.all()
    return customer_accounts_schema.jsonify(customer_accounts)

@app.route('/customer_accounts', methods=['POST'])
def create_customer_account():
    try:
        customer_account_data = customer_account_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400
    new_customer_account = Customer_Accounts(username=customer_account_data['username'], password=customer_account_data['password'], email=customer_account_data['email'])
    db.session.add(new_customer_account)
    db.session.commit()
    return jsonify({'message': 'Customer account added successfully.'}), 201

@app.route('/customer_accounts/<int:id>', methods=['GET'])
def read_customer_account(id):
    customer_account_schema = Customer_Accounts.query.get_or_404(id)
    return customer_account_schema.jsonify(customer_account)

@app.route('/customer_accounts/<int:id>', methods=['PUT'])
def update_customer_account(id):
    customer_account = Customer_Accounts.query.get_or_404(id)
    try:
        customer_account_data = customer_account_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400
    customer_account.username = customer_account_data['username']
    customer_account.password = customer_account_data['password']
    customer_account.email = customer_account_data['email']
    db.session.commit()
    return jsonify({'message': 'Customer account updated successfully.'})

@app.route('/customer_accounts/<int:id>', methods=['DELETE'])
def delete_customer_account(id):
    customer_account = Customer_Accounts.query.get_or_404(id)
    db.session.delete(customer_account)
    db.session.commit()
    return jsonify({'message': 'Customer account deleted successfully.'})

#CRUD Endpoints for Products
@app.route('/products', methods=['POST'])
def create_product():
    try:
        product_data = product_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400
    new_product = Products(name=product_data['name'], price=product_data['price'])
    db.session.add(new_product)
    db.session.commit()
    return jsonify({'message': 'Product added successfully.'}), 201

@app.route('/products/<int:id>', methods=['GET'])
def read_product(id):
    product = Products.query.get_or_404(id)
    return product_schema.jsonify(product)

@app.route('/products/<int:id>', methods=['PUT'])
def update_product(id):
    product = Products.query.get_or_404(id)
    try:
        product_data = product_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400
    product.name = product_data['name']
    product.price = product_data['price']
    db.session.commit()
    return jsonify({'message': 'Product updated successfully.'})

@app.route('/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    product = Products.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    return jsonify({'message': 'Product deleted successfully.'})

@app.route('/products', methods=['GET'])
def list_products():
    products = Products.query.all()
    return products_schema.jsonify(products)
#View and Manage Product Stock Levels

@app.route('/products/<int:id>/stock', methods=['POST'])
def add_stock(id):
    try:
        stock_data = stock_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400
    new_stock = Stock(product_id=id, quantity=stock_data['quantity'])
    db.session.add(new_stock)
    db.session.commit()
    return jsonify({'message': 'Stock added successfully.'}), 201

@app.route('/products/<int:id>/stock', methods=['GET'])
def view_stock(id):
    stock = Stock.query.filter_by(product_id=id).first_or_404()
    return stock_schema.jsonify(stock)

@app.route('/products/<int:id>/stock', methods=['PUT'])
def restock_product(id):
    stock = Stock.query.filter_by(product_id=id).first_or_404()
    try:
        stock_data = stock_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400
    stock.quantity = stock_data['quantity']
    db.session.commit()
    return jsonify({'message': 'Stock updated successfully.'})
    
#Create an Order
@app.route('/orders', methods=['POST'])
def create_order_request():
    try:
        order_data = order_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400
    new_order = Orders(date=datetime.now(), customer_id=order_data['customer_id'])
    db.session.add(new_order)
    db.session.commit()
    return jsonify({'message': 'Order added successfully.'}), 201

#everything below here doesn't work I just changed it again and it still doesn't work if I could get some feedback on it I'd greatly appreciate it
@app.route('/orders/<int:id>/add_product', methods=['POST'])
def add_order_product(id):
    try:
        order_product_data = order_product_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400
    
    stock = Stock.query.filter_by(product_id=order_product_data['product_id']).first()
    if not stock or stock.quantity < order_product_data['quantity']:
        return jsonify({'error': 'Insufficient stock'}), 400

    stock.quantity -= order_product_data['quantity']

    new_order_product = Order_Products(
        order_id=id,
        product_id=order_product_data['product_id'],
        quantity=order_product_data['quantity']
    )
    db.session.add(new_order_product)
    db.session.commit()
    return jsonify({'message': 'Product added to order successfully.'}), 201

@app.route('/orders/<int:id>', methods=['GET'])
def view_order(id):
    order = Orders.query.get_or_404(id)
    order_products = Order_Products.query.filter_by(order_id=id).all()
    
    order_details = order_schema.dump(order)
    products = order_products_schema.dump(order_products)
    
    response = {
        'order': order_details,
        'products': products
    }
    return jsonify(response)

@app.route('/orders/<int:id>', methods=['DELETE'])
def delete_order(id):
    order = Orders.query.get_or_404(id)
    Order_Products.query.filter_by(order_id=id).delete()
    db.session.delete(order)
    db.session.commit()
    return jsonify({'message': 'Order and associated products deleted successfully.'})



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
