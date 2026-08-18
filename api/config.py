"""Configuration for the TeraBox Flask API."""
import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
# Local development only; Vercel environment variables are injected by Vercel.
load_dotenv(BASE_DIR / ".env")

PORT = int(os.getenv("PORT", "5001"))
HOST = os.getenv("HOST", "0.0.0.0")
DEBUG = os.getenv("DEBUG", "false").lower() == "true"

CORS_HEADERS = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type",
}

API_AUTHOR = os.getenv("API_AUTHOR", "AccelPedia シ")
API_CONTACT = os.getenv("API_CONTACT", "https://t.me/November2k")

# Optional override. If empty, routes/terabox.py builds https://<current-host>/dl.
TERABOX_CORS_DOWNLOAD_BASE = os.getenv("TERABOX_CORS_DOWNLOAD_BASE", "").strip()

TERABOX_DOWNLOAD_TOKEN_TTL_SECONDS = 60 * 60
TERABOX_DOWNLOAD_LINK_BATCH_SIZE = 5
TERABOX_SCAN_TIMEOUT_SECONDS = int(os.getenv("TERABOX_SCAN_TIMEOUT_SECONDS", "25"))


# Alias used by the TeraBox route. Empty means the current request host + /dl.
CORS_DOWNLOAD_BASE = TERABOX_CORS_DOWNLOAD_BASE
