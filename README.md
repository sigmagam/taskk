# TeraBox Standalone API

A self-contained Flask API that extracts direct download links from TeraBox
share URLs (including password-protected and folder shares). Extracted from the
larger Sonzai X API and packaged so it can run anywhere on its own.

## Features

- `GET /terabox?url=<TERABOX_URL>` — list files + direct download links.
- `GET /terabox?url=<TERABOX_URL>&pwd=<PASSWORD>` — password-protected shares.
- Auto session/jsToken scraping with cookie + endpoint failover.
- Recursive folder scan with configurable timeout.
- Local JSON session cache at `database/terabox_session.json`.

No API key required.

## Layout

```
terabox/
├── app.py                # Flask entrypoint
├── config.py             # env-driven config
├── utils.py              # JSON helpers
├── routes/
│   └── terabox.py        # core scraper + blueprint
├── database/             # auto-created (session cache)
├── requirements.txt
├── Procfile
├── .env.example
└── .gitignore
```

## Run locally

```bash
cd terabox
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env              # edit if needed
python app.py
```

Server starts on `http://0.0.0.0:5001` by default.

## Run with gunicorn (production)

```bash
gunicorn app:app -b 0.0.0.0:5001 -w 2 --timeout 120
```

The included `Procfile` works with Heroku/Railway/Render.

## Run with Docker

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
ENV PORT=5001
EXPOSE 5001
CMD ["gunicorn", "app:app", "-b", "0.0.0.0:5001", "-w", "2", "--timeout", "120"]
```

```bash
docker build -t terabox-api .
docker run -p 5001:5001 --env-file .env terabox-api
```

## API

### `GET /`
Service info + endpoint listing.

### `GET /terabox?url=<terabox_url>[&pwd=<password>]`

Example:

```bash
curl "http://localhost:5001/terabox?url=https://1024terabox.com/s/1HcZ4bbKShOS8o69NX7MXFg"
```

Response:

```json
{
  "author": "Sonzai X シ",
  "contact": "https://t.me/November2k",
  "status": "success",
  "source": "Terabox",
  "request_url": "...",
  "extracted_shorturl": "HcZ4bbKShOS8o69NX7MXFg",
  "is_private": false,
  "total_files": 1,
  "files": [
    {
      "filename": "video.mp4",
      "size": 12345678,
      "path": "/video.mp4",
      "thumbnail": "https://...",
      "download_link": "https://proxy.sonzaixlab.workers.dev/dl?url=...&cookie=..."
    }
  ],
  "debug": ["..."]
}
```

`download_link` is routed through a Cloudflare Worker (configurable via
`TERABOX_CORS_DOWNLOAD_BASE`) so the VPS bandwidth is not used for the actual
download.

## Configuration

All config is driven by environment variables (see `.env.example`):

| Variable | Default | Description |
| --- | --- | --- |
| `PORT` | `5001` | HTTP port |
| `HOST` | `0.0.0.0` | Bind host |
| `DEBUG` | `false` | Flask debug |
| `API_AUTHOR` | `Sonzai X シ` | Branding in response |
| `API_CONTACT` | `https://t.me/November2k` | Branding in response |
| `TERABOX_CORS_DOWNLOAD_BASE` | `https://proxy.sonzaixlab.workers.dev/dl` | Worker proxy base |
| `TERABOX_SCAN_TIMEOUT_SECONDS` | `25` | Soft timeout per share scan |

## Notes

- The session cache (`database/terabox_session.json`) holds a working `jsToken`
  and is auto-refreshed on failure. Safe to delete; it'll be regenerated.
- Built-in fallback cookies are used to bootstrap sessions. If TeraBox rotates
  them you can edit `routes/terabox.py` (`TERABOX_CONFIG`) to add fresh ones.
