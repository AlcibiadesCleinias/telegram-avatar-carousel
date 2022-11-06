from pydantic import BaseModel, validator


class ChangeAvatar(BaseModel):
    api_key: int
    api_hash: str
    phone: str
    image_url: str

    @validator('api_key', pre=True)
    def parse_api_key(cls, value):
        return int(value)
