import os

from dotenv import load_dotenv
load_dotenv()


app_stage = os.environ.get('ENV')
assert app_stage

from .base import *

print(BASE_DIR)

print(f'app stage environment = {app_stage}')

if app_stage == 'STG':
    from .stg import *
else :
    from .local import *