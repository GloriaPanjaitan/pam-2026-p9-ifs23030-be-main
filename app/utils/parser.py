import json
import re

def parse_llm_response(result):
    """
    Fungsi ini berguna jika di kemudian hari Gloria ingin Gemini
    mengeluarkan data dalam format JSON yang terstruktur (misal untuk tabel pedang).
    """
    try:
        # Mengambil string response dari dictionary
        content = result.get("response") if isinstance(result, dict) else result

        # 🔥 Pembersih Markdown: Menghapus bungkus ```json ... ``` agar tidak error saat di-parse
        content = re.sub(r"```json\n|\n```", "", content)
        content = content.strip()

        parsed = json.loads(content)

        # Kita ganti key-nya dari 'motivations' menjadi 'swords'
        return parsed.get("swords", [])

    except Exception as e:
        # Jika bukan JSON, kita kembalikan teks aslinya sebagai list agar sistem tidak crash
        return [{"name": "Info", "description": content}]