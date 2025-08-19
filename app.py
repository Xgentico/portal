# app.py

from flask import Flask, render_template
from openai import OpenAI
from qdrant_client import QdrantClient
#from sqlalchemy import create_engine
from sqlalchemy import create_engine, text  # ✅ Add `text`

from config import (
    OPENAI_API_KEY, OPENAI_MODEL,
    SQLALCHEMY_DATABASE_URI,
    QDRANT_API_KEY, QDRANT_URL,
    FLASK_PORT
)

app = Flask(__name__)
client = OpenAI(api_key=OPENAI_API_KEY)

# Connect to Qdrant
qdrant = QdrantClient(
    url=QDRANT_URL,
    api_key=QDRANT_API_KEY
)

# Connect to PostgreSQL
engine = create_engine(SQLALCHEMY_DATABASE_URI)

@app.route("/")
def Index():
    # Simple connectivity check
    try:
        with engine.connect() as conn:
            #conn.execute("SELECT 1")
            conn.execute(text("SELECT 1"))  # ✅ Fixes the "not executable object" error
            db_status = "✅ Connected"
    except Exception as e:
        db_status = f"❌ Error: {str(e)}"

    try:
        client.models.list()
        openai_status = "✅ Connected"
    except Exception as e:
        openai_status = f"❌ Error: {str(e)}"

    try:
        qdrant.get_collections()
        qdrant_status = "✅ Connected"
    except Exception as e:
        qdrant_status = f"❌ Error: {str(e)}"

    return render_template("index.html", 
        db_status=db_status,
        openai_status=openai_status,
        qdrant_status=qdrant_status
    )

if __name__ == "__main__":
    app.run(debug=True, port=FLASK_PORT)
