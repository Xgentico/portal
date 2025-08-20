# config.py
import os
from dotenv import load_dotenv
from pathlib import Path

# Load .env in development (Render uses dashboard env vars)
base_dir = Path(__file__).parent
env_path = base_dir / ".env"
if env_path.exists():
    load_dotenv(env_path)

# OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL   = os.getenv("OPENAI_MODEL", "gpt-4o-mini")  # deterministic default

# PostgreSQL (Render: set these in the service env)
POSTGRES_DB       = os.getenv("POSTGRES_DB")
POSTGRES_USER     = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_HOST     = os.getenv("POSTGRES_HOST")
POSTGRES_PORT     = os.getenv("POSTGRES_PORT", "5432")
DB_SSLMODE        = os.getenv("DB_SSLMODE", "require")  # Render-friendly

# SQLAlchemy DSN (psycopg2 driver explicit)
SQLALCHEMY_DATABASE_URI = (
     f"postgresql+psycopg://{POSTGRES_USER}:{POSTGRES_PASSWORD}"
     f"@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
     f"?sslmode={DB_SSLMODE}"
 )

# Qdrant
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
QDRANT_URL     = os.getenv("QDRANT_URL")  # e.g. https://xxxx.cloud.qdrant.io

# Flask
# Render injects $PORT for Gunicorn; this is only for local runs
FLASK_PORT = int(os.getenv("FLASK_PORT", "10000"))

# Optional sanity checks (fail fast in prod if misconfigured)
REQUIRED_VARS = [
    ("OPENAI_API_KEY", OPENAI_API_KEY),
    ("POSTGRES_DB", POSTGRES_DB),
    ("POSTGRES_USER", POSTGRES_USER),
    ("POSTGRES_PASSWORD", POSTGRES_PASSWORD),
    ("POSTGRES_HOST", POSTGRES_HOST),
    ("QDRANT_API_KEY", QDRANT_API_KEY),
    ("QDRANT_URL", QDRANT_URL),
]
missing = [k for k, v in REQUIRED_VARS if not v]
if missing and not env_path.exists():
    # In Render (no .env), raise to surface misconfig during boot
    raise RuntimeError(f"Missing required env vars: {', '.join(missing)}")
