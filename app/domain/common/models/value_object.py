from pydantic import BaseModel, Extra


class ValueObject(BaseModel):
    class Config:
        orm_mode = True
        extra = Extra.forbid
        frozen = True
