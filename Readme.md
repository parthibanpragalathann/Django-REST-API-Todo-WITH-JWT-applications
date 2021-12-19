# TODO with JWT using DRF & PostgresQL
Django-RestFramework-TODO-APPS-WITH-JSON-WEB-TOKEN-AUTHENTICATION Applications.

## Install package for TO-DO Apps
Installed packages are django, djangorestframework, simplejwt, psycopg2, psycopg2-binary.

###Django
Django is a high-level Python web framework that enables rapid development of secure and maintainable websites.

###Django Rest Framework
Django REST framework is a powerful and flexible toolkit for building Web APIs.

###Psycopg2 & Psycopg2-binary  
Psycopg is the most popular PostgreSQL adapter for the Python programming language. 
At its core it fully implements the Python DB API 2.0

psycopg2 contains the sources to recompile the library,  
psycopg2-binary contains an already compiled wheel-package with binary

###wheel package
A built-package format for Python.  
A wheel is a ZIP-format archive with a specially formatted filename and the dot . whl extension.

###Pillow
The Python Imaging Library adds image processing capabilities to our Python interpreter.

###simpleJWT
Simple JWT provides a JSON Web Token authentication backend for the Django REST Framework.

###Token authentication
Token-based authentication is a protocol which allows users to verify their identity, and in return receive a unique access token.

```bash
pip install django djangorestframework psycopg2 psycopg2-binary pillow djangorestframework-simplejwt
```
## Check installed package
```bash
pip freeze
```
## Result of Usage 

```bash
asgiref==3.4.1
Django==4.0
djangorestframework==3.13.1
djangorestframework-simplejwt==5.0.0
Pillow==8.4.0
psycopg2==2.9.2
psycopg2-binary==2.9.2
PyJWT==2.3.0
pytz==2021.3
sqlparse==0.4.2
tzdata==2021.5
```
##Create Django project and applications
```bash
PS F:\AdityaChola_Projects\TODO_JWT_DRF> django-admin startproject Project .
PS F:\AdityaChola_Projects\TODO_JWT_DRF> django-admin startapp App

Result list of source code Files Directory
    Directory: F:\AdityaChola_Projects\TODO_JWT_DRF

Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
d-----        17-12-2021     21:01                .idea
d-----        17-12-2021     21:03                App
d-----        17-12-2021     21:02                Project
-a----        17-12-2021     21:02            685 manage.py
```

###project 
```bash
Result list of project source code Files Directory

    Directory: F:\AdityaChola_Projects\TODO_JWT_DRF\Project

Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
-a----        17-12-2021     21:02            407 asgi.py
-a----        17-12-2021     21:02           3345 settings.py
-a----        17-12-2021     21:02            770 urls.py
-a----        17-12-2021     21:02            407 wsgi.py
-a----        17-12-2021     21:02              0 __init__.py
```

###application 
```bash
Result list of application source code Files Directory

    Directory: F:\AdityaChola_Projects\TODO_JWT_DRF\App

Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
d-----        17-12-2021     21:45                migrations
d-----        18-12-2021     00:57                __pycache__
-a----        17-12-2021     21:03             66 admin.py
-a----        17-12-2021     21:03            144 apps.py
-a----        17-12-2021     21:18           1358 manager.py
-a----        17-12-2021     21:16           1299 models.py
-a----        18-12-2021     00:33            218 pagination.py
-a----        17-12-2021     21:20           4297 serializer.py
-a----        17-12-2021     21:03             63 tests.py
-a----        18-12-2021     00:56           1526 urls.py
-a----        18-12-2021     00:12           7813 views.py
-a----        17-12-2021     21:03              0 __init__.py
```

## setup and DB configuration  settings.py file project Directory
```python
import os
from datetime import timedelta
from pathlib import Path
Installed_apps=[
    'App',                     # api is a local application
    'rest_framework',          # for django REST framework is a powerful and flexible toolkit for building Web APIs
    'rest_framework_simplejwt.token_blacklist',
]

AUTH_USER_MODEL = 'app.CustomUser'
#using postgresql
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'db',
        'USER': 'parthi',
        'PASSWORD': 'parthi*619',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',        # permissions Allow for register and login.
        'rest_framework.permissions.IsAuthenticated', # permissions checked at the start to end of all view.
    ),

    'DEFAULT_PARSER_CLASSES': (  # parsers used when accessing the request.data property
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
    ),
}

#DOUBT
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(weeks=521),  # 10 years
    "REFRESH_TOKEN_LIFETIME": timedelta(weeks=521),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "VERIFYING_KEY": None,
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
}

#create media directory in the project root directory 
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

```
##python manage.py makemigrations

##python manage.py migrate

##python manage.py runserver
