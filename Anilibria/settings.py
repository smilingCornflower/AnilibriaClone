from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

DEBUG = True

INTERNAL_HOST = os.getenv('INTERNAL_HOST')
PUBLIC_HOST = os.getenv('PUBLIC_HOST')

ALLOWED_HOSTS = [
    '127.0.0.1',
    'localhost',
    INTERNAL_HOST,
    PUBLIC_HOST,
]

frontend_origin = f"http://{PUBLIC_HOST}:5173"
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    frontend_origin,
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'corsheaders',

    'anime',
    'main',
    'users',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
]

ROOT_URLCONF = 'Anilibria.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'Anilibria.wsgi.application'

DATABASE = os.getenv('DATABASE')

if DATABASE == 'postgresql':
    db_username = os.getenv('DB_USERNAME')
    db_name = os.getenv('DB_NAME')
    db_password = os.getenv('DB_PASSWORD')
    db_host = os.getenv('INTERNAL_HOST')
    db_port = os.getenv('DB_PORT')

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': db_name,
            'USER': db_username,
            'PASSWORD': db_password,
            'HOST': db_host,
            'PORT': db_port,
        }
    }

else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

SESSION_COOKIE_AGE = 3600 * 2400  # 100 days
SESSION_EXPIRE_AT_BROWSER_CLOSE = False

SECRET_KEY = os.getenv("SECRET_KEY")

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

# todo: Один из этих двух не нужен, потом надо разобраться
EMAIL_HOST_USER = os.getenv('EMAIL')
EMAIL = os.getenv('EMAIL')
APP_PASSWORD = os.getenv('APP_PASSWORD')
# EMAIL_HOST_PASSWORD = os.getenv('APP_PASSWORD')
# SMTP_PASSWORD = secret.app_password

# AWS_ACCESS_KEY_ID = secret.aws_access_key_id
# AWS_SECRET_ACCESS_KEY = secret.aws_secret_access_key
# AWS_S3_REGION_NAME = secret.aws_region

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_S3_REGION_NAME = os.getenv('AWS_REGION')
AWS_STORAGE_BUCKET_NAME = os.getenv('BUCKET_NAME')
ENDPOINT_URL = os.getenv('ENDPOINT_URL')
SECRET_KEY = os.getenv('SECRET_KEY')

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {'min_length': 6}
    },
]

LANGUAGE_CODE = 'ru'
TIME_ZONE = 'Asia/Almaty'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'users.User'
LOGIN_URL = '/user/login/'
