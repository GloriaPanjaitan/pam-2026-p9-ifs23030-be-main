from flask import Flask
from flask_cors import CORS
from app.extensions import Base, engine
# Kita ganti import agar sesuai dengan nama file dan blueprint yang baru
from app.routes.sword_routes import sword_bp

def create_app():
    app = Flask(__name__)

    # Enable CORS agar Flutter bisa mengakses backend ini
    CORS(app)

    # Membuat tabel secara otomatis di database (SQLite/MySQL)
    # Ini akan membuat tabel 'requests' dan 'swords'
    Base.metadata.create_all(bind=engine)

    # Register blueprint dengan nama yang sudah kita ubah
    app.register_blueprint(sword_bp)

    return app

if __name__ == "__main__":
    app = create_app()
    # Berjalan di port 5000
    app.run(host="0.0.0.0", port=5000, debug=True)