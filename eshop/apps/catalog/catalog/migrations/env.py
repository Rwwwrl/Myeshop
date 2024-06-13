from catalog.app_config import CatalogAppConfig

from framework.alembic.migration_runner import MigrationRunner

migration_runner = MigrationRunner(app_config=CatalogAppConfig)
migration_runner.run_migrations()
