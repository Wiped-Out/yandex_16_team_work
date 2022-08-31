import os

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')  # type: ignore # noqa: F821
