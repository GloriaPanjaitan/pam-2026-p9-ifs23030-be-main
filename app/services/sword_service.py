from app.extensions import SessionLocal
from app.models.sword import Sword
from app.models.request_log import RequestLog
from app.services.llm_service import generate_from_llm

def create_swords(country: str, total: int):
    session = SessionLocal()

    try:
        # Memanggil fungsi LLM yang sudah kita modifikasi sebelumnya
        # Kita mengirimkan 'country' dan 'total' langsung
        result = generate_from_llm(country, total)

        # Mengambil teks jawaban dari dictionary yang dikembalikan LLMService
        ai_response_text = result.get("response")

        # 1. Simpan riwayat request ke RequestLog
        req_log = RequestLog(
            country=country,
            requested_count=total
        )
        session.add(req_log)
        session.commit() # Commit agar kita dapat ID-nya

        # 2. Simpan hasil jawaban AI ke tabel Sword
        new_sword_entry = Sword(
            content=ai_response_text,
            request_id=req_log.id
        )
        session.add(new_sword_entry)
        session.commit()

        # Kita kembalikan hasilnya dalam bentuk list agar sesuai dengan format route
        return [ai_response_text]

    except Exception as e:
        session.rollback()
        raise e

    finally:
        session.close()


def get_all_swords(page: int = 1, per_page: int = 10):
    session = SessionLocal()

    try:
        # Mengambil data dari tabel Sword
        query = session.query(Sword)
        total_data = query.count()

        data = (
            query
            .order_by(Sword.id.desc())
            .offset((page - 1) * per_page)
            .limit(per_page)
            .all()
        )

        result = [
            {
                "id": s.id,
                "content": s.content,
                "request_id": s.request_id,
                "created_at": s.created_at.isoformat()
            }
            for s in data
        ]

        return {
            "page": page,
            "per_page": per_page,
            "total": total_data,
            "total_pages": (total_data + per_page - 1) // per_page,
            "data": result
        }

    finally:
        session.close()