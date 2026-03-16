# owui-semwebfetch  
*Open WebUI semantic web fetch – a tiny FastAPI service + Open‑WebUI‑compatible tool*

---

## Quick Start

> **Prerequisites** – Docker (≥ 20.10) and a running Browserless instance.  
> Browserless must be reachable at `http://browserless:3000` (default) or the URL you’ll pass via `BROWSERLESS_API_URL`.

### 1. Build & run the service

```bash
git clone https://github.com/ekelhala/owui-semwebfetch.git
cd owui-semwebfetch
docker build -t owui-semwebfetch .
docker run -d \
  --name semwebfetch \
  --network host -p 8000:8000 \
  -e BROWSERLESS_API_URL=http://browserless:3000/content \
  owui-semwebfetch
```

The service will expose `http://localhost:8000/semantic-search`.

### 2. Test with `cURL`

```bash
curl -X POST http://localhost:8000/semantic-search \
     -H "Content-Type: application/json" \
     -d '{
           "urls": ["https://en.wikipedia.org/wiki/Natural_language_processing"],
           "search_query": "transformers in NLP",
           "top_k": 5,
           "chunk_size": 800,
           "overlap": 150,
           "min_score": 0.25
         }'
```

You should see a Markdown‑formatted answer with the best matches.

> The `Tools` class pulls its configuration from **Open‑WebUI valves** – you can edit the sidecar URL, chunk size, overlap, and minimum score in the UI.

---

## Project Layout

```
owui-semwebfetch/
├─ web_fetch/          # FastAPI service
│  ├─ __init__.py
│  ├─ constants.py
│  ├─ fetcher.py
│  ├─ cleaner.py
│  ├─ chunker.py
│  ├─ semantic.py
│  ├─ app.py
│  ├─ main.py
│  ├─ requirements.txt
│  └─ Dockerfile
└─ tool/              # Open‑WebUI tool
   ├─ __init__.py
   └─ tool.py
```

---

## API

```
POST /semantic-search
Content-Type: application/json

Request body
{
  "urls":          [<URL> | "<URL>"],
  "search_query":  "<text>",
  "top_k":         <int, default 3>,
  "chunk_size":    <int, default 800>,
  "overlap":       <int, default 150>,
  "min_score":     <float, default 0.25>
}
```

*The endpoint returns plain Markdown; no JSON wrapper.*

---

## Configuration

| Source | Variable | Description |
|--------|-----------|-------------|
| **Open‑WebUI valves** | `base_url` | Sidecar service endpoint (`http://sidecar:8000` by default) |
| | `chunk_size` | Characters per chunk |
| | `overlap` | Overlap between chunks |
| | `min_score` | Minimum cosine‑similarity threshold |
| **Environment** | `BROWSERLESS_API_URL` | URL of the Browserless instance (default `http://browserless:3000/content`) |

---

## Documentation

| File | Purpose |
|------|----------|
| `README.md` | Quick‑start guide (this file) |
| `semantic_search_service/Dockerfile` | Docker image for the sidecar |
| `SemanticSearchClient/tools.py` | Open‑WebUI‑compatible tool |
| `semantic_search_service/app.py` | FastAPI app (exposes `/semantic-search`) |
| `semantic_search_service/semantic.py` | Semantic ranking logic |

---

## Contributing

Pull‑requests are welcome.  
Feel free to add:

- Additional chunking strategies  
- New embeddings models  
- Extra Open‑WebUI valve types

Please run the included tests (if any) before submitting.

---

Happy fetching!  
