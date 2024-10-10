from sqlalchemy.orm import Session
import models_database
import schemas_database


def get_item(db: Session, item_id: int):
    return db.query(models_database.Item).filter(
        models_database.Item.id == item_id).first()


def get_items(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models_database.Item).offset(skip).limit(limit).all()


def create_item(db: Session, item: schemas_database.ItemCreate):
    db_item = models_database.Item(
        id=item.id,
        username=item.username,
        code=item.code,
        date=item.date,
        model=item.model,
        prediction=item.prediction,
        prediction_probability=item.prediction_probability,
        explainability_file=item.explainability_file,
        results_file=item.results_file)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
