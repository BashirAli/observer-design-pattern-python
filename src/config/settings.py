from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    name: str = "observer-design-pattern-python"


settings = Settings()
