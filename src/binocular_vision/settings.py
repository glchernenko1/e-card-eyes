from lib2to3.pgen2 import driver

from jose import jwt
from pydantic import BaseSettings


class Settings(BaseSettings):
    server_host: str = 'localhost'
    server_port: int = 8000

    dialect: str = 'postgresql'
    driver: str = 'psycopg2'
    database_url: str = 'localhost'
    port_db: str = '5432'
    postgres_user: str = 'user'
    postgres_password: str = '1234'
    postgres_db_name: str = 'postgres'

    jwt_secret: str
    jwt_algorithm: str = 'HS256'
    jwt_expiration_doctor: int = 9
    jwt_expiration_patient: int = 1

    def get_url_db(self) -> str:
        return f'{self.dialect}+{self.driver}://{self.postgres_user}:' \
               f'{self.postgres_password}@{self.database_url}:{self.port_db}/{self.postgres_db_name}'

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


settings = Settings(_env_file='../../.env')
