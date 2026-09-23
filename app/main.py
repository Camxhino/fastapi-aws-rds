from typing import List
from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session, select
from app.database import get_session, init_db
from app.models import (
    Usuario, UsuarioCreate, UsuarioRead,
    Producto, ProductoCreate, ProductoRead
)

app = FastAPI(
    title="API con FastAPI, EC2 y RDS",
    description="API RESTful conectada a base de datos PostgreSQL en Amazon RDS.",
    version="1.0.0"
)

@app.on_event("startup")
def on_startup():
    init_db()

# --- ENDPOINTS USUARIOS ---
@app.post("/usuarios/", response_model=UsuarioRead, status_code=201, tags=["Usuarios"])
def crear_usuario(usuario: UsuarioCreate, session: Session = Depends(get_session)):
    db_user = Usuario.from_orm(usuario)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

@app.get("/usuarios/", response_model=List[UsuarioRead], tags=["Usuarios"])
def listar_usuarios(session: Session = Depends(get_session)):
    return session.exec(select(Usuario)).all()

@app.get("/usuarios/{usuario_id}", response_model=UsuarioRead, tags=["Usuarios"])
def obtener_usuario(usuario_id: int, session: Session = Depends(get_session)):
    user = session.get(Usuario, usuario_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user

@app.put("/usuarios/{usuario_id}", response_model=UsuarioRead, tags=["Usuarios"])
def actualizar_usuario(usuario_id: int, datos: UsuarioCreate, session: Session = Depends(get_session)):
    user = session.get(Usuario, usuario_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    user.nombre = datos.nombre
    user.email = datos.email
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

@app.delete("/usuarios/{usuario_id}", tags=["Usuarios"])
def eliminar_usuario(usuario_id: int, session: Session = Depends(get_session)):
    user = session.get(Usuario, usuario_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    session.delete(user)
    session.commit()
    return {"message": f"Usuario {usuario_id} eliminado exitosamente"}

@app.post("/productos/", response_model=ProductoRead, status_code=201, tags=["Productos"])
def crear_producto(producto: ProductoCreate, session: Session = Depends(get_session)):
    db_prod = Producto.from_orm(producto)
    session.add(db_prod)
    session.commit()
    session.refresh(db_prod)
    return db_prod

@app.get("/productos/", response_model=List[ProductoRead], tags=["Productos"])
def listar_productos(session: Session = Depends(get_session)):
    return session.exec(select(Producto)).all()

@app.get("/productos/{producto_id}", response_model=ProductoRead, tags=["Productos"])
def obtener_producto(producto_id: int, session: Session = Depends(get_session)):
    prod = session.get(Producto, producto_id)
    if not prod:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return prod

@app.put("/productos/{producto_id}", response_model=ProductoRead, tags=["Productos"])
def actualizar_producto(producto_id: int, datos: ProductoCreate, session: Session = Depends(get_session)):
    prod = session.get(Producto, producto_id)
    if not prod:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    prod.titulo = datos.titulo
    prod.precio = datos.precio
    prod.usuario_id = datos.usuario_id
    session.add(prod)
    session.commit()
    session.refresh(prod)
    return prod

@app.delete("/productos/{producto_id}", tags=["Productos"])
def eliminar_producto(producto_id: int, session: Session = Depends(get_session)):
    prod = session.get(Producto, producto_id)
    if not prod:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    session.delete(prod)
    session.commit()
    return {"message": f"Producto {producto_id} eliminado exitosamente"}