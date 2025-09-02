from sqlalchemy.orm import Session
from . import models, schemas
from uuid import UUID

def create_message(db: Session, message: schemas.MessageCreate):
    """
    Create a new message in the database.

    Args:
        db (Session): SQLAlchemy database session.
        message (schemas.MessageCreate): Pydantic model containing message data.

    Returns:
        models.Message: The newly created message object, including database-generated fields (e.g., message_id).
    """
    db_message = models.Message(**message.model_dump())
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message

def update_message(db: Session, message_id: UUID, message: schemas.MessageUpdate):
    """
    Update an existing message in the database.

    Args:
        db (Session): SQLAlchemy database session.
        message_id (UUID): The UUID of the message to update.
        message (schemas.MessageUpdate): Pydantic model containing fields to update. Only provided fields are updated.

    Returns:
        models.Message | None: The updated message object if found, otherwise None.
    """
    db_message = db.query(models.Message).filter(models.Message.message_id == message_id).first()
    if not db_message:
        return None
    for key, value in message.model_dump(exclude_unset=True).items():
        setattr(db_message, key, value)
    db.commit()
    db.refresh(db_message)
    return db_message

def get_all_messages(db: Session):
    """
    Retrieve all messages from the database.

    Args:
        db (Session): SQLAlchemy database session.

    Returns:
        list[models.Message]: A list of all message objects stored in the database.
    """
    return db.query(models.Message).all()
