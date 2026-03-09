import os
from google.adk.agents.llm_agent import Agent
from google.adk.models.google_llm import Gemini
from google.adk.tools import VertexAiSearchTool
from google.adk.tools.agent_tool import AgentTool
from google.genai import types
from toolbox_core import ToolboxSyncClient

from google.adk.a2a.utils.agent_to_a2a import to_a2a

from google.auth.transport.requests import Request as GoogleAuthRequest
import google.oauth2.id_token
import subprocess
from dotenv import load_dotenv

load_dotenv()

# Configure Retry Options
retry_config=types.HttpRetryOptions(
    attempts=5,  # Maximum retry attempts
    exp_base=7,  # Delay multiplier
    initial_delay=1, # Initial delay before first retry (in seconds)
    http_status_codes=[429, 500, 503, 504] # Retry on these HTTP errors
)

# 1. Create a function that fetches a fresh token dynamically
def get_bearer_token() -> str:
    credentials, project_id = google.auth.default()

    if hasattr(credentials, "id_token_info"):
         req = GoogleAuthRequest()
         credentials.refresh(req)
         token = credentials.token
    else:
         from google.oauth2 import id_token
         req = GoogleAuthRequest()
         
         try:
             token = id_token.fetch_id_token(req, server_url)
         except google.auth.exceptions.DefaultCredentialsError:
             
             result = subprocess.run(
                 ["gcloud", "auth", "print-identity-token"], 
                 capture_output=True, 
                 text=True, 
                 check=True,
                 shell=True
             )
             token = result.stdout.strip()
             
    return f"Bearer {token}"

# 2. Map the Authorization header to your function
headers = {
    "Authorization": get_bearer_token
}

server_url=os.getenv("TOOLBOX_URL")
toolbox = ToolboxSyncClient(
                            server_url,
                            client_headers=headers
                            )
hospital_toolset = toolbox.load_toolset("hospital_toolset",)

# ---
vertex_ai_search_agent = Agent(
    model=Gemini(model='gemini-2.5-flash', retry_options=retry_config),
    name='vertex_ai_search_agent',
    description=(
        'Agen ini berfungsi sebagai asisten ahli mengenai Standar Tarif Pelayanan Kesehatan dalam '
        'Program Jaminan Kesehatan berdasarkan Peraturan Menteri Kesehatan RI Nomor 3 Tahun 2023. '
        'Agen memiliki akses mendalam terhadap detail tarif kapitasi, non-kapitasi, serta tarif INA-CBG dan Non INA-CBG '
        'yang berlaku di Fasilitas Kesehatan Tingkat Pertama (FKTP) maupun Fasilitas Kesehatan Rujukan Tingkat Lanjutan (FKRTL).'
    ),
    instruction="""
    Anda adalah asisten spesialis tarif JKN (Jaminan Kesehatan Nasional). 
    Gunakan instruksi berikut untuk memandu respons Anda:
    - **Basis Informasi**: Selalu gunakan data yang tersedia dalam menjawab pertanyaan seputar biaya dan standar pelayanan kesehatan.
    - **Klasifikasi Tarif**: Jika ditanya tentang biaya di Puskesmas, Klinik Pratama, atau Dokter Mandiri, carilah informasi pada bagian Tarif Kapitasi atau Non Kapitasi. Jika ditanya tentang biaya rumah sakit atau prosedur medis kompleks (seperti operasi atau rawat inap spesialis), rujuklah ke bagian Tarif INA-CBG.
    - **Detail Penyakit**: Untuk pertanyaan spesifik penyakit (contoh: demam, infeksi, atau prosedur bedah), cari kode diagnosis atau deskripsi penyakit dalam lampiran tarif INA-CBG sesuai dengan kelas perawatan (Kelas 1, 2, atau 3) dan tingkat keparahan (Ringan, Sedang, Berat).
    - **Akurasi Wilayah**: Perhatikan bahwa tarif INA-CBG dapat berbeda berdasarkan Regional wilayah rumah sakit. Selalu informasikan jika ada perbedaan tarif antar regional jika relevan.
    - **Gaya Bahasa**: Berikan jawaban yang informatif, teknis namun mudah dipahami, serta sebutkan kategori tarif (misal: "Berdasarkan tarif INA-CBG Regional 1...") agar pengguna memahami konteks biaya tersebut.
    """,
    tools=[VertexAiSearchTool(data_store_id="projects/bmhs-ai/locations/global/collections/default_collection/dataStores/bmhs-datastore_1772762883301",max_results=5)]
)

