from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from crud import create_item, get_items, get_item, update_item, delete_item
from models import SessionLocal, Item


app = FastAPI()

# Dependência para obter a sessão do banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Operações CRUD

@app.post("/items/")
def create_item_api(item: dict, db: Session = Depends(get_db)):
    return create_item(db, item)

@app.get("/items/")
def read_items_api(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_items(db, skip=skip, limit=limit)

@app.get("/items/{item_id}")
def read_item_api(item_id: int, db: Session = Depends(get_db)):
    db_item = get_item(db, item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

@app.put("/items/{item_id}")
def update_item_api(item_id: int, updated_item: dict, db: Session = Depends(get_db)):
    db_item = update_item(db, item_id, updated_item)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

@app.delete("/items/{item_id}")
def delete_item_api(item_id: int, db: Session = Depends(get_db)):
    db_item = delete_item(db, item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"message": "Item deleted successfully", "deleted_item": db_item}
