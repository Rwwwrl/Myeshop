from framework.alembic.migration_runner import MigrationRunner

from order.app_config import OrderAppConfig

migration_runner = MigrationRunner(app_config=OrderAppConfig)
migration_runner.run_migrations()
