-- Create postgres user if not exists
DO
$do$
BEGIN
   IF NOT EXISTS (
      SELECT FROM pg_catalog.pg_roles
      WHERE  rolname = 'postgres') THEN
      CREATE USER postgres WITH PASSWORD 'postgres123' SUPERUSER;
   END IF;
END
$do$;

-- Create keycloak database
CREATE DATABASE keycloak;
\c keycloak;

-- Create Keycloak tables
CREATE TABLE IF NOT EXISTS realm (
    id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(255),
    enabled BOOLEAN,
    ssl_required VARCHAR(255),
    registration_allowed BOOLEAN,
    reset_password_allowed BOOLEAN,
    verify_email BOOLEAN,
    login_with_email_allowed BOOLEAN,
    duplicate_emails_allowed BOOLEAN,
    remember_me BOOLEAN,
    registration_email_as_username BOOLEAN
);

-- Create trading database
CREATE DATABASE trading;
\c trading;

-- Create schema core
CREATE SCHEMA IF NOT EXISTS core;

-- Create schema metrics
CREATE SCHEMA IF NOT EXISTS metrics;

-- Create users table
CREATE TABLE core.users (
    id UUID PRIMARY KEY,
    email CITEXT UNIQUE NOT NULL,
    role VARCHAR(20) CHECK (role IN ('trader', 'manager', 'admin', 'superadmin')),
    preferred_locale VARCHAR(5) DEFAULT 'en-US',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create user_api_keys table
CREATE TABLE core.user_api_keys (
    user_id UUID PRIMARY KEY REFERENCES core.users(id),
    exchange VARCHAR(16) NOT NULL,
    api_key_enc BYTEA NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create wallet_transactions table
CREATE TABLE core.wallet_transactions (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES core.users(id),
    amount NUMERIC(20,8) NOT NULL,
    currency VARCHAR(6) NOT NULL,
    source VARCHAR(20) CHECK (source IN ('stripe', 'btcpay', 'fee')),
    ext_ref VARCHAR(128),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create orders table
CREATE TABLE core.orders (
    id BIGSERIAL PRIMARY KEY,
    user_id UUID REFERENCES core.users(id),
    exchange_order_id VARCHAR(64),
    pair VARCHAR(10) NOT NULL,
    side VARCHAR(10) CHECK (side IN ('long', 'short')),
    leverage INTEGER NOT NULL,
    amount NUMERIC(20,8) NOT NULL,
    status VARCHAR(20) CHECK (status IN ('new', 'filled', 'closed', 'error')),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create metrics.pnl hypertable
CREATE TABLE metrics.pnl (
    time TIMESTAMPTZ NOT NULL,
    user_id UUID NOT NULL,
    symbol VARCHAR(10) NOT NULL,
    pnl_usd NUMERIC(20,8) NOT NULL
);

-- Create hypertable for pnl
SELECT create_hypertable('metrics.pnl', 'time', chunk_time_interval => INTERVAL '1 day');

-- Create indexes
CREATE INDEX idx_orders_user_id ON core.orders(user_id);
CREATE INDEX idx_orders_status ON core.orders(status);
CREATE INDEX idx_orders_created_at ON core.orders(created_at DESC);
CREATE INDEX idx_wallet_transactions_user_id ON core.wallet_transactions(user_id);
CREATE INDEX idx_wallet_transactions_created_at ON core.wallet_transactions(created_at DESC);
CREATE INDEX idx_pnl_user_id ON metrics.pnl(user_id);
CREATE INDEX idx_pnl_time ON metrics.pnl(time DESC);

-- Create audit_log table
CREATE TABLE core.audit_log (
    id BIGSERIAL PRIMARY KEY,
    user_id UUID REFERENCES core.users(id),
    action VARCHAR(50) NOT NULL,
    table_name VARCHAR(50) NOT NULL,
    record_id VARCHAR(50) NOT NULL,
    old_data JSONB,
    new_data JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create indexes for audit_log
CREATE INDEX idx_audit_log_user_id ON core.audit_log(user_id);
CREATE INDEX idx_audit_log_created_at ON core.audit_log(created_at DESC); 