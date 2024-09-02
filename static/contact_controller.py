import pymongo
from flask import Flask, jsonify, request

app = Flask(__name__)
mongo = pymongo.MongoClient('mongodb://localhost:27017/')
dataBase = mongo['contact_flask']


@app.route('/sign_up', methods=['POST'])
def sign_up():
    data = request.get_json()
    user_name = data['user_name']
    email = data['email']
    if "@" not in email or "." not in email:
        return jsonify({"message": "Opps, you missed @ or ."}), 400
    if email:
        dataBase.note.find_one({"email": email})
        return jsonify({"Email already exits"}), 400
    else:
        password = data['password']
        if not password or not email:
            return jsonify({"message": "Invalid email or password"}), 400
        else:
            dataBase.note.insert_one({"email": email, "password": password, "user_name": user_name})
    return jsonify({"message": "Successfully signup"}), 201


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data['email']
    password = data['password']
    if password or email:
        dataBase.note.find_one({"password": password, "email": email})
        return jsonify({"message": "Invalid password"})
    if not email or not password:
        return jsonify({"message": "Wrong password or email"})


@app.route('/addContact', methods=["POST"])
def addContact():
    data = request.get_json()
    first_name = data['first_name']
    last_name = data['last_name']
    phone_number = data['phone_number']
    validate_phone_number = dataBase.note.find_one({"phone_number": phone_number}), 400
    if validate_phone_number:
        return jsonify({"message": phone_number + " " + " phone number already exist"})
    email = data['email']
    validate_email = dataBase.note.find_one({"email": email}), 400
    if validate_email:
        return jsonify({"message": email + " " + " email already exist"})
    else:
        dataBase.note.insert_one({"first_name": first_name,
                                  "last_name": last_name,
                                  "phone_number": phone_number,
                                  "email": email})
    return jsonify({
        "message": "Contact created successfully"}), 201


@app.route('/updateContact', methods=['PATCH'])
def updateContact():
    data = request.get_json()
    first_name = data['first_name']
    last_name = data['last_name']
    phone_number = data['phone_number']
    validate_phone_number = dataBase.note.find_one({"phone_number": phone_number})
    if validate_phone_number:
        return jsonify({"message": phone_number + " Already exists"}), 400
    email = data['email']
    validate_contact_email = dataBase.note.find_one({"email": email})
    if validate_contact_email:
        return jsonify({"message": email + " Already exists"}), 400
    dataBase.note.update_one({"email": email}, {"$set": {"phone_number": phone_number, "first_name": first_name,
                                                         "last_name": last_name,
                                                         }})
    return jsonify({
        "message": "Contact updated successfully"
    }), 200


@app.route('/delete_contact_', methods=['DELETE'])
def deleteContactBy():
    data = request.get_json()
    phone_number = data.get('phone_number')
    validata_phone_number = dataBase.note.find_one({"phone_number": phone_number})
    if not validata_phone_number:
        return jsonify({"message": "phone number not found"}), 400
    else:
        dataBase.note.delete_one({"phone_number": phone_number})
        return jsonify({
            "message": "You've successfully deleted this contact"
        }), 201
