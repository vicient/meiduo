"""
Django settings for meiduo_mall project.

Generated by 'django-admin startproject' using Django 1.11.11.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""
import datetime
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 新增包搜索路径
import sys

sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'bxo*pt98w+jwm(ich*0+jl)36^17cdpgh#0xj3%2m35twsi*b!'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['api.meiduo.site']

# Application definition

INSTALLED_APPS = [
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	# 第三方库
	'rest_framework',
	'corsheaders',
	'ckeditor',  # 富文本编辑器
	'ckeditor_uploader',  # 富文本编辑器上传图片模块
	'django_crontab',
	'haystack',
	# 自定义apps
	'user.apps.UserConfig',
	'verifications.apps.VerificationsConfig',
	'oauth.apps.OauthConfig',
	'areas.apps.AreasConfig',
	'goods.apps.GoodsConfig',
	'content.apps.ContentConfig',
	'cart.apps.CartConfig',
	'orders.apps.OrdersConfig',
]

MIDDLEWARE = [
	'corsheaders.middleware.CorsMiddleware',
	'django.middleware.security.SecurityMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.common.CommonMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'meiduo_mall.urls'

TEMPLATES = [
	{
		'BACKEND': 'django.template.backends.django.DjangoTemplates',
		'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'meiduo_mall.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.mysql',
		'HOST': '127.0.0.1',  # 数据库主机
		'PORT': 3306,  # 数据库端口
		'USER': 'root',  # 数据库用户名
		'PASSWORD': 'w92z12x14',  # 数据库用户密码
		'NAME': 'meiduo_mall'  # 数据库名字
	}
}

# redis配置
CACHES = {
	# 默认
	"default": {
		"BACKEND": "django_redis.cache.RedisCache",
		"LOCATION": "redis://127.0.0.1:6379/0",
		"OPTIONS": {
			"CLIENT_CLASS": "django_redis.client.DefaultClient",
		}
	},
	# admin的session
	"session": {
		"BACKEND": "django_redis.cache.RedisCache",
		"LOCATION": "redis://127.0.0.1:6379/1",
		"OPTIONS": {
			"CLIENT_CLASS": "django_redis.client.DefaultClient",
		}
	},
	# 验证码相关
	"verify_codes": {
		"BACKEND": "django_redis.cache.RedisCache",
		"LOCATION": "redis://127.0.0.1:6379/2",
		"OPTIONS": {
			"CLIENT_CLASS": "django_redis.client.DefaultClient",
		}
	},
	"history": {
		"BACKEND": "django_redis.cache.RedisCache",
		"LOCATION": "redis://127.0.0.1:6379/3",
		"OPTIONS": {
			"CLIENT_CLASS": "django_redis.client.DefaultClient",
		}
	},
	"cart": {
		"BACKEND": "django_redis.cache.RedisCache",
		"LOCATION": "redis://127.0.0.1:6379/4",
		"OPTIONS": {
			"CLIENT_CLASS": "django_redis.client.DefaultClient",
		}
	},
}
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "session"

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

# LANGUAGE_CODE = 'en-us'
#
# TIME_ZONE = 'UTC'
LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'

# 日志配置
LOGGING = {
	'version': 1,
	'disable_existing_loggers': False,  # 是否禁用已经存在的日志器
	'formatters': {  # 日志信息显示的格式
		'verbose': {
			'format': '%(levelname)s %(asctime)s %(module)s %(lineno)d %(message)s'
		},
		'simple': {
			'format': '%(levelname)s %(module)s %(lineno)d %(message)s'
		},
	},
	'filters': {  # 对日志进行过滤
		'require_debug_true': {  # django在debug模式下才输出日志
			'()': 'django.utils.log.RequireDebugTrue',
		},
	},
	'handlers': {  # 日志处理方法
		'console': {  # 向终端中输出日志
			'level': 'DEBUG',
			'filters': ['require_debug_true'],
			'class': 'logging.StreamHandler',
			'formatter': 'simple'
		},
		'file': {  # 向文件中输出日志
			'level': 'INFO',
			'class': 'logging.handlers.RotatingFileHandler',
			'filename': os.path.join(os.path.dirname(BASE_DIR), "logs/meiduo.log"),  # 日志文件的位置
			'maxBytes': 300 * 1024 * 1024,
			'backupCount': 10,
			'formatter': 'verbose'
		},
	},
	'loggers': {  # 日志器
		'django': {  # 定义了一个名为django的日志器
			'handlers': ['console', 'file'],  # 可以同时向终端与文件中输出日志
			'propagate': True,  # 是否继续传递日志信息
			'level': 'DEBUG',  # 日志器接收的最低日志级别
		},
	}
}

# 异常处理
REST_FRAMEWORK = {
	'EXCEPTION_HANDLER': 'meiduo_mall.utils.exceptions.exception_handler',
	'DEFAULT_AUTHENTICATION_CLASSES': (
		'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
		'rest_framework.authentication.SessionAuthentication',
		'rest_framework.authentication.BasicAuthentication',
	),
	# 制定分页使用的累
	'DEFAULT_PAGINATION_CLASS': 'meiduo_mall.utils.pagination.StandardResultsSetPagination',
}

# JWT超时时间
JWT_AUTH = {
	'JWT_EXPIRATION_DELTA': datetime.timedelta(days=1),
	'JWT_RESPONSE_PAYLOAD_HANDLER': 'user.utils.jwt_response_payload_handler',
}

# 模型相关配置
AUTH_USER_MODEL = 'user.User'

# 跨域访问
CORS_ORIGIN_WHITELIST = (
	'127.0.0.1:8080',
	'localhost:8080',
	'www.meiduo.site:8080',
	'api.meiduo.site:8000'
)
CORS_ALLOW_CREDENTIALS = True  # 允许携带cookie

# QQ登录参数
QQ_CLIENT_ID = '101474184'  # appid
QQ_CLIENT_SECRET = 'c6ce949e04e12ecc909ae6a8b09b637c'  # appkey
QQ_REDIRECT_URI = 'http://www.meiduo.site:8080/oauth_callback.html'  # 登录成功后重定向的界面
QQ_STATE = '/'

# 邮箱设置
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.163.com'
EMAIL_PORT = 25
# 发送邮件的邮箱
EMAIL_HOST_USER = '15071176826@163.com'
# 在邮箱中设置的客户端授权密码
EMAIL_HOST_PASSWORD = 'wzx921214'
# 收件人看到的发件人
EMAIL_FROM = 'spirit<15071176826@163.com>'

# 常用数据的缓存,drf扩展累
REST_FRAMEWORK_EXTENSIONS = {
	# 缓存时间
	'DEFAULT_CACHE_RESPONSE_TIMEOUT': 60 * 60,
	# 缓存存储
	'DEFAULT_USE_CACHE': 'default',
}

# django文件存储
DEFAULT_FILE_STORAGE = 'meiduo_mall.utils.fastdfs.storage.FastDFSStorage'

# FastDFS
# FDFS_URL = 'http://image.meiduo.site:8888/'
FDFS_BASE_URL = 'http://image.meiduo.site:8888/'
FDFS_CLIENT_CONF = os.path.join(BASE_DIR, 'utils/fastdfs/client.conf')

# 富文本编辑器ckeditor配置
CKEDITOR_CONFIGS = {
	'default': {
		'toolbar': 'full',  # 工具条功能
		'height': 300,  # 编辑器高度
		# 'width': 300,  # 编辑器宽
	},
}
CKEDITOR_UPLOAD_PATH = ''  # 上传图片保存路径，使用了FastDFS，所以此处设为''

GENERATED_STATIC_HTML_FILES_DIR = os.path.join(os.path.dirname(os.path.dirname(BASE_DIR)), 'front_end_pc')

CRONJOBS = [
	# 每5分钟执行一次生成主页静态文件
	(
	'*/5 * * * *', 'contents.crons.generate_static_index_html', '>> /Users/delron/Desktop/meiduo_mall/logs/crontab.log')
]

CRONTAB_COMMAND_PREFIX = 'LANG_ALL=zh_cn.UTF-8'

# Haystack
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
        'URL': 'http://192.168.246.144:9200/',  # 此处为elasticsearch运行的服务器ip地址，端口号固定为9200
        'INDEX_NAME': 'meiduo',  # 指定elasticsearch建立的索引库的名称
    },
}

# 当添加、修改、删除数据时，自动生成索引
HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'