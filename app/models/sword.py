from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey
from datetime import datetime, timezone
from app.extensions import db # Mengikuti standar Flask-SQLAlchemy

class Sword(db.Model):
    __tablename__ = "swords"

    id = Column(Integer, primary_key=True)
    # Kolom 'text' ini akan menyimpan jawaban lengkap dari Gemini tentang pedang
    content = Column(Text, nullable=False)
    # Menghubungkan hasil ini dengan riwayat request (negara & jumlah)
    request_id = Column(Integer, ForeignKey("requests.id"))
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f"<Sword result for request_id {self.request_id}>"