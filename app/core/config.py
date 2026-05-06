import os
from pydantic import BaseModel, Field

class Settings(BaseModel):
    env: str = Field(default=os.getenv("ENV", "dev"))
    database_url: str = Field(default=os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./app.db"))
    secret_key: str = Field(default=os.getenv("SECRET_KEY", "change-me"))

settings = Settings()
