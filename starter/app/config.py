import os
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")

PAPERS_DIR = ROOT / "docs" / "papers"
UPLOADS_DIR = ROOT / "data" / "docs"
INDEX_DIR = ROOT / "data" / "index"

MODEL = os.getenv("MODEL", "gpt-5.4-mini-2026-03-17")
EMBEDDING_MODEL = "text-embedding-3-small"

CHUNK_SIZE = 400
CHUNK_OVERLAP = 0
TOP_K = 3
