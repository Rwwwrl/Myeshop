from framework.alembic.migration_runner import MigrationRunner

from user_identity.app_config import UserIdentityAppConfig

migration_runner = MigrationRunner(app_config=UserIdentityAppConfig)
migration_runner.run_migrations()
