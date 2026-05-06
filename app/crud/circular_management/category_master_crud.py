from sqlalchemy.orm import Session
from sqlalchemy import text
from datetime import datetime

from app.schemas.circular_management.category_master_schema import CategoryCreate, CategoryUpdate



def create_category(db: Session, data: CategoryCreate):

    payload = data.model_dump()

    query = text("""
        INSERT INTO category_master (
            category_name,
            description,
            is_deleted,
            created_by
        )
        VALUES (
            :category_name,
            :description,
            FALSE,
            :created_by
        )
        RETURNING category_id
    """)
    
    result = db.execute(query, payload)
    category_id = result.scalar()
    insert_category_master_history(db, category_id)
    db.commit()
    return category_id

def insert_category_master_history(db: Session, category_id: int):
    history_sql = text("""
        INSERT INTO category_master_history (
            category_id,              
            category_name,
            description,
            is_deleted,
            created_by,
            created_date,
            updated_by,
            updated_date
        )
        SELECT
            category_id,              
            category_name,
            description,
            is_deleted,
            created_by,
            created_date,
            updated_by,
            updated_date
        FROM category_master
        WHERE category_id = :category_id
    """)
 
    db.execute(history_sql, {"category_id": category_id})


def update_category(db: Session, category_id: int, data: CategoryUpdate):

    payload = data.model_dump(exclude_unset=True)

    if not payload:
        return False
    
    query = text("""
        UPDATE category_master
        SET
            category_name = COALESCE(:category_name, category_name),
            description   = COALESCE(:description, description),
            updated_by    = COALESCE(:updated_by, updated_by),
            updated_date  = COALESCE(:updated_date, now())
        WHERE category_id = :category_id
          AND is_deleted = FALSE
    """)

    payload["category_id"] = category_id
    db.execute(query, payload)
    insert_category_master_history(db, category_id)
    db.commit()
    return True

def get_category(db: Session, category_id: int):
    query = text("""
        SELECT
            category_id,
            category_name,
            description,
            created_by,
            created_date,
            updated_by,
            updated_date
        FROM category_master
        WHERE category_id = :category_id
        ORDER BY category_id DESC
    """)
 
    result = db.execute(
        query,
        {"category_id": category_id}
    ).mappings().first()
    return result

def get_all_category(db: Session):
    query = text("""
        SELECT
            cm.category_id,
            cm.category_name,
            cm.description,
            cm.created_by,
            cm.created_date,
            cm.updated_by,
            cm.updated_date,
            COUNT(DISTINCT pcm.publisher_id) AS publisher_count,
            COALESCE(
                json_agg(
                    DISTINCT jsonb_build_object(
                        'publisher_id', pcm.publisher_id,
                        'user_id', u.user_id,
                        'username', u.username
                    )
                ) FILTER (WHERE pcm.publisher_id IS NOT NULL),
                '[]'
            ) AS publishers
        FROM category_master cm
          JOIN publisher_master pcm
            ON EXISTS (
                SELECT 1
                FROM jsonb_array_elements_text(pcm.category_id) cat_id
                WHERE cat_id::INT = cm.category_id
            )
         JOIN users u ON pcm.user_id = u.user_id
        GROUP BY
            cm.category_id,
            cm.category_name,
            cm.description,
            cm.created_by,
            cm.created_date,
            cm.updated_by,
            cm.updated_date

        ORDER BY cm.category_id DESC
    """)
 
    result = db.execute(query).mappings().all()
    return result




def delete_category(db: Session, category_id: int, deleted_by: int = None):

    delete_subcategory_sql = text("""
        UPDATE subcategory_master
        SET
            is_deleted = TRUE
        WHERE category_id = :category_id
          AND is_deleted = FALSE
    """)

    db.execute(delete_subcategory_sql, {
        "category_id": category_id
    })

    delete_category_sql = text("""
        UPDATE category_master
        SET
            is_deleted = TRUE,
            updated_by = :deleted_by,
            updated_date = now()
        WHERE category_id = :category_id
          AND is_deleted = FALSE
    """)

    result = db.execute(delete_category_sql, {
        "category_id": category_id,
        "deleted_by": deleted_by
    })

    db.commit()

    if result.rowcount == 0:
        return False

    return True

# get_all_category_subcategory

def get_all_category_subcategory(db: Session):
    query = text("""
        SELECT
            c.category_id,
            c.category_name,

            s.subcategory_id,
            s.subcategory_name,
            s.description

        FROM category_master c
        LEFT JOIN subcategory_master s
            ON c.category_id = s.category_id
           AND s.is_deleted = FALSE

        WHERE c.is_deleted = FALSE
        ORDER BY c.category_id, s.subcategory_id
    """)

    rows = db.execute(query).mappings().all()

    categories = {}

    for row in rows:
        cat_id = row["category_id"]

        # -------- CATEGORY BASE --------
        if cat_id not in categories:
            categories[cat_id] = {
                "category_id": cat_id,
                "category_name": row["category_name"],
                "subcategories": []
            }

        # -------- SUBCATEGORIES --------
        if row["subcategory_id"]:
            categories[cat_id]["subcategories"].append({
                "subcategory_id": row["subcategory_id"],
                "subcategory_name": row["subcategory_name"],
                "description": row["description"]
            })

    return list(categories.values())