import os
from pathlib import Path

from dotenv import load_dotenv
from split_settings.tools import include

load_dotenv()
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('SECRET_KEY')

DEBUG = os.environ.get('DEBUG', False) == 'True'

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

include(
    'components/installed_apps.py',
)

include(
    'components/middleware.py',
)

ROOT_URLCONF = 'config.urls'

include(
    'components/templates.py',
)

WSGI_APPLICATION = 'config.wsgi.application'

include(
    'components/database.py',
)

include(
    'components/auth_password_validators.py',
)

include(
    'components/internationalization.py',
)

include(
    'components/static.py',
)

include(
    'components/logging.py',
)

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

include(
    'components/corsheaders.py',
)

include(
    'components/debug_toolbar.py',
)
