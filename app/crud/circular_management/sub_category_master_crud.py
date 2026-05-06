from sqlalchemy.orm import Session
from sqlalchemy import text

from app.schemas.circular_management.sub_category_master_schema import SubCategoryCreate, SubCategoryUpdate

def create_subcategory(db: Session, data: SubCategoryCreate):
    payload = data.model_dump()

    query = text("""
        INSERT INTO subcategory_master (
            subcategory_name,
            category_id,
            description,
            is_deleted
        )
        VALUES (
            :subcategory_name,
            :category_id,
            :description,
            FALSE
        )
        RETURNING subcategory_id
    """)

    result = db.execute(query, payload)
    subcategory_id = result.scalar()
    db.commit()
    return subcategory_id


def update_subcategory(db: Session, subcategory_id: int, data: SubCategoryUpdate):
    payload = data.model_dump(exclude_unset=True)

    if not payload:
        return False

    query = text("""
        UPDATE subcategory_master
        SET
            subcategory_name = COALESCE(:subcategory_name, subcategory_name),
            category_id      = COALESCE(:category_id, category_id),
            description      = COALESCE(:description, description)
        WHERE subcategory_id = :subcategory_id
          AND is_deleted = FALSE
    """)

    payload["subcategory_id"] = subcategory_id
    db.execute(query, payload)
    db.commit()
    return True


def get_subcategory(db: Session, subcategory_id: int):
    query = text("""
        SELECT
            sc.subcategory_id,
            sc.subcategory_name,
            sc.category_id,
            cm.category_name,
            sc.description
        FROM subcategory_master sc
        INNER JOIN category_master cm ON cm.category_id = sc.category_id
        WHERE sc.subcategory_id = :subcategory_id AND sc.is_deleted = FALSE AND cm.is_deleted = FALSE
    """)

    result = db.execute(
        query,
        {"subcategory_id": subcategory_id}
    ).mappings().first()

    return result


def get_all_subcategory(db: Session):
    query = text("""
        SELECT
            sc.subcategory_id,
            sc.subcategory_name,
            sc.category_id,
            cm.category_name,
            sc.description
        FROM subcategory_master sc
        INNER JOIN category_master cm ON cm.category_id = sc.category_id
        WHERE sc.is_deleted = FALSE AND cm.is_deleted = FALSE
        ORDER BY subcategory_id DESC
    """)

    result = db.execute(query).mappings().all()
    return result


def delete_subcategory(db: Session, subcategory_id: int):
    query = text("""
        UPDATE subcategory_master
        SET
            is_deleted = TRUE
            WHERE subcategory_id = :subcategory_id
    """)

    db.execute(query, {
        "subcategory_id": subcategory_id
    })
    db.commit()
    return True
