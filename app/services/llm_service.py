import json
from google import genai

def generate_from_llm(country: str, count: int):
    try:
        client = genai.Client()

        prompt = f"""
        Kamu adalah ahli sejarah senjata.

        TUGAS:
        Buat {count} pedang legendaris dari negara {country}.

        FORMAT OUTPUT (WAJIB JSON VALID):
        [
          {{
            "name": "Nama Pedang",
            "description": "Deskripsi lengkap + sejarah singkat"
          }}
        ]

        ATURAN:
        - Output HARUS JSON saja
        - TANPA penjelasan tambahan
        - TANPA markdown
        """

        response = client.models.generate_content(
            model='gemini-1.5-flash-latest',
            contents=prompt,
        )

        raw_text = response.text.strip()

        # 🔥 Bersihkan kalau AI kasih markdown
        if raw_text.startswith("```"):
            raw_text = raw_text.replace("```json", "").replace("```", "").strip()

        # 🔥 Convert ke JSON
        parsed = json.loads(raw_text)

        # Validasi basic biar aman
        if not isinstance(parsed, list):
            raise Exception("Format AI bukan list")

        return parsed

    except Exception as e:
        raise Exception(f"Gagal parse AI: {str(e)}")