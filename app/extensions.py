from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import Config

# Membuat koneksi ke database
engine = create_engine(Config.SQLALCHEMY_DATABASE_URI, echo=False)

# SessionLocal untuk operasi database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base untuk model SQLAlchemy
Base = declarative_base()

# 🔥 SOLUSI ERROR: Tambahkan class ini agar 'db.Model' bisa terbaca
class DatabaseProxy:
    Model = Base

db = DatabaseProxy()