vertex_ai_search_tool = AgentTool(agent=vertex_ai_search_agent)

# --- 
mcp_agent  = Agent(
    model=Gemini(model='gemini-2.5-flash', retry_options=retry_config),
    name='mcp_agent',
    description='Agen untuk menjawab pertanyaan berkaitan dengan operasi rumah sakit seperti mencari dokter berdasarkan spesialisasi, mencari nama pasien, Mencari riwayat kunjungan pasien berdasarkan keluhan.',
        instruction="""
    Anda adalah agen operasi rumah sakit yang membantu pengguna menemukan informasi terkait dokter, pasien, dan riwayat kunjungan pasien.

    Tanggung jawab utama Anda:
    1. Menjawab pertanyaan tentang dokter berdasarkan spesialisasi.
    2. Mencari data pasien berdasarkan nama pasien.
    3. Menemukan riwayat kunjungan pasien berdasarkan keluhan atau informasi lain yang diberikan.
    4. Menggunakan tool yang tersedia untuk mengambil data dari sistem rumah sakit.

    Aturan penggunaan:
    - Selalu gunakan tool yang tersedia ketika pertanyaan memerlukan data dari sistem.
    - Jangan membuat atau mengarang data pasien, dokter, atau kunjungan.
    - Jika informasi yang diberikan pengguna tidak cukup jelas, minta klarifikasi terlebih dahulu.
    - Jika hasil pencarian kosong, jelaskan bahwa data tidak ditemukan.

    Format jawaban:
    - Berikan jawaban yang singkat, jelas, dan mudah dipahami.
    - Jika hasil berupa daftar (misalnya daftar dokter), tampilkan dalam bentuk bullet list.
    - Sertakan informasi penting seperti nama dokter, spesialisasi, nama pasien, tanggal kunjungan, dan keluhan jika tersedia.

    Contoh pertanyaan pengguna:
    - "Cari dokter spesialis jantung."
    - "Cari pasien bernama Budi Santoso."
    - "Riwayat kunjungan pasien dengan keluhan demam."

    Tujuan Anda adalah membantu pengguna mendapatkan informasi operasional rumah sakit dengan cepat dan akurat.
    """,
    tools=hospital_toolset
)

mcp_agent_tool  = AgentTool(agent=mcp_agent)

