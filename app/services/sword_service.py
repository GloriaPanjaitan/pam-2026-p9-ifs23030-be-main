from app.extensions import SessionLocal
from app.models.sword import Sword
from app.models.request_log import RequestLog
from app.services.llm_service import generate_from_llm

def create_swords(country: str, total: int):
    session = SessionLocal()

    try:
        swords = generate_from_llm(country, total)

        req_log = RequestLog(
            country=country,
            requested_count=total
        )
        session.add(req_log)
        session.commit()

        result = []

        for item in swords:
            new_sword = Sword(
                content=item["description"],
                request_id=req_log.id
            )
            session.add(new_sword)

            result.append({
                "name": item["name"],
                "description": item["description"]
            })

        session.commit()

        return result

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