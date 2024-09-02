import pymongo
from flask import request, jsonify, Flask
from pymongo import MongoClient

app = Flask(__name__)
mongo = pymongo.MongoClient('mongodb://localhost:27017/')
dataBase = mongo['contact_flask']


@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    first_name = data['first_name']
    last_name = data['last_name']
    user_name = data['user_name']
    phone_number = data['phone_number']
    email = data['email']
    isPhoneNumber_Exist = dataBase.note.find_one({"phone_number": phone_number})
    isEmail_Exist = dataBase.note.find_one({"email": email})
    if isEmail_Exist:
        return jsonify({"message": " Account Already exist "})
    if isPhoneNumber_Exist:
        return jsonify({"message": "Phone number already exist"})
    if "@" not in email or "." not in email:
        return jsonify({"message": "Email must contain @ and ."}), 400
    else:
        password = data['password']
        if " " in password or " " in email:
            return jsonify({"message": "Enter an email or password"}), 400
        if " " in user_name:
            return jsonify({"message": "Enter a valid user name"}), 400
        if " " in first_name:
            return jsonify({"message": "Enter your first name"}), 400
        if " " in last_name:
            return jsonify({"message": "Enter your last name"}), 400
        else:
            dataBase.note.insert_one({"last_name": last_name, "first_name": first_name,
                                      "email": email, "password": password,
                                      "user_name": user_name, "phone_number": phone_number})
    return jsonify({"message": "Successfully signup"}), 201


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data['email']
    password = data['password']

    user = dataBase.note.find_one({"password": password, "email": email})
    if not user:
        return jsonify({"message": "Wrong password or email"}), 401
    if password or email:
        dataBase.note.insert_one({"email": email, "password": password})
        return jsonify({"message": "Successfully logged in"}), 200


def isLoggedIn():
    if isLoggedIn():
        return True
    else:
        return False


@app.route('/addContact', methods=['POST'])
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
        return jsonify({"message": email + " " + " email already exist"}), 400
    # isSignup = dataBase.note.find_one({"email": email, "phone_number": phone_number})
    # if not isSignup:
    #     return jsonify({"message": "Please Kindly Signup"})
    else:
        dataBase.note.insert_one({"first_name": first_name, "last_name": last_name, "phone_number": phone_number,
                                  "email": email})
    return jsonify({
        "message": "Contact created successfully"}), 201


@app.route('/updateContact', methods=['PUT'])
def updateContact():
    data = request.get_json()
    first_name = data['first_name']
    last_name = data['last_name']
    phone_number = data['phone_number']
    validate_phone_number = dataBase.note.find_one({"phone_number": phone_number})
    if validate_phone_number:
        return jsonify({"message": phone_number + " Does not exists"}), 400
    email = data['email']
    validate_contact_email = dataBase.note.find_one({"email": email})
    if validate_contact_email:
        return jsonify({"message": email + " Does not exists"}), 400
    else:
        dataBase.note.update_one({"email": email}, {"$set": {"first_name": first_name, "last_name": last_name,
                                                             "phone_number": phone_number}})
    return jsonify({
        "message": "Contact updated successfully"}), 200


@app.route('/deleteContact', methods=['DELETE'])
def deleteContactBy():
    data = request.get_json()
    phone_number = data.get('phone_number')
    validata_phone_number = dataBase.note.find_one({"phone_number": phone_number})
    if not validata_phone_number:
        return jsonify({"message": "phone number not found"}), 404
    else:
        dataBase.note.delete_one({"phone_number": phone_number})
        return jsonify({
            "message": "You've successfully deleted this contact."
        }), 201

@app.route('/displayContact', methods=['GET'])
def displayContact():
    contacts = dataBase.note.find()
    contact_list = list(contacts)
    return jsonify(contacts=contact_list)


if __name__ == '__main__':
    app.run(Debug=True)
