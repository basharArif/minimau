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

For production, ensure `DJANGO_SETTINGS_MODULE` is set to `sitecore.settings.prod`.

## Testing

Run `pytest` to execute tests.
