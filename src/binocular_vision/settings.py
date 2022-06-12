from pydantic import BaseSettings


class Settings(BaseSettings):
    server_host: str = 'localhost'
    server_port: int = 8000

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


settings = Settings()
