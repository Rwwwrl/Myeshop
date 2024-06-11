from basket.app_config import BasketAppConfig

from framework.alembic.migration_runner import MigrationRunner

migration_runner = MigrationRunner(app_config=BasketAppConfig)
migration_runner.run_migrations()