root_agent = Agent(
    model=Gemini(model='gemini-2.5-flash', retry_options=retry_config),
    name='root_agent',
    description='Agen ini berfungsi sebagai gerbang utama untuk menangani semua permintaan pengguna, mulai dari pencarian data operasional (dokter, pasien, kunjungan) hingga konsultasi mengenai standar tarif JKN sesuai regulasi pemerintah.',
    instruction="""
    Anda adalah Koordinator Utama Layanan Informasi Rumah Sakit. Tugas Anda adalah menganalisis pertanyaan pengguna dan meneruskannya ke sub-agen yang tepat.

    Gunakan panduan berikut dalam menjalankan tugas:

    1. KLASIFIKASI PERTANYAAN:
    - Jika pertanyaan berkaitan dengan regulasi pemerintah, biaya pengobatan, tarif BPJS/JKN, tarif kapitasi, atau detail biaya berdasarkan penyakit (contoh: "Berapa biaya operasi katarak?"), gunakan 'vertex_ai_search_tool'.
    - Jika pertanyaan berkaitan dengan data internal rumah sakit, seperti mencari jadwal/nama dokter, data pasien, atau melihat riwayat kunjungan medis (contoh: "Siapa dokter jantung yang praktek hari ini?" atau "Cek riwayat kunjungan pasien Budi"), gunakan 'mcp_agent_tool'.

    2. PENANGANAN PERTANYAAN CAMPURAN:
    - Jika pengguna bertanya tentang dua hal sekaligus (contoh: "Siapa dokter anak yang tersedia dan berapa biaya konsultasinya?"), panggillah kedua agen secara berurutan dan gabungkan informasinya menjadi satu jawaban yang komprehensif.

    3. KETENTUAN KOMUNIKASI:
    - Bersikaplah profesional, membantu, dan efisien.
    - Jangan memberikan informasi medis atau tarif berdasarkan asumsi; selalu andalkan hasil dari sub-agen.
    - Jika input pengguna ambigu, mintalah klarifikasi (contoh: "Apakah Anda ingin mencari riwayat medis pasien atau informasi tarif umum untuk keluhan tersebut?").

    4. FORMAT JAWABAN:
    - Sampaikan jawaban langsung pada intinya.
    - Jika data berasal dari 'vertex_ai_search_tool', pastikan menyebutkan bahwa informasi tersebut berdasarkan PMK No. 3 Tahun 2023.
    - Jika data berasal dari 'mcp_agent_tool', tampilkan informasi operasional secara terstruktur (seperti tabel atau daftar poin).
    """,
    tools=[
        vertex_ai_search_tool,
        mcp_agent_tool
        ]   
)

current_dir = os.path.dirname(os.path.abspath(__file__))
agent_card_path = os.path.join(current_dir, 'agent.json')

a2a_app = to_a2a(
                root_agent, 
                port=8001,
                agent_card=agent_card_path,
                 )

# ---
import requests
from fastapi import Request
from fastapi.responses import JSONResponse

# 1. Define allowed emails (Load from environment variable for security)
# Example format in .env: ALLOWED_EMAILS=doctor1@bmhs.co.id,admin@bmhs.co.id
allowed_emails_env = os.getenv("ALLOWED_EMAILS", "")
ALLOWED_EMAILS =[email.strip() for email in allowed_emails_env.split(",") if email.strip()]

@a2a_app.middleware("http")
async def restrict_by_email(request: Request, call_next):
    public_paths =["/agent.json", "/docs", "/openapi.json"]
    
    if request.url.path in public_paths or request.url.path.startswith("/.well-known/"):
        return await call_next(request)

    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        print("DEBUG: No Bearer token found in the request header.") # <--- DEBUG LOG
        return JSONResponse(status_code=401, content={"error": "Unauthorized. Bearer token missing."})

    token = auth_header.split(" ")[1]

    try:
        user_info_resp = requests.get(
            "https://www.googleapis.com/oauth2/v3/userinfo",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        if user_info_resp.status_code != 200:
            print(f"DEBUG: Google API rejected token. Status: {user_info_resp.status_code}, Response: {user_info_resp.text}") # <--- DEBUG LOG
            return JSONResponse(status_code=401, content={"error": "Invalid or expired Google token."})
            
        user_info = user_info_resp.json()
        user_email = user_info.get("email")

        # ==========================================
        # DEBUG LOGS: Check what email was extracted
        # ==========================================
        print(f"DEBUG: Successfully fetched token info.")
        print(f"DEBUG: Extracted Email -> '{user_email}'")
        print(f"DEBUG: Allowed Emails List -> {ALLOWED_EMAILS}")
        # ==========================================

        if not user_email or user_email not in ALLOWED_EMAILS:
            print(f"DEBUG: Access DENIED for email -> '{user_email}'") # <--- DEBUG LOG
            return JSONResponse(
                status_code=403, 
                content={"error": f"Access denied. Email '{user_email}' is not authorized to use this agent."}
            )
            
        print(f"DEBUG: Access GRANTED for email -> '{user_email}'") # <--- DEBUG LOG

    except Exception as e:
        print(f"DEBUG: Exception occurred during auth -> {str(e)}") # <--- DEBUG LOG
        return JSONResponse(status_code=500, content={"error": f"Authentication error: {str(e)}"})

    response = await call_next(request)
    return response