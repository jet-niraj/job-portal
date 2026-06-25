# Job Portal

Full-stack job posting and management app — Vue.js + Django + PostgreSQL.

---

## Tech Stack
- **Frontend:** Vue.js 3, Chart.js, Axios
- **Backend:** Django, Django REST Framework
- **Database:** PostgreSQL

---

## Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Create `.env` in `backend/`:
```env
SECRET_KEY=django-insecure-your-secret-key
DEBUG=True
DB_NAME=job_portal_db
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
```

```bash
python manage.py migrate
python manage.py runserver       # http://localhost:8000
```

---

## Frontend Setup

```bash
cd frontend
npm install
npm run dev                      # http://localhost:5173
```

---

## CORS (Required)

```bash
pip install django-cors-headers
```

```python
# settings.py
INSTALLED_APPS += ['corsheaders']
MIDDLEWARE = ['corsheaders.middleware.CorsMiddleware', ...]
CORS_ALLOWED_ORIGINS = ['http://localhost:5173']
```

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/jobs/` | List jobs |
| POST | `/api/jobs/` | Create job |
| PATCH | `/api/jobs/:id/` | Update job |
| DELETE | `/api/jobs/:id/` | Delete job |
| POST | `/api/jobs/:id/duplicate/` | Duplicate job |
| GET | `/api/jobs/analytics/` | Analytics data |