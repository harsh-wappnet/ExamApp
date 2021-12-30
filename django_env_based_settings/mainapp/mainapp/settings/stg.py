import os

region = os.getenv('REGION')
assert region
ENV = os.getenv('ENV')
assert ENV

DEBUG = True

SECRET_KEY = "to-be-take-using-ssm-only"

# all envs values have to be take from ssm
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': os.getenv('POSTGRES_DB'),
#         'USER': os.getenv('POSTGRES_USER'),
#         'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
#         'HOST': os.getenv('POSTGRES_HOST', '127.0.0.1'),
#         'PORT': os.getenv('POSTGRES_PORT', '54320'),
#         'TEST': {
#             'NAME': 'lmstestdatabase',
#         },
#     }
# }

# uri = f"postgresql://{DATABASES['default']['USER']}:{DATABASES['default']['PASSWORD']}@{DATABASES['default']['HOST']}:{DATABASES['default']['PORT']}/{DATABASES['default']['NAME']}"
# print(f'DATABASE CONNECTION: {uri}')
