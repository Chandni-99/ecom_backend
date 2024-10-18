import os
from urllib.parse import quote
from dotenv import load_dotenv
from pydantic.v1 import BaseSettings

load_dotenv("env/project.env")

class Settings(BaseSettings):
    PROJECT_NAME: str
    MYSQL_DB: str
    MYSQL_USER: str
    MYSQL_PASSWORD: str
    MYSQL_HOST: str
    MYSQL_PORT: str
    ACCESS_TOKEN_EXPIRE_MINUTES :int
    REFRESH_TOKEN_EXPIRE_DAYS : int

    PROJECT_NAME = os.getenv("PROJECT_NAME")
    MYSQL_DB = os.getenv("MYSQL_DB")
    MYSQL_USER = os.getenv("MYSQL_USER")
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
    MYSQL_HOST = os.getenv("MYSQL_HOST")
    MYSQL_PORT = os.getenv("MYSQL_PORT")
    ACCESS_TOKEN_EXPIRE_MINUTES =os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
    SECRET_KEY =os.getenv("SECRET_KEY")
    ALGORITHM =os.getenv("ALGORITHM")
    REFRESH_TOKEN_EXPIRE_DAYS =os.getenv("REFRESH_TOKEN_EXPIRE_DAYS")

    # URL-encode the password here
    encoded_password = quote(MYSQL_PASSWORD)
    safe_password = encoded_password.replace('%',"%%")

    # Build the database URL with the encoded password
    DB_URL = f"mysql+pymysql://{MYSQL_USER}:{safe_password}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"

    class Config:
        env_file = "env/project.env"  # Adjust path as needed

settings = Settings()

