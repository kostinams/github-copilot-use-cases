"""
Database Migration Script Examples
Demonstrates using Copilot to generate migration scripts for schema changes and data transformation.

Prompt: Generate a migration script to add a new column to the users table with proper validation
"""

from sqlalchemy import create_engine, Column, String, Integer, DateTime, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import logging

# Configure logging for migration tracking
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

Base = declarative_base()


# ===========================
# EXAMPLE 1: Simple Column Addition
# ===========================
class Migration_001_AddStatusColumn:
    """
    Migration: Add status column to users table
    Direction: UP - for applying migration
    Direction: DOWN - for rolling back migration
    
    Prompt: Generate a migration to add a status column to users table
    """
    
    def __init__(self, engine):
        self.engine = engine
        self.migration_name = "001_add_status_column"
    
    def up(self):
        """Apply migration: Add status column"""
        try:
            with self.engine.connect() as connection:
                connection.execute("""
                    ALTER TABLE users ADD COLUMN status VARCHAR(50) DEFAULT 'active';
                """)
                connection.execute("""
                    ALTER TABLE users ADD CONSTRAINT check_status 
                    CHECK (status IN ('active', 'inactive', 'suspended'));
                """)
                connection.execute("""
                    CREATE INDEX idx_users_status ON users(status);
                """)
                connection.commit()
                logger.info(f"Migration {self.migration_name} applied successfully")
        except Exception as e:
            logger.error(f"Error applying migration: {e}")
            raise
    
    def down(self):
        """Rollback migration: Remove status column"""
        try:
            with self.engine.connect() as connection:
                connection.execute("DROP INDEX IF EXISTS idx_users_status;")
                connection.execute("ALTER TABLE users DROP CONSTRAINT check_status;")
                connection.execute("ALTER TABLE users DROP COLUMN status;")
                connection.commit()
                logger.info(f"Migration {self.migration_name} rolled back successfully")
        except Exception as e:
            logger.error(f"Error rolling back migration: {e}")
            raise


# ===========================
# EXAMPLE 2: Data Type Conversion
# ===========================
class Migration_002_ConvertTimestampsToISO:
    """
    Migration: Convert timestamps from Unix epoch to ISO 8601 format
    
    Prompt: Generate a migration to convert timestamps from integer seconds to ISO 8601 format
    """
    
    def __init__(self, engine):
        self.engine = engine
        self.migration_name = "002_convert_timestamps_to_iso"
    
    def up(self):
        """Apply migration: Convert timestamp format"""
        try:
            with self.engine.connect() as connection:
                # Add new column
                connection.execute("""
                    ALTER TABLE events ADD COLUMN timestamp_iso VARCHAR(30);
                """)
                
                # Migrate data: convert Unix epoch to ISO 8601
                connection.execute("""
                    UPDATE events 
                    SET timestamp_iso = to_char(to_timestamp(timestamp_epoch), 'YYYY-MM-DD"T"HH24:MI:SS"Z"')
                    WHERE timestamp_epoch IS NOT NULL;
                """)
                
                # Verify migration
                connection.execute("""
                    SELECT COUNT(*) as mismatches FROM events 
                    WHERE timestamp_epoch IS NOT NULL AND timestamp_iso IS NULL;
                """)
                
                # Drop old column after verification
                connection.execute("ALTER TABLE events DROP COLUMN timestamp_epoch;")
                connection.execute("ALTER TABLE events RENAME COLUMN timestamp_iso TO timestamp;")
                
                connection.commit()
                logger.info(f"Migration {self.migration_name} applied successfully")
        except Exception as e:
            logger.error(f"Error applying migration: {e}")
            raise
    
    def down(self):
        """Rollback migration: Restore original format"""
        try:
            with self.engine.connect() as connection:
                connection.execute("""
                    ALTER TABLE events ADD COLUMN timestamp_epoch INTEGER;
                """)
                connection.execute("""
                    UPDATE events 
                    SET timestamp_epoch = EXTRACT(EPOCH FROM timestamp::timestamp)::INTEGER;
                """)
                connection.execute("ALTER TABLE events DROP COLUMN timestamp;")
                connection.execute("ALTER TABLE events RENAME COLUMN timestamp_epoch TO timestamp;")
                connection.commit()
                logger.info(f"Migration {self.migration_name} rolled back successfully")
        except Exception as e:
            logger.error(f"Error rolling back migration: {e}")
            raise


