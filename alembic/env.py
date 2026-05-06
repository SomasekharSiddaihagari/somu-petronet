from alembic import context
from sqlalchemy import engine_from_config, pool
from logging.config import fileConfig
import os
from dotenv import load_dotenv
from configparser import BasicInterpolation

# ------------------------------------------------------------
# Load environment variables
# ------------------------------------------------------------
load_dotenv()

# ------------------------------------------------------------
# Import Base and all models
# ------------------------------------------------------------
from app.database import Base

# Existing models
from app.models import UserModel
from app.models.RoleModel import Role
from app.models.MOC.StationModel import Station

# 🟢 NEW MODELS (add these lines)
from app.models.MOC.MocRequestModel import MoCRequest
from app.models.MOC.MocClosureModel import MoCClosure
from app.models.MOC.HiraModel import HIRAEntry

# ------------------------------------------------------------
# Alembic Config
# ------------------------------------------------------------
config = context.config
config.file_config._interpolation = BasicInterpolation()

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL not found in .env file.")


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        {"sqlalchemy.url": DATABASE_URL},
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
