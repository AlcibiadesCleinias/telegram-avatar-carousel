from pydantic import BaseModel, validator


class RequestBase(BaseModel):
    api_key: int
    api_hash: str
    phone: str

    @validator('api_key', pre=True)
    def parse_api_key(cls, value):
        return int(value)


class RequestCode(RequestBase):
    pass


class PostCodeIn(RequestBase):
    code: str
    password: str


class PostCodeOut(RequestBase):
    pass


# class ImagesIn(ImagesBase):
#
#     @validator('start', 'end', pre=True)
#     def parse_date(cls, value):
#         return datetime.fromisoformat(value)
#
#
# class Image(BaseModel):
#     message_id: int
#     file: bytes
#
#
# class ImagesOut(ImagesBase):
#     images: List[Image]
