# 🎓 StudyMate — AI-Powered Learning Assistant

A ChatGPT-like web app that recommends ranked YouTube learning videos using Gemini AI + YouTube Data API v3.

---

## 🏗️ Architecture

```
User → Django (UI) → FastAPI (AI + YouTube + Ranking) → YouTube API
                            ↓
                       Gemini API (query refinement)
```

---

## ⚙️ Setup

### 1. Clone / extract the project

```bash
cd studyMate
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate        # Linux/Mac
venv\Scripts\activate           # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Edit `.env` and fill in your API keys:

```env
GEMINI_API_KEY=your_gemini_api_key_here
YOUTUBE_API_KEY=your_youtube_api_key_here
FASTAPI_BASE_URL=http://127.0.0.1:8001
DJANGO_SECRET_KEY=your-secret-key
```

**Get API Keys:**
- **Gemini API Key** → https://aistudio.google.com/app/apikey
- **YouTube Data API v3** → https://console.developers.google.com/ (enable "YouTube Data API v3")

---

## 🚀 Running the App

You need **two terminals** running simultaneously.

### Terminal 1 — Start FastAPI backend

```bash
cd fastapi_app
uvicorn main:app --host 0.0.0.0 --port 8001 --reload
```

### Terminal 2 — Start Django frontend

```bash
# from project root (studyMate/)
python manage.py runserver 8000
```

### Open in browser

```
http://127.0.0.1:8000
```

---

## 📁 Project Structure

```
studyMate/
├── manage.py
├── requirements.txt
├── .env                          ← API keys go here
│
├── studymate_project/            ← Django project config
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── django_app/                   ← Django frontend app
│   ├── views.py                  ← Proxies requests to FastAPI
│   ├── urls.py
│   └── templates/
│       └── django_app/
│           └── index.html        ← Chatbot UI
│
└── fastapi_app/                  ← FastAPI backend service
    ├── main.py                   ← /recommend endpoint
    ├── services/
    │   ├── gemini_service.py     ← Query refinement via Gemini
    │   └── youtube_service.py    ← YouTube Data API v3
    └── utils/
        └── ranking.py            ← Scoring algorithm
```

---

## 🔄 API Flow

1. User types topic → Django view calls `GET /recommend?topic=...` on FastAPI
2. FastAPI refines query with Gemini API
3. Fetches 10 videos from YouTube search API
4. Fetches view/like counts from YouTube videos API
5. Ranks by: `relevance×0.4 + views×0.2 + likes×0.2 + title_match×0.1 + recency×0.1`
6. Returns top 5 ranked videos with reasons
7. Django renders video cards in chatbot UI

---

## 🔌 FastAPI Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/recommend?topic=...` | Get ranked YouTube videos |
| GET | `/health` | Health check |

Test directly:
```
http://127.0.0.1:8001/recommend?topic=python+for+beginners
http://127.0.0.1:8001/docs   ← Swagger UI
```

---

## 💡 Notes

- If `GEMINI_API_KEY` is not set, the raw user query is used directly (graceful fallback)
- Results are not cached — each query hits the YouTube API fresh
- YouTube API has a daily quota of 10,000 units; each search costs ~100 units
