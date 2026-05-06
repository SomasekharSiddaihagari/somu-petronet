from sqlalchemy import text
from app.database import SessionLocal

def fix_table():
    db = SessionLocal()
    try:
        print("Checking 'notifications' table schema...")
        
        # Add reference_id if missing
        db.execute(text("""
            DO $$ 
            BEGIN 
                IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                               WHERE table_name='notifications' AND column_name='reference_id') THEN
                    ALTER TABLE notifications ADD COLUMN reference_id VARCHAR;
                    RAISE NOTICE 'Added reference_id column';
                END IF;
            END $$;
        """))
        
        # Add redirect_url if missing
        db.execute(text("""
            DO $$ 
            BEGIN 
                IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                               WHERE table_name='notifications' AND column_name='redirect_url') THEN
                    ALTER TABLE notifications ADD COLUMN redirect_url VARCHAR;
                    RAISE NOTICE 'Added redirect_url column';
                END IF;
            END $$;
        """))
        
        db.commit()
        print("✅ Database schema updated successfully.")
    except Exception as e:
        db.rollback()
        print(f"❌ Error updating schema: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    fix_table()
