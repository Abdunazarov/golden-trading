# stdlib
import os
from datetime import timedelta

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
ACCESS_TOKEN_EXPIRY = ACCESS_TOKEN_EXPIRY = timedelta(
    minutes=int(os.environ["ACCESS_TOKEN_EXPIRY"])
)
REFRESH_TOKEN_EXPIRY = timedelta(days=int(os.environ["REFRESH_TOKEN_EXPIRY"]))
JWT_SECRET = os.environ["REFRESH_TOKEN_EXPIRY"]
