from pydantic import BaseModel


class APIResponse(BaseModel):
    status_code: int
    status_message: str
    data: dict | None
