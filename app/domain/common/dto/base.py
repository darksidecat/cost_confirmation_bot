from pydantic import BaseModel, Extra


class DTO(BaseModel):
    class Config:
        use_enum_values = True
        extra = Extra.forbid
        frozen = True
