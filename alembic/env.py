import sys
from pathlib import Path
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

# Tambahkan direktori root proyek ke sys.path agar bisa mengimpor modul app
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

# Import settings dan Base metadata dari app
from app.core.config import settings
from app.models import Base  # Mengimpor Base dan semua model yang terdaftar di __init__.py

config = context.config

# Setup logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Escape simbol '%' agar configparser tidak menganggapnya sebagai interpolation variable (%23 -> %%23)
escaped_url = settings.DATABASE_URL.replace("%", "%%")
config.set_main_option("sqlalchemy.url", escaped_url)

# Daftarkan metadata model untuk autogenerate
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    context.configure(
        url=settings.DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    configuration = config.get_section(config.config_ini_section, {})
    configuration["sqlalchemy.url"] = settings.DATABASE_URL

    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
