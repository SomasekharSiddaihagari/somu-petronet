from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.MOC.MocfileModel import File

def get_files_by_model_name(db: Session, model_name: str) -> List[File]:
    return db.query(File).filter_by(model_name=model_name).all()

def create_file(db: Session, filename: str, filepath: str, moc_request_id: int, moc_request_no: str) -> File:
    new_file = File(
        filename=filename,
        filepath=filepath,
        moc_request_id=moc_request_id,
        moc_request_no=moc_request_no,
    )
    db.add(new_file)
    db.commit()
    db.refresh(new_file)
    return new_file

def get_files_by_model_id(db: Session, model_id: int) -> List[File]:
    return db.query(File).filter_by(model_id=model_id).all()



def get_file_by_id(db: Session, file_id: int) -> Optional[File]:
    return db.query(File).filter_by(id=file_id).first()


def delete_file(db: Session, file_id: int):
    file = get_file_by_id(db, file_id)
    if file:
        db.delete(file)
        db.commit()
def get_file_by_id(db: Session, file_id: int) -> Optional[File]:
    return db.query(File).filter_by(id=file_id).first()