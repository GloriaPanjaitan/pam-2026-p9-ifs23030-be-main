from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.extensions import db  # Pastikan import ini sesuai dengan extensions.py kamu

class RequestLog(db.Model):
    __tablename__ = "requests"

    id = Column(Integer, primary_key=True)
    # Kita ubah theme menjadi country
    country = Column(String(100), nullable=False)
    # Kita tambahkan kolom untuk menyimpan jumlah pedang yang diminta
    requested_count = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<RequestLog {self.country} - {self.requested_count} blades>"