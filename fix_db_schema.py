import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    print("❌ DATABASE_URL not found in .env file.")
    exit(1)

# In case it's using the old 'postgres://' format
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(DATABASE_URL)

def add_columns():
    statements = [
        # Disciplinary Incidents
        "ALTER TABLE disciplinary_incidents ADD COLUMN IF NOT EXISTS acknowledgement BOOLEAN;",
        "ALTER TABLE disciplinary_incidents ADD COLUMN IF NOT EXISTS is_deleted BOOLEAN DEFAULT FALSE;",
        "ALTER TABLE disciplinary_incidents_history ADD COLUMN IF NOT EXISTS acknowledgement BOOLEAN;",
        "ALTER TABLE disciplinary_incidents_history ADD COLUMN IF NOT EXISTS is_deleted BOOLEAN DEFAULT FALSE;",
        
        # Employee Transfers
        "ALTER TABLE employee_transfers ADD COLUMN IF NOT EXISTS acknowledgement BOOLEAN;",
        "ALTER TABLE employee_transfers ADD COLUMN IF NOT EXISTS is_deleted BOOLEAN DEFAULT FALSE;",
        "ALTER TABLE employee_transfers_history ADD COLUMN IF NOT EXISTS acknowledgement BOOLEAN;",
        "ALTER TABLE employee_transfers_history ADD COLUMN IF NOT EXISTS is_deleted BOOLEAN DEFAULT FALSE;",

        # Transfer Documents
        "ALTER TABLE transfer_documents ADD COLUMN IF NOT EXISTS acknowledgement BOOLEAN;",
        "ALTER TABLE transfer_documents ADD COLUMN IF NOT EXISTS is_deleted BOOLEAN DEFAULT FALSE;",
        "ALTER TABLE transfer_documents_history ADD COLUMN IF NOT EXISTS acknowledgement BOOLEAN;",
        "ALTER TABLE transfer_documents_history ADD COLUMN IF NOT EXISTS is_deleted BOOLEAN DEFAULT FALSE;",

        # Promotions
        "ALTER TABLE promotions ADD COLUMN IF NOT EXISTS acknowledgement BOOLEAN;",
        "ALTER TABLE promotions ADD COLUMN IF NOT EXISTS is_deleted BOOLEAN DEFAULT FALSE;",
        "ALTER TABLE promotions_history ADD COLUMN IF NOT EXISTS acknowledgement BOOLEAN;",
        "ALTER TABLE promotions_history ADD COLUMN IF NOT EXISTS is_deleted BOOLEAN DEFAULT FALSE;"
    ]

    with engine.connect() as conn:
        print("🔍 Checking and adding missing columns...")
        for statement in statements:
            try:
                conn.execute(text(statement))
                conn.commit()
                # print(f"✅ Executed: {statement}")
            except Exception as e:
                print(f"⚠️ Error executing '{statement}': {e}")
                conn.rollback()

    print("\n✨ Database schema sync complete!")

if __name__ == "__main__":
    add_columns()
