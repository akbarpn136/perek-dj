from perek.core_settings import *

SECRET_KEY = 'j#8@93ujklh+t_k8m^(lccm+^o9heq(^n1)j+f)2%(9u56s@we_perek'
DEBUG = True
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]
