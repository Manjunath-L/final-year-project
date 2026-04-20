# Deployment Guide

This project is best deployed as two services:

- Django API: `django-backend/concept_crafter`
- React frontend: `frontend`

The PostgreSQL database can stay where it is already deployed. Put its connection string in the Django service as `DATABASE_URL`.

## 1. Deploy Django API

Use Railway, Render, or another Python web service.

Service root:

```txt
django-backend/concept_crafter
```

Build command:

```bash
pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate
```

Start command:

```bash
gunicorn concept_crafter.wsgi --log-file -
```

Environment variables:

```env
SECRET_KEY=your-production-secret
DEBUG=False
DATABASE_URL=your-postgres-url
OPENROUTER_API_KEY=your-openrouter-key
AI_BASE_URL=https://openrouter.ai/api/v1/chat/completions
AI_MODEL=google/gemma-3-27b-it:free
ALLOWED_HOSTS=your-django-domain.onrender.com
CORS_ALLOWED_ORIGINS=https://your-frontend-domain.vercel.app
CSRF_TRUSTED_ORIGINS=https://your-frontend-domain.vercel.app
```

After the Django deploy finishes, test:

```txt
https://your-django-domain/api/templates/
```

It may return `401 Unauthorized` for protected endpoints. That is okay. It means the API is reachable.

## 2. Deploy React Frontend

Use Vercel, Netlify, or another static frontend host.

Project root:

```txt
frontend
```

Build command:

```bash
npm run build
```

Output directory:

```txt
dist/public
```

Environment variables:

```env
VITE_API_URL=https://your-django-domain
```

Do not include a trailing slash in `VITE_API_URL`.

## 3. Update CORS After Frontend Deploy

After the frontend gets its real URL, go back to the Django service and set:

```env
CORS_ALLOWED_ORIGINS=https://your-real-frontend-domain
CSRF_TRUSTED_ORIGINS=https://your-real-frontend-domain
```

Then redeploy/restart Django.

## 4. Local Development

Django:

```bash
cd django-backend/concept_crafter
python manage.py runserver
```

React:

```bash
cd frontend
npm run dev
```

Locally, Vite proxies `/api` to `http://localhost:8000`.
