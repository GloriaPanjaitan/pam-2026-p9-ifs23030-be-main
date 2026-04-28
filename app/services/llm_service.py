import os
from google import genai

def generate_from_llm(country: str, count: int):
    try:
        # Inisialisasi client
        # Pastikan di file .env kamu kuncinya adalah GEMINI_API_KEY
        client = genai.Client()

        # Kita buat prompt yang sangat spesifik sesuai permintaanmu
        prompt = f"""
        Kamu adalah seorang kurator museum senjata bersejarah.
        
        TUGAS:
        Berikan daftar {count} jenis pedang tradisional atau legendaris yang berasal dari negara: {country}.
        
        FORMAT JAWABAN:
        1. Sebutkan nama pedang.
        2. Berikan deskripsi singkat bentuk dan kegunaannya.
        3. Berikan sejarah singkat atau fakta menariknya.
        
        ATURAN KHUSUS:
        - Jika negara '{country}' ternyata hanya memiliki jumlah pedang ikonik yang kurang dari {count}, 
          tampilkan semua yang tersedia saja.
        - Jika hal itu terjadi, di akhir jawaban WAJIB tambahkan kalimat: 
          "Catatan: Hanya pedang-pedang ini yang merupakan ciri khas utama dari negara tersebut."
        - Gunakan bahasa Indonesia yang santai tapi edukatif.
        - Jika input '{country}' bukan nama negara yang valid, jawab dengan: "Maaf, data pedang untuk wilayah tersebut tidak ditemukan."
        """

        # Menggunakan model Gemini 1.5 Flash (atau 2.0 jika tersedia di akunmu)
        response = client.models.generate_content(
            model='gemini-1.5-flash',
            contents=prompt,
        )

        raw_text = response.text

        # Pembersihan markdown jika ada
        if raw_text.startswith("```json"):
            raw_text = raw_text.replace("```json", "", 1).replace("```", "")
        elif raw_text.startswith("```"):
            raw_text = raw_text.replace("```", "")

        raw_text = raw_text.strip()

        return {
            "country": country,
            "requested_count": count,
            "response": raw_text
        }

    except Exception as e:
        raise Exception(f"PESAN ASLI GEMINI: {str(e)}")