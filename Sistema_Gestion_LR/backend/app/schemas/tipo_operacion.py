from pydantic import BaseModel

class TipoOperacionBase(BaseModel):
    nombre: str

class TipoOperacionCreate(TipoOperacionBase):
    pass

class TipoOperacion(TipoOperacionBase):
    id: int

    class Config:
        from_attributes = True
