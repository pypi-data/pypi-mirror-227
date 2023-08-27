from pydantic import BaseSettings


class Settings(BaseSettings):
    host: str = "localhost"
    port: int = 6379
    password: str = "secret"
    # embedding_model: str = "glove"
    # embedding_dim: int = 300


#class Settings(BaseSettings, case_sensitive=True):
#    redis: RedisSettings
