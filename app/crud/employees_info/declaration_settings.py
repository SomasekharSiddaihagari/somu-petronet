from sqlalchemy.orm import Session

from app.models.employees_info.gloabal_setting_declaration import DeclarationSettings

def clean_dates(data: dict):
    for key in ("opening_date", "closing_date"):
        value = data.get(key)

        if value is None:
            continue

        # Convert "" or " " or "null" etc → None
        if str(value).strip().lower() in ("", "none", "null"):
            data[key] = None

    return data

def get_all_declaration_settings(db: Session):
    return db.query(DeclarationSettings).all()


def create_declaration_setting(db: Session, data: dict):
    new_item = DeclarationSettings(**data)
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item

def update_declaration_setting(db: Session, dec_id: int, data: dict):
    data = clean_dates(data)  # <-- FIX HERE

    item = db.query(DeclarationSettings).filter(
        DeclarationSettings.dec_id == dec_id
    ).first()

    if not item:
        return None

    for key, value in data.items():
        setattr(item, key, value)

    db.commit()
    db.refresh(item)
    return item

