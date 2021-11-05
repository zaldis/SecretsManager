import string
import dotenv
import os
import pathlib


dotenv.load_dotenv()


ALPHABET = os.environ.get(
    'ALPHABET',
    string.ascii_letters + string.digits + string.punctuation
)
PASSWORD_SIZE = int(os.environ.get('SIZE', '30'))
SECRET_KEY = os.environ.get('SECRET_KEY')
CLIP_MODULE = os.environ.get('CLIP')
CURRENT_DIR = pathlib.Path(os.path.dirname(__file__))
