from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas, crud, database, dependencies

# Create DB tables
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Message Persistence Service")

@app.post("/messages/", response_model=schemas.Message)
def create_message(message: schemas.MessageCreate, db: Session = Depends(database.get_db), api_key: str = Depends(dependencies.get_api_key)):
    return crud.create_message(db, message)

@app.put("/messages/{message_id}", response_model=schemas.Message)
def update_message(message_id: str, message: schemas.MessageUpdate, db: Session = Depends(database.get_db), api_key: str = Depends(dependencies.get_api_key)):
    updated = crud.update_message(db, message_id, message)
    if not updated:
        raise HTTPException(status_code=404, detail="Message not found")
    return updated

@app.get("/messages/", response_model=list[schemas.Message])
def read_messages(db: Session = Depends(database.get_db), api_key: str = Depends(dependencies.get_api_key)):
    return crud.get_all_messages(db)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )