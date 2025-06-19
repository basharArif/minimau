from .base import *  # noqa: F401,F403,F405

env.read_env(BASE_DIR / '.env.prod')  # noqa: F405

DEBUG = False

MIDDLEWARE = (  # noqa: F405
    MIDDLEWARE[:1]  # noqa: F405
    + ['whitenoise.middleware.WhiteNoiseMiddleware']
    + MIDDLEWARE[1:]  # noqa: F405  # noqa: F405
)  # noqa: F405

SECURE_SSL_REDIRECT = True
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_PRELOAD = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = True

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
