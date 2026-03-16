from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    LINE_CHANNEL_SECRET: str
    LINE_CHANNEL_ACCESS_TOKEN: str

    class Config:
        env_file = ".env"

settings = Settings()
