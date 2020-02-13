# coding:utf8
"""
Django settings for skstack project.


For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
import  configparser as ConfigParser





# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


if os.path.exists(BASE_DIR+'/skstack_dev.conf'):
    CONFIGFILE = os.path.join(BASE_DIR, 'skstack_dev.conf')
else:
    CONFIGFILE = os.path.join(BASE_DIR, 'skstack_prod.conf')

config = ConfigParser.ConfigParser()
config.read(CONFIGFILE)




# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'n@s)3&f$tu#-^^%k-dj__th2)7m!m*(ag!fs=6ezyzb7l%@i@9'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config.get('setup', 'debug')

# DEBUG = True if config.get('setup', 'debug') == 'True' else False
ALLOWED_HOSTS = config.get('setup', 'allowed_hosts').split(',')




SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# Application definition

INSTALLED_APPS = [
    'skrpt',
#     'sktask',
#     'skcmdb',
#     'skrecord',
#     'skyw',
    'skconfig',
    'skaccounts',
    'skworkorders',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_celery_results',
#     'channels',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
#     'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.common.BrokenLinkEmailsMiddleware',

]

ROOT_URLCONF = 'skstack.urls'


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
                'skstack.context_processor.url_permission',
            ],
        },
    },
]

WSGI_APPLICATION = 'skstack.wsgi.application'


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
            'OPTIONS': {
              "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",                                                              
          }
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


DATABASE_ROUTERS = ['skstack.utils.DatabaseAppsRouter']
DATABASE_APPS_MAPPING = {
    'skjumpserver': 'jumpserver_db',
}


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



LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False

STATIC_URL = '/static/'
# STATIC_ROOT = BASE_DIR + '\\static\\'
#for windows py37
STATIC_ROOT = ''
STATICFILES_DIRS = ( os.path.join('static'), )

#for windows py37_64 debug mode
# STATIC_ROOT = os.path.join(BASE_DIR, '/static/')
# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR, 'static')
# ]
#print("STATIC_ROOT: %s" % STATIC_ROOT)
# STATICFILES_DIRS = (
#     os.path.join(BASE_DIR, './static/').replace('\\', '/'),
# #     os.path.join(BASE_DIR, '/static/'),
#   
# )
# print("this STATICFILES_DIRS: %s" % STATICFILES_DIRS)

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_IMAGE_BACKEND = "pillow"
CKEDITOR_RESTRICT_BY_USER = False
CKEDITOR_CONFIGS = {
    # 配置名是default时，django-ckeditor默认使用这个配置
    'default': {
        # 使用简体中文
        'language':'zh-cn',
        # 编辑器的宽高请根据你的页面自行设置
        'width':'530px',
        'height':'150px',
        'image_previewText':' ',
        'tabSpaces': 4,
        'toolbar': 'Custom',
        # 添加按钮在这里
        'toolbar_Custom': [
            ['Bold', 'Italic', 'Underline', 'Format', 'RemoveFormat'],
            ['NumberedList', 'BulletedList'],
            ['Blockquote', 'CodeSnippet'],
            ['Image', 'Link', 'Unlink'],
            ['Maximize']
        ],
        # 插件
        'extraPlugins': ','.join(['codesnippet','uploadimage','widget','lineutils',]),
    }
}
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

#celery config

CELERY_BROKER_URL = 'redis://:redis0619@localhost:6379/0'
CELERY_RESULT_BACKEND = 'django-db'
CELERY_TIMEZONE = 'Asia/Shanghai'
CELERY_TASK_RESULT_EXPIRES = 99999


log_path = config.get('log', 'log_path')
   
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
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
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'null': {
            'level':'DEBUG',
            'class':'logging.NullHandler',
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'filters': ['require_debug_false'],  #  DEBUG = False sendemail
            'include_html':True,
            'formatter': 'standard',
        },
        'default': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(log_path,'skstack.log'),  
            'maxBytes': 1024 * 1024 * 5,  
            'backupCount': 5,  
            'formatter': 'standard',  
        },

     
        'console': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
         'skworkorders_log': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(log_path,'skworkorders.log'),
            'formatter': 'standard'
        },
            
          
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['console', 'default'],
            'level': 'INFO',
            'propagate': False,
        },
        'skstack': {
            'handlers': ['console', 'default'],
            'level': 'INFO',
            'propagate': False,
        },
         'skworkorders': {
            'handlers': ['skworkorders_log','console'],
            'level': 'INFO',
            'propagate': False,
        },
    }
}

# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = config.get('email', 'email_host')
# EMAIL_PORT = config.get('email', 'email_port')
# EMAIL_HOST_USER = config.get('email', 'email_user')
# EMAIL_HOST_PASSWORD = config.get('email', 'email_password')
# EMAIL_SUBJECT_PREFIX = 'skstack' #为邮件标题的前缀,默认是'[django]'
# DEFAULT_FROM_EMAIL = SERVER_EMAIL = EMAIL_HOST_USER #设置发件人
# 
# ADMINS = (
# 
# ('encodingl','encodingl@sina.com'),
# 
# )
# MANAGERS = ADMINS
# SEND_BROKEN_LINK_EMAILS = True

# CRONJOBS = [
#     ('*/10 * * * *', 'skrecord.cron','>>/var/log/skrecord_cron.log')
# ]

#for channels websockets
# ASGI_APPLICATION = 'skstack.routing.application'
# RedisHost = config.get('redis', 'host')
# RedisPort = config.get('redis', 'port')
# CHANNEL_LAYERS = {
#     "default": {
#         "BACKEND": "channels_redis.core.RedisChannelLayer",
#         "CONFIG": {
#             "hosts": [(RedisHost, RedisPort)],
#         },
#  
#     },
# }

