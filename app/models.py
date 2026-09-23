from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship

class UsuarioBase(SQLModel):
    nombre: str
    email: str

class Usuario(UsuarioBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    productos: List["Producto"] = Relationship(back_populates="propietario")

class UsuarioCreate(UsuarioBase):
    pass

class UsuarioRead(UsuarioBase):
    id: int

class ProductoBase(SQLModel):
    titulo: str
    precio: float
    usuario_id: Optional[int] = Field(default=None, foreign_key="usuario.id")

class Producto(ProductoBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    propietario: Optional[Usuario] = Relationship(back_populates="productos")

class ProductoCreate(ProductoBase):
    pass

class ProductoRead(ProductoBase):
    id: int