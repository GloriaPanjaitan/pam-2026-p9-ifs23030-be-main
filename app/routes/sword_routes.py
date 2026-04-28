import os
from flask import Blueprint, request, jsonify
from app.services.sword_service import (
    create_swords,
    get_all_swords
)

# Inisialisasi Blueprint
sword_bp = Blueprint("sword", __name__)

@sword_bp.route("/", methods=["GET"])
def index():
    # Identitas kamu tetap muncul sebagai respon root API
    return "API Sword GAGAL berjalan, tapi berlari"


# --- FITUR LOGIN STATIS (TANPA REGISTRASI) ---
@sword_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    # Mengambil kredensial dari file .env secara aman
    # Jika di .env belum diset, defaultnya adalah username 'gloria' & password '11S23030'
    ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "gloria")
    ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "11S23030")

    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        return jsonify({
            "status": "success",
            "message": "Login Berhasil!",
            "user": {
                "name": "Gloria Panjaitan",
                "nim": "11S23030"
            }
        }), 200
    else:
        return jsonify({
            "status": "error",
            "message": "Username atau Password salah!"
        }), 401


# --- FITUR GENERATE PEDANG (AI GEMINI) ---
@sword_bp.route("/swords/generate", methods=["POST"])
def generate():
    data = request.get_json()
    country = data.get("country")
    total = data.get("total")

    if not country:
        return jsonify({"error": "Country is required"}), 400

    if not total:
        return jsonify({"error": "Total count is required"}), 400

    # Validasi angka 1-10 sesuai permintaanmu
    try:
        total = int(total)
    except ValueError:
        return jsonify({"error": "Total harus berupa angka"}), 400

    if total <= 0:
        return jsonify({"error": "Jumlah harus lebih besar dari 0"}), 400

    if total > 10:
        return jsonify({"error": "Jumlah maksimal adalah 10"}), 400

    try:
        # Memanggil service pedang untuk proses AI
        result = create_swords(country, total)

        return jsonify({
            "country": country,
            "total_requested": total,
            "total_found": len(result),
            "data": result
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# --- FITUR HISTORY PENCALIAN ---
@sword_bp.route("/swords", methods=["GET"])
def get_all():
    page = request.args.get("page", default=1, type=int)
    per_page = request.args.get("per_page", default=10, type=int)

    # Mengambil histori pencarian pedang dari database
    data = get_all_swords(page=page, per_page=per_page)

    return jsonify(data)