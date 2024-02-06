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
SMTP_SERVER = os.environ["SMTP_SERVER"]
SMTP_PORT = os.environ["SMTP_PORT"]
SMTP_USERNAME = os.environ["SMTP_USERNAME"]
SMTP_PASSWORD = os.environ["SMTP_PASSWORD"]
RABBITMQ_URI = os.environ["RABBITMQ_URI"]
ELASTIC_USERNAME = os.environ["ELASTIC_USERNAME"]
ELASTIC_PASSWORD = os.environ["ELASTIC_PASSWORD"]
