# coding:utf8
"""
Django settings for skipper project.

Generated by 'django-admin startproject' using Django 1.9.8.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os
import ConfigParser

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if os.path.exists(BASE_DIR+'/skipper_dev.conf'):
    CONFIGFILE = os.path.join(BASE_DIR, 'skipper_dev.conf')
else:
    CONFIGFILE = os.path.join(BASE_DIR, 'skipper.conf')

config = ConfigParser.ConfigParser()
config.read(CONFIGFILE)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'n@s)3&f$tu#-^^%k-dj__th2)7m!m*(ag!fs=6ezyzb7l%@i@9'

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = config.get('setup', 'debug')

DEBUG = True if config.get('setup', 'debug') == 'True' else False
ALLOWED_HOSTS = config.get('setup', 'allowed_hosts').split(',')

ADMINS = (
    ('yehaiquan', 'haiquan.ye@mljr.com'),
)
MANAGERS = ADMINS

SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# Application definition

INSTALLED_APPS = [
    'sktask',
    'skdomain',
    'skcmdb',
    'skconfig',
    'skaccounts',
    'skapi',
    'skrpt',
    'skdeploy',
    'skyw',
    'skrecord',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'skipper.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'skipper.context_processor.url_permission',
            ],
        },
    },
]

WSGI_APPLICATION = 'skipper.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }


DATABASES = {}
if config.get('db', 'engine') == 'mysql':
    DB_HOST = config.get('db', 'host')
    DB_PORT = config.getint('db', 'port')
    DB_USER = config.get('db', 'user')
    DB_PASSWORD = config.get('db', 'password')
    DB_DATABASE = config.get('db', 'database')
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': DB_DATABASE,
            'USER': DB_USER,
            'PASSWORD': DB_PASSWORD,
            'HOST': DB_HOST,
            'PORT': DB_PORT,
        }
    }
elif config.get('db', 'engine') == 'sqlite':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': config.get('db', 'database'),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }

# DATABASES['jumpserver_db'] = {
#     'ENGINE': 'django.db.backends.mysql',
#     'NAME': config.get('jumpserver_db', 'database'),
#     'USER': config.get('jumpserver_db', 'user'),
#     'PASSWORD': config.get('jumpserver_db', 'password'),
#     'HOST': config.get('jumpserver_db', 'host'),
#     'PORT': config.getint('jumpserver_db', 'port'),
# }

DATABASE_ROUTERS = ['skipper.utils.DatabaseAppsRouter']
DATABASE_APPS_MAPPING = {
    'skjumpserver': 'jumpserver_db',
}

# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False

STATIC_ROOT = BASE_DIR + '/static'
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static').replace('\\', '/'),
)
'''
REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ]
}
'''
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    )
}

AUTH_USER_MODEL = 'skaccounts.UserInfo'
LOGIN_URL = '/skaccounts/login/'

# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'handlers': {
#         'console': {
#             'class': 'logging.StreamHandler',
#         },
#     },
#     'loggers': {
#         'django.db.backends': {
#             'handlers': ['console'],
#             'level': 'INFO' if DEBUG else 'INFO',
#         },
#     },
# }

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
    },
    'formatters': {
        'standard': {
            'format': '%(asctime)s|%(levelname)s|%(process)d|%(funcName)s|%(lineno)d|msg:%(message)s'
        },
    },
    'handlers': {
        'mail_admins': {
            'level': 'INFO',
            'class': 'django.utils.log.AdminEmailHandler',
            'filters': ['require_debug_false'],  # 仅当 DEBUG = False 时才发送邮件
            # 'include_html':True,
            'formatter': 'standard',
        },
        'default': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/opt/data/logs/skipper/skipper.log',  # 日志输出文件
            'maxBytes': 1024 * 1024 * 5,  # 文件大小
            'backupCount': 5,  # 备份份数
            'formatter': 'standard',  # 使用哪种formatters日志格式
        },
        'error_file': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/opt/data/logs/skipper/skipper-error.log',
            'formatter': 'standard'
        },
        'info_file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/opt/data/logs/skipper/skipper-info.log',
            'formatter': 'standard'
        },
        'debug': {  # 记录到日志文件(需要创建对应的目录，否则会出错)
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/opt/data/logs/skipper/skipper-debug.log',  # 日志输出文件
            'maxBytes': 1024 * 1024 * 5,  # 文件大小
            'backupCount': 5,  # 备份份数
            'formatter': 'standard',  # 使用哪种formatters日志格式
        },
        'zabbix_file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/opt/data/logs/skipper/skipper-zabbix.log',
            'formatter': 'standard'
        },
        'api_file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/opt/data/logs/skipper/skipper-api.log',
            'formatter': 'standard'
        },
        'nginx_info': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/opt/data/logs/skipper/nginx_req_info.log',
            'formatter': 'standard'
        },
        'console': {
            'level': 'DEBUG',
            'filters': ['require_debug_false'],
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        },
        # 对于不在 ALLOWED_HOSTS 中的请求不发送报错邮件
        # 'django.security.DisallowedHost': {
        #     'handlers': ['null'],
        #     'propagate': False,
        # },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'info_file'],
            'level': 'INFO',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['console', 'info_file'],
            'level': 'ERROR',
            'propagate': False,
        },
        'skipper': {
            'handlers': ['console', 'info_file'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'zabbix': {
            'handlers': ['zabbix_file'],
            'level': 'INFO',
            'propagate': False,
        },
        'api': {
            'handlers': ['api_file'],
            'level': 'INFO',
            'propagate': False,
        },
        'nginx_info': {
            'handlers': ['nginx_info'],
            'level': 'INFO',
            'propagate': False,
        },
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = config.get('email', 'email_host')
EMAIL_PORT = config.get('email', 'email_port')
EMAIL_HOST_USER = config.get('email', 'email_user')
EMAIL_HOST_PASSWORD = config.get('email', 'email_password')
