from pydantic import BaseModel


class BotConfig(BaseModel):
    token: str
