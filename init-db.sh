#!/bin/bash
set -e

function create_db_if_not_exists() {
  DB_NAME=$1
  OWNER_USER=$2
  DB_EXIST=$(psql -U "$POSTGRES_USER" -tAc "SELECT 1 FROM pg_database WHERE datname='$DB_NAME'")
  
  if [ "$DB_EXIST" = "1" ]; then
    echo "Database $DB_NAME exists. Dropping it."
    psql -U "$POSTGRES_USER" -c "DROP DATABASE $DB_NAME;"
  else
    echo "Database $DB_NAME does not exist."
  fi
  
  echo "Creating database $DB_NAME with owner $OWNER_USER."
  psql -U "$POSTGRES_USER" -c "CREATE DATABASE $DB_NAME OWNER $OWNER_USER;"
}

function create_user_if_not_exists() {
  USERNAME=$1
  USER_PASSWORD=$2
  USER_EXIST=$(psql -U "$POSTGRES_USER" -tAc "SELECT 1 FROM pg_roles WHERE rolname='$USERNAME'")
  if [ "$USER_EXIST" != "1" ]; then
    psql -U "$POSTGRES_USER" -c "CREATE USER $USERNAME WITH PASSWORD '$USER_PASSWORD';"
  fi
}

function create_table_if_not_exists() {
  DB_NAME=$1
  TABLE_NAME=$2
  TABLE_EXIST=$(psql -U "$POSTGRES_USER" -d "$DB_NAME" -tAc "SELECT to_regclass('$TABLE_NAME');")
  if [ -z "$TABLE_EXIST" ]; then
    return 0
  fi
  return 1
}

create_user_if_not_exists trading trading123

create_db_if_not_exists keycloak "$POSTGRES_USER"
create_db_if_not_exists trading trading
create_db_if_not_exists temporal trading
create_db_if_not_exists temporal_visibility trading

# Create Keycloak tables
if create_table_if_not_exists keycloak realm; then
  psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "keycloak" <<-EOSQL
      CREATE TABLE realm (
          id VARCHAR(36) NOT NULL,
          name VARCHAR(255) NOT NULL UNIQUE,
          PRIMARY KEY (id)
      );
  EOSQL
fi

# Grant permissions for temporal and temporal_visibility
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "postgres" <<-EOSQL
    GRANT ALL PRIVILEGES ON DATABASE temporal TO trading;
    GRANT ALL PRIVILEGES ON DATABASE temporal_visibility TO trading;
EOSQL

# Initialize temporal schema
if [ -f /docker-entrypoint-initdb.d/temporal-schema.sql ]; then
    echo "Initializing Temporal schema..."
    psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "temporal" -f /docker-entrypoint-initdb.d/temporal-schema.sql
    
    # Create schema_version table if it doesn't exist
    psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "temporal" <<-EOSQL
        CREATE TABLE IF NOT EXISTS schema_version (
            version_partition INT NOT NULL,
            db_name VARCHAR(255) NOT NULL,
            creation_time TIMESTAMP NOT NULL,
            curr_version VARCHAR(64) NOT NULL,
            min_compatible_version VARCHAR(64) NOT NULL,
            description VARCHAR(255) NOT NULL,
            PRIMARY KEY (version_partition, db_name)
        );
        
        INSERT INTO schema_version (version_partition, db_name, creation_time, curr_version, min_compatible_version, description)
        VALUES (0, 'temporal', NOW(), '1.0', '0.1', 'base version of schema') 
        ON CONFLICT (version_partition, db_name) DO NOTHING;
    EOSQL

    # Initialize temporal_visibility schema with the same schema as temporal
    psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "temporal_visibility" -f /docker-entrypoint-initdb.d/temporal-schema.sql
    
    # Create schema_version table for visibility too
    psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "temporal_visibility" <<-EOSQL
        CREATE TABLE IF NOT EXISTS schema_version (
            version_partition INT NOT NULL,
            db_name VARCHAR(255) NOT NULL,
            creation_time TIMESTAMP NOT NULL,
            curr_version VARCHAR(64) NOT NULL,
            min_compatible_version VARCHAR(64) NOT NULL,
            description VARCHAR(255) NOT NULL,
            PRIMARY KEY (version_partition, db_name)
        );
        
        INSERT INTO schema_version (version_partition, db_name, creation_time, curr_version, min_compatible_version, description)
        VALUES (0, 'temporal_visibility', NOW(), '1.0', '0.1', 'base version of schema')
        ON CONFLICT (version_partition, db_name) DO NOTHING;
    EOSQL
fi

# Connect to temporal DB and grant schema permissions
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "temporal" <<-EOSQL
    GRANT ALL ON SCHEMA public TO trading;
    GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO trading;
    GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO trading;
    ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO trading;
    ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO trading;
EOSQL

# Connect to temporal_visibility DB and grant schema permissions
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "temporal_visibility" <<-EOSQL
    GRANT ALL ON SCHEMA public TO trading;
    GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO trading;
    GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO trading;
    ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO trading;
    ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO trading;
EOSQL

# Create Trading tables
if create_table_if_not_exists trading trades; then
  psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "trading" <<-EOSQL
      CREATE TABLE trades (
          id VARCHAR(50) NOT NULL,
          user_id VARCHAR(50) NOT NULL,
          symbol VARCHAR(20) NOT NULL,
          side VARCHAR(10) NOT NULL,
          size DECIMAL(20,8) NOT NULL,
          entry_price DECIMAL(20,8) NOT NULL,
          exit_price DECIMAL(20,8),
          pnl DECIMAL(20,8),
          timestamp TIMESTAMPTZ NOT NULL,
          PRIMARY KEY (id, timestamp)
      );

      -- удалено: SELECT create_hypertable('trades', 'timestamp', if_not_exists => TRUE);
  EOSQL

  # Create indexes with error handling
  for index in "idx_trades_user_id" "idx_trades_symbol" "idx_trades_timestamp"; do
    INDEX_EXIST=$(psql -U "$POSTGRES_USER" -d "trading" -tAc "SELECT 1 FROM pg_indexes WHERE indexname='$index'")
    if [ "$INDEX_EXIST" != "1" ]; then
      case $index in
        "idx_trades_user_id")
          psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "trading" -c "CREATE INDEX $index ON trades(user_id);"
          ;;
        "idx_trades_symbol")
          psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "trading" -c "CREATE INDEX $index ON trades(symbol);"
          ;;
        "idx_trades_timestamp")
          psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "trading" -c "CREATE INDEX $index ON trades(timestamp DESC);"
          ;;
      esac
    fi
  done
fi

# Grant permissions for trading db to trading user
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "trading" <<-EOSQL
    GRANT ALL PRIVILEGES ON DATABASE trading TO trading;
    GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO trading;
    GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO trading;
    ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO trading;
    ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO trading;
EOSQL 