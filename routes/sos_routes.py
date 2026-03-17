from flask import Blueprint, request, jsonify
from firebase_config import db
import datetime

sos_bp = Blueprint("sos", __name__)

# 🚨 1️⃣ Trigger SOS
@sos_bp.route("/trigger", methods=["POST"])
def trigger_sos():
    try:
        data = request.json

        if not data:
            return jsonify({"error": "No data provided"}), 400

        user_id = data.get("user_id")
        latitude = data.get("latitude")
        longitude = data.get("longitude")

        if not user_id or not latitude or not longitude:
            return jsonify({"error": "Missing required fields"}), 400

        alert_data = {
            "user_id": user_id,
            "latitude": latitude,
            "longitude": longitude,
            "status": "active",
            "created_at": datetime.datetime.utcnow(),
            "updated_at": None,
            "closed_at": None
        }

        doc_ref = db.collection("sos_alerts").add(alert_data)

        return jsonify({
            "status": "success",
            "message": "SOS Triggered Successfully",
            "alert_id": doc_ref[1].id
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# 📍 2️⃣ Update Live Location
@sos_bp.route("/update/<alert_id>", methods=["POST"])
def update_location(alert_id):
    try:
        data = request.json

        latitude = data.get("latitude")
        longitude = data.get("longitude")

        if not latitude or not longitude:
            return jsonify({"error": "Missing location data"}), 400

        db.collection("sos_alerts").document(alert_id).update({
            "latitude": latitude,
            "longitude": longitude,
            "updated_at": datetime.datetime.utcnow()
        })

        return jsonify({
            "status": "success",
            "message": "Location Updated"
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ✅ 3️⃣ Close SOS
@sos_bp.route("/close/<alert_id>", methods=["POST"])
def close_sos(alert_id):
    try:
        db.collection("sos_alerts").document(alert_id).update({
            "status": "resolved",
            "closed_at": datetime.datetime.utcnow()
        })

        return jsonify({
            "status": "success",
            "message": "SOS Closed"
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    # ==============================
# GET SOS HISTORY
# ==============================
@sos_bp.route("/history/<user_id>", methods=["GET"])
def get_sos_history(user_id):

    alerts = db.collection("sos_alerts") \
        .where("user_id", "==", user_id) \
        .stream()

    history_list = []

    for doc in alerts:
        alert = doc.to_dict()
        alert["id"] = doc.id
        history_list.append(alert)

    return jsonify(history_list), 200
# ==============================
# GET SINGLE SOS
# ==============================
@sos_bp.route("/details/<alert_id>", methods=["GET"])
def get_sos_details(alert_id):

    doc = db.collection("sos_alerts").document(alert_id).get()

    if not doc.exists:
        return jsonify({"error": "SOS not found"}), 404

    alert = doc.to_dict()
    alert["id"] = doc.id

    return jsonify(alert), 200
