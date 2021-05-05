from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
from products import products


app = Flask(__name__)
app.config['MONGO_URI']='mongodb://localhost/ecommercetest'
mongo = PyMongo(app)

@app.route('/users', methods=['POST'])
def create_user():
  username = request.json['username']
  email = request.json['email']
  password = request.json['password']

  if username and email and password:
    hashed_password = generate_password_hash(password)
    id = mongo.db.user.insert_one(
      {'username': username,
      'email': email,
      'password': hashed_password
      }
    )
    response = {
      'message': 'user created',
      'id': str(id),
      'username':username
    }
    return response
  else:
    return {'message': 'ERROR: something went wrong'}


@app.route('/ping')
def ping():
  return jsonify({"menssage": "pong!"})

@app.route('/products', methods=['GET'])
def getProducts():
  return jsonify({"products": products, "message": "Products List"})

@app.route('/product/<string:name>')
def getProduct(name):
  print(name)
  productsFound = [product for product in products if product['name'] == name]
  if (len(productsFound) > 0):
    return jsonify({"product": productsFound[0]})
  return jsonify({"product":"Not Found"})

@app.route('/products', methods=['POST'])
def addProduct():
  new_product = {
    "name": request.json['name'],
    "price": request.json['price'],
    "quantity": request.json['quantity']
  }
  products.append(new_product)
  return jsonify({"message": "Product Added Succesfully", "products": products})

@app.route('/products/<string:name>', methods=['PUT'])
def editProduct(name):
  productFound = [product for product in products if product['name'] == name]
  if (len(productFound)>0):
    productFound[0]['name'] = request.json['name']
    productFound[0]['price'] = request.json['price']
    productFound[0]['quantity'] = request.json['quantity']
    return jsonify({
      "message": "Product Updated",
      "product": productFound[0]
    })
  return jsonify({"message": "Product Not Found"})

@app.route('/products/<string:name>', methods=['DELETE'])
def deleteProduct(name):
  productFound = [product for product in products if product['name'] == name]
  if (len(productFound)>0):
    products.remove(productFound[0])
    return jsonify({
      "message": "Product Deleted",
      "products": products
    })
  return jsonify({"message": "Product Not Found"})

if __name__ == '__main__':
  app.run(debug=True,port=4000)