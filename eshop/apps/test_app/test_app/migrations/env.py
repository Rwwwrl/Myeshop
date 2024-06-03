from test_app.app_config import TestAppConfig

from framework.alembic.migration_runner import MigrationRunner

migration_runner = MigrationRunner(app_config=TestAppConfig)
migration_runner.run_migrations()
