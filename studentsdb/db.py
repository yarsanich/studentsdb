import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

#DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, '..', 'db.sqlite3'),
#     }

DATABASES = {
    'default': {
    'ENGINE': 'django.db.backends.mysql',
    'HOST': 'localhost',
    'USER': 'root',
    'PASSWORD': '23790564',
    'NAME': 'students_db',
	}
	}
