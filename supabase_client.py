import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_KEY")

if not url or not key:
    raise RuntimeError(
        "Faltan SUPABASE_URL o SUPABASE_KEY. Copia .env.example a .env y completa "
        "con las credenciales del proyecto 'practica6' ya existente en Supabase."
    )

supabase: Client = create_client(url, key)
