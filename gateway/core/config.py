from pydantic import BaseSettings

class Settings(BaseSettings):
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_DB: int = 0
    REDIS_DECODE_RESPONSES: bool = True

    class Config:
        env_file = ".env"

settings = Settings()
