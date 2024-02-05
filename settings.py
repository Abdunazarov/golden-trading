# stdlib
import os

# thirdparty
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.environ["DATABASE_URL"]
EMAIL_PATTERN = (
    r"^[a-z0-9!#$%&'*+\/=?^_‘{|}~-]+"
    r"(?:\.[a-z0-9!#$%&'*+\/=?^_‘{|}~-]+)*@"
    r"(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+"
    r"[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$"
)