"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

last_name = "Jackson"
_members = [
    {
        "first_name": "John",
        "age": 33,
        "lucky_numbers": [7,13,22]
    },
    {
        "first_name": "Jane",
        "age": 35,
        "lucky_numbers": [10,14,3]
    },
    {
        "first_name": "Jimmy",
        "age": 5,
        "lucky_numbers": [1]
    }
]

jackson_family = FamilyStructure(last_name)

for member in _members:
    jackson_family.add_member(member)

@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

@app.route('/')
def sitemap():
    return generate_sitemap(app)

# GET ALL MEMBERS
@app.route('/members', methods=['GET'])
def handle_hello():

    try:
        jackson_family
    except NameError:
        return jsonify({"msg": "Family does not exist"}), 500
    else:
        members = jackson_family.get_all_members()
        return jsonify(members), 200

# GET MEMBER
@app.route('/member/<int:member_id>', methods=['GET'])
def get_member(member_id):
    try:
        jackson_family
    except NameError:
        return jsonify({"msg": "Family does not exist"}), 500
    
    member = jackson_family.get_member(member_id)

    if member:
        return jsonify(member),200
    else:
        return jsonify({"msg": "Member does not exist"}), 400


# ADD MEMBER
@app.route('/member', methods=['POST'])
def add_member():
    try:
        jackson_family
    except NameError:
        return jsonify({"msg":"Family doesnt exist"}),500

    data = request.get_json()

    try:
        first_name = data["first_name"]
        if not isinstance(first_name, str):
            raise ValueError()
    except KeyError:
        return jsonify({"msg": "Name is required"}), 400
    except ValueError:
        return jsonify({"msg": "Don't be ridiculous"}), 400

    try:
        age = int(data["age"])
        if age < 0:
            raise Exception()
    except KeyError:
        return jsonify({"msg": "Age is required"}), 400
    except Exception:
        return jsonify({"msg": "Don't be ridiculous"}), 400

    try:
        lucky_numbers = data["lucky_numbers"]
    except KeyError:
        return jsonify({"msg": "Lucky numbers are required"}), 400

    new_member = {
        "first_name": first_name,
        "age": age,
        "lucky_numbers": lucky_numbers
    }

    if data["id"]:
        id = data["id"]
        new_member["id"] = int(id)
            
    jackson_family.add_member(new_member)

    return jsonify({"msg": "Member added"}), 200

# DELETE MEMBER
@app.route('/member/<int:id>', methods=['DELETE'])
def delete_member(id):
    try:
        jackson_family
    except NameError:
        return jsonify({"msg": "Family does not exist"}),500

    if jackson_family.delete_member(id):
        return jsonify({"done": True}), 200
    else:
        return jsonify({"msg":"Member not found"}), 404

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)