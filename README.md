# Sitecore

Django conversion of static Minimau site.

## Setup

```bash
pip install -r requirements.txt
cp .env.dev .env
python manage.py migrate
python manage.py runserver
```

Use `.env.prod` for production environment variables.

## Testing

Run `pytest` to execute tests.
