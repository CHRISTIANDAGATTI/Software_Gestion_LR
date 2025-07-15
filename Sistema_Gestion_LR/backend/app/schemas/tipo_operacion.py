from pydantic import BaseModel

class TipoOperacion(BaseModel):
    id: int
    nombre: str

    class Config:
        orm_mode = True
