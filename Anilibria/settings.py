from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# Project
DEBUG = os.getenv('DEBUG') == "True"
SECRET_KEY = os.getenv("SECRET_KEY")

# Email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
APP_PASSWORD = os.getenv('APP_PASSWORD')

# todo: Один из этих двух не нужен, потом надо разобраться
EMAIL_HOST_USER = os.getenv('EMAIL')
EMAIL = os.getenv('EMAIL')


# Databse
DATABASE = os.getenv('DATABASE')
DB_USERNAME = os.getenv('DB_USERNAME')
DB_NAME = os.getenv('DB_NAME')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_PORT = os.getenv('DB_PORT')

# WEB
INTERNAL_HOST = os.getenv('INTERNAL_HOST')
PUBLIC_HOST = os.getenv('PUBLIC_HOST')
FRONTEND_PORT = os.getenv('FRONTEND_PORT')

# AWS
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_S3_REGION_NAME = os.getenv('AWS_REGION')
AWS_STORAGE_BUCKET_NAME = os.getenv('BUCKET_NAME')
ENDPOINT_URL = os.getenv('ENDPOINT_URL')

ALLOWED_HOSTS = [
    '127.0.0.1',
    'localhost',
    INTERNAL_HOST,
    PUBLIC_HOST,
]

PUBLIC_ORIGIN = f"http://{PUBLIC_HOST}:{FRONTEND_PORT}"
INTERNAL_ORIGIN = f"http://{INTERNAL_HOST}:{FRONTEND_PORT}"

CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    PUBLIC_ORIGIN,
    INTERNAL_ORIGIN,
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


if DATABASE == 'postgresql':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': DB_NAME,
            'USER': DB_USERNAME,
            'PASSWORD': DB_PASSWORD,
            'HOST': 'localhost',
            'PORT': DB_PORT,
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
