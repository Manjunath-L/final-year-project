SECRET_KEY = "django-insecure-&)lc3g\*%+aa$yh#08b0=3_qg8q3jff$2prbg+im4qd8a0t2y(b"

cd django-backend/concept_crafter
pip install -r requirements.txt

# Set up your .env file (copy from .env.example)

python manage.py migrate
python manage.py seed_templates
python manage.py runserver

set VITE_API_TARGET=http://localhost:8000 && npm run dev
