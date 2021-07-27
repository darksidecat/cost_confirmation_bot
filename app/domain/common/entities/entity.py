from pydantic import BaseModel, Extra


class Entity(BaseModel):
    class Config:
        orm_mode = True
        extra = Extra.forbid
        validate_assignment = True
        allow_mutation = True
        allow_population_by_field_name = True
