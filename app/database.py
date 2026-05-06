# # app/database.py
# import os
# from dotenv import load_dotenv
# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker

# #  Load environment variables
# load_dotenv()

# #  Read database URL from .env
# SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# #  Create SQLAlchemy engine
# engine = create_engine(SQLALCHEMY_DATABASE_URL)

# # SessionLocal
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# #  Base class for models
# Base = declarative_base()

# #  Dependency for FastAPI routes
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()



# import os
# from dotenv import load_dotenv
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker, declarative_base

# # -------------------------------
# # Load environment variables
# # -------------------------------
# load_dotenv()

# # -------------------------------
# # Read database URL from .env
# # Example:
# # DATABASE_URL=postgresql://user:password@host:5432/dbname
# # -------------------------------
# SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# # -------------------------------
# # Create SQLAlchemy Engine
# # Connection pool tuned for PostgreSQL max_connections = 100
# # -------------------------------
# engine = create_engine(
#     SQLALCHEMY_DATABASE_URL,
#     pool_size=30,        # permanent connections
#     max_overflow=40,     # temporary burst connections
#     pool_timeout=30,     # wait time before pool timeout error
#     pool_recycle=1800,   # recycle connections every 30 minutes
#     pool_pre_ping=True   # check connection health automatically
# )

# # -------------------------------
# # Session Factory
# # -------------------------------
# SessionLocal = sessionmaker(
#     autocommit=False,
#     autoflush=False,
#     bind=engine
# )

# # -------------------------------
# # Base class for SQLAlchemy models
# # -------------------------------
# Base = declarative_base()

# # -------------------------------
# # Dependency for FastAPI routes
# # Ensures DB session is closed after request
# # -------------------------------
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# -------------------------------
# Pool Math for 80 users
# PostgreSQL max_connections = 100
# Reserve 5 for admin/migrations
# Assuming 2 Uvicorn workers
# 95 / 2 workers = ~47 → use 20 pool + 5 overflow = 25 per worker = 50 total (safe)
# -------------------------------
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_size=20,           # 20 × 2 workers = 40 base connections
    max_overflow=5,         # 5 × 2 workers = 10 burst = 50 total max (safe under 95)
    pool_timeout=30,        # wait 30s before raising timeout error
    pool_recycle=1800,      # recycle every 30 min (prevents stale connections)
    pool_pre_ping=True,     # health check before using a connection
    connect_args={
        "options": (
            "-c statement_timeout=30000 "              # kill slow queries after 30s
            "-c idle_in_transaction_session_timeout=60000"  # kill stuck transactions after 60s
        )
    }
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

# -------------------------------
# Dependency for FastAPI routes
# -------------------------------
# ✅ Fixed
def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception:
        db.rollback()
        raise  # <-- this is the critical missing line
    finally:
        db.close()