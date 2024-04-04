from bson import objectid
from flask import Flask, request, jsonify, Response
from flask.json import jsonify
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
from bson import json_util
from bson.objectid import ObjectId
from werkzeug.wrappers import response


app = Flask(__name__)
app.config['MONGO_URI']='mongodb://localhost/pythonmongodb' #27017 defecto
mongo = PyMongo(app)

@app.route('/users', methods=['POST'])
def create_user():
    # Receiving data
    username = request.json['username']
    password= request.json['password']
    email = request.json['email']

    if username and password and email:
        hash_pwd = generate_password_hash(password)
        id = mongo.db.users.insert_one(
            {'username': username, 'password': hash_pwd, 'email': email}
        )
        response = {
            'id': str(id),
            'username': username,
            'password': hash_pwd,
            'email': email
        }
        return response
    return {'message':'received'}
       
@app.route('/users/<id>', methods=['GET'])
def get_user(id):
    user = mongo.db.users.find_one({'_id': ObjectId(id)})
    response = json_util.dumps(user)
    return Response(response, mimetype='applocation/json')

@app.route('/users/<id>', methods=['DELETE'])
def delete_user(id):
    mongo.db.users.delete_one({'id': ObjectId(id)})
    response = jsonify({'message': 'User' + id + 'was Deleted successfully'})
    return response

@app.route('/users/<id>', methods=['PUT'])
def update_user(id):
    username = request.json['username']
    password= request.json['password']
    email = request.json['email']

    if username and password and email:
        hash_pwd = generate_password_hash(password)
        mongo.db.users.update_one({'_id': ObjectId(id)}, {'$set':{'username': username,'password': hash_pwd,'email': email}})
        response = jsonify({'message': 'user' + id + 'was Update sucessfully'})
        return response

@app.route('/users', methods=['GET'])
def get_users():
    users = mongo.db.users.find()
    response = json_util.dumps(users)
    return Response(response, mimetype='application/json')

@app.errorhandler(404)
def not_found(error=None):
    response = jsonify({
        'message': 'Resource not found:' + request.url,
        'status': 404
    })
    response.status_code = 404
    return response

if __name__ == '__main__':
    app.run(debug=True)
