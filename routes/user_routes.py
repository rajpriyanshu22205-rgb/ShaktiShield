from flask import Blueprint, request, jsonify, current_app
import jwt
import datetime
from functools import wraps
from firebase_config import db   # ✅ Import Firestore from config

# Blueprint
user_bp = Blueprint("user_bp", __name__)

# ============================================
# TOKEN REQUIRED DECORATOR
# ============================================

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        # Get token from Authorization header
        if "Authorization" in request.headers:
            auth_header = request.headers["Authorization"]
            parts = auth_header.split(" ")

            if len(parts) == 2 and parts[0] == "Bearer":
                token = parts[1]

        if not token:
            return jsonify({"error": "Token is missing"}), 401

        try:
            data = jwt.decode(
                token,
                current_app.config["SECRET_KEY"],
                algorithms=["HS256"]
            )

            current_user_id = data["user_id"]

        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expired"}), 401

        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401

        return f(current_user_id, *args, **kwargs)

    return decorated


# ============================================
# LOGIN ROUTE (Temporary Hardcoded Login)
# ============================================

@user_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    # Temporary test credentials
    if email == "rishabh@gmail.com" and password == "123456":

        token = jwt.encode(
            {
                "user_id": 1,
                "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
            },
            current_app.config["SECRET_KEY"],
            algorithm="HS256"
        )

        return jsonify({"token": token}), 200

    return jsonify({"error": "Invalid credentials"}), 401


# ============================================
# PROTECTED ROUTE
# ============================================

@user_bp.route("/protected", methods=["GET"])
@token_required
def protected(current_user_id):
    return jsonify({
        "message": "Access granted",
        "user_id": current_user_id
    }), 200


# ============================================
# GET ALL USERS FROM FIRESTORE
# ============================================

@user_bp.route("/users", methods=["GET"])
def get_users():
    try:
        users_ref = db.collection("users")
        docs = users_ref.stream()

        users_list = []

        for doc in docs:
            user_data = doc.to_dict()
            user_data["id"] = doc.id
            users_list.append(user_data)

        return jsonify(users_list), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 
# ==============================
# ADD EMERGENCY CONTACT
# ==============================
@user_bp.route("/add-contact", methods=["POST"])
def add_contact():
    data = request.json

    user_id = data.get("user_id")
    name = data.get("contactName")
    number = data.get("contactNumber")
    relation = data.get("contactRelation")

    if not user_id or not name or not number:
        return jsonify({"error": "Missing required fields"}), 400

    contact_data = {
        "userId": user_id,
        "contactName": name,
        "contactNumber": number,
        "contactRelation": relation
    }

    doc_ref = db.collection("emergency_contacts").add(contact_data)

    return jsonify({
        "message": "Contact added successfully",
        "contact_id": doc_ref[1].id
    }), 201


# ==============================
# GET EMERGENCY CONTACTS
# ==============================
@user_bp.route("/get-contacts/<user_id>", methods=["GET"])
def get_contacts(user_id):

    contacts = db.collection("emergency_contacts") \
        .where("userId", "==", user_id).stream()

    contact_list = []

    for doc in contacts:
        contact = doc.to_dict()
        contact["id"] = doc.id
        contact_list.append(contact)

    return jsonify(contact_list), 200


# ==============================
# DELETE CONTACT
# ==============================
@user_bp.route("/delete-contact/<contact_id>", methods=["DELETE"])
def delete_contact(contact_id):

    db.collection("emergency_contacts").document(contact_id).delete()

    return jsonify({"message": "Contact deleted successfully"}), 200