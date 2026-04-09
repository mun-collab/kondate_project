import os  # osインポートを追加
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# --- セキュリティ設定 ---
# Renderの設定画面で登録する環境変数を読み込むようにします
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-j9kj(@cfgo66(t$ze%bew3q3*#b(el(5g!xb1jg2_yo3!$=4_*')

# Render上ではDEBUGをFalseにし、ローカル開発時のみTrueになるようにします
DEBUG = os.environ.get('DEBUG', 'True') == 'True'

# 全てのホストを許可（RenderのURLが決まったら、後で特定のURLに絞るのが理想です）
ALLOWED_HOSTS = ['*']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'roulette',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # 【追加】静的ファイル配信用のライブラリ
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'kondate_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'kondate_project.wsgi.application'

# Database (SQLiteを使用。Renderの無料プランでは再起動でデータが消える点に注意)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]

# Internationalization
LANGUAGE_CODE = 'ja'
TIME_ZONE = 'Asia/Tokyo'
USE_I18N = True
USE_TZ = True

# --- 静的ファイルの設定 ---
STATIC_URL = 'static/'
# 本番環境でCSSなどを集約する場所を指定します
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
# WhiteNoiseの設定
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'