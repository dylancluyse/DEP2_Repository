import os

try:  # nosec
    from dotenv import load_dotenv

    load_dotenv(verbose=True)
except Exception:  # nosec
    pass

class Config():
    DATABASE: str = os.getenv("DB_NAME")
    USER: str = os.getenv("DB_USER")
    HOST: str = os.getenv("DB_HOST")
    PORT: str = os.getenv("DB_PORT")
    PASSWORD: str = os.getenv("DB_PASSWORD")

config = Config()