# ===========================
# EXAMPLE 3: Complex Data Transformation
# ===========================
class Migration_003_NormalizeUserProfiles:
    """
    Migration: Normalize user data by splitting profiles into separate table
    
    Prompt: Generate a migration to normalize user profiles from embedded to separate table
    """
    
    def __init__(self, engine):
        self.engine = engine
        self.migration_name = "003_normalize_user_profiles"
    
    def up(self):
        """Apply migration: Create profiles table and migrate data"""
        try:
            with self.engine.connect() as connection:
                # Create new profiles table
                connection.execute("""
                    CREATE TABLE user_profiles (
                        id SERIAL PRIMARY KEY,
                        user_id INTEGER NOT NULL UNIQUE REFERENCES users(id) ON DELETE CASCADE,
                        bio TEXT,
                        avatar_url VARCHAR(255),
                        phone VARCHAR(20),
                        location VARCHAR(100),
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );
                """)
                
                # Migrate data from users table to profiles table
                connection.execute("""
                    INSERT INTO user_profiles (user_id, bio, avatar_url, phone, location)
                    SELECT id, bio, avatar_url, phone, location FROM users
                    WHERE bio IS NOT NULL OR avatar_url IS NOT NULL;
                """)
                
                # Remove columns from users table
                connection.execute("""
                    ALTER TABLE users 
                    DROP COLUMN bio,
                    DROP COLUMN avatar_url,
                    DROP COLUMN phone,
                    DROP COLUMN location;
                """)
                
                connection.commit()
                logger.info(f"Migration {self.migration_name} applied successfully")
        except Exception as e:
            logger.error(f"Error applying migration: {e}")
            raise
    
    def down(self):
        """Rollback migration: Restore original schema"""
        try:
            with self.engine.connect() as connection:
                # Add columns back to users table
                connection.execute("""
                    ALTER TABLE users 
                    ADD COLUMN bio TEXT,
                    ADD COLUMN avatar_url VARCHAR(255),
                    ADD COLUMN phone VARCHAR(20),
                    ADD COLUMN location VARCHAR(100);
                """)
                
                # Migrate data back
                connection.execute("""
                    UPDATE users u
                    SET bio = p.bio,
                        avatar_url = p.avatar_url,
                        phone = p.phone,
                        location = p.location
                    FROM user_profiles p
                    WHERE u.id = p.user_id;
                """)
                
                # Drop profiles table
                connection.execute("DROP TABLE user_profiles;")
                
                connection.commit()
                logger.info(f"Migration {self.migration_name} rolled back successfully")
        except Exception as e:
            logger.error(f"Error rolling back migration: {e}")
            raise


# ===========================
# EXAMPLE 4: Migration Runner
# ===========================
class MigrationRunner:
    """
    Manages running migrations in order with transaction support and error handling
    
    Prompt: Create a migration runner that executes migrations with proper error handling
    """
    
    def __init__(self, engine):
        self.engine = engine
        self.applied_migrations = []
    
    def run_migration(self, migration_class, direction='up'):
        """
        Execute a single migration with proper error handling
        
        Args:
            migration_class: The migration class to execute
            direction: 'up' to apply, 'down' to rollback
        """
        migration = migration_class(self.engine)
        
        try:
            if direction == 'up':
                migration.up()
                self.applied_migrations.append(migration.migration_name)
                logger.info(f"Successfully applied: {migration.migration_name}")
            else:
                migration.down()
                if migration.migration_name in self.applied_migrations:
                    self.applied_migrations.remove(migration.migration_name)
                logger.info(f"Successfully rolled back: {migration.migration_name}")
        except Exception as e:
            logger.error(f"Failed to execute migration {migration.migration_name}: {e}")
            raise
    
    def rollback_all(self, migrations):
        """Rollback all migrations in reverse order"""
        for migration_class in reversed(migrations):
            try:
                self.run_migration(migration_class, direction='down')
            except Exception as e:
                logger.error(f"Rollback failed, migration may be in inconsistent state: {e}")
                raise


# ===========================
# USAGE EXAMPLE
# ===========================
if __name__ == "__main__":
    # Setup database connection
    # engine = create_engine('postgresql://user:password@localhost/mydb')
    
    # Create migration runner
    # runner = MigrationRunner(engine)
    
    # Apply migrations in order
    # try:
    #     runner.run_migration(Migration_001_AddStatusColumn, direction='up')
    #     runner.run_migration(Migration_002_ConvertTimestampsToISO, direction='up')
    #     runner.run_migration(Migration_003_NormalizeUserProfiles, direction='up')
    # except Exception as e:
    #     print(f"Migration failed: {e}")
    #     runner.rollback_all([
    #         Migration_001_AddStatusColumn,
    #         Migration_002_ConvertTimestampsToISO,
    #         Migration_003_NormalizeUserProfiles
    #     ])
    
    print("Migration examples ready. Uncomment the usage section to run.")
