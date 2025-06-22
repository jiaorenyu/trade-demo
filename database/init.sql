-- E-Commerce Platform Database Schema
-- Implementation of CREATIVE-001 Database Design
-- Single PostgreSQL database with service-specific schemas

-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Create schemas for each microservice
CREATE SCHEMA IF NOT EXISTS auth_service;
CREATE SCHEMA IF NOT EXISTS user_service;
CREATE SCHEMA IF NOT EXISTS product_service;
CREATE SCHEMA IF NOT EXISTS order_service;
CREATE SCHEMA IF NOT EXISTS payment_service;
CREATE SCHEMA IF NOT EXISTS localization_service;
CREATE SCHEMA IF NOT EXISTS admin_service;

-- ==============================================
-- LOCALIZATION SERVICE SCHEMA (Dependencies First)
-- ==============================================

-- Supported languages
CREATE TABLE localization_service.languages (
    code VARCHAR(10) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    native_name VARCHAR(100) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Supported currencies
CREATE TABLE localization_service.currencies (
    code VARCHAR(3) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    symbol VARCHAR(10) NOT NULL,
    decimal_places INTEGER DEFAULT 2,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Exchange rates
CREATE TABLE localization_service.exchange_rates (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    from_currency VARCHAR(3) NOT NULL REFERENCES localization_service.currencies(code),
    to_currency VARCHAR(3) NOT NULL REFERENCES localization_service.currencies(code),
    rate DECIMAL(20,8) NOT NULL,
    effective_date TIMESTAMPTZ NOT NULL,
    source VARCHAR(50) NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(from_currency, to_currency, effective_date)
);

-- ==============================================
-- AUTH SERVICE SCHEMA
-- ==============================================

-- Users table for authentication
CREATE TABLE auth_service.users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    email_verified BOOLEAN DEFAULT FALSE,
    verification_token VARCHAR(255),
    reset_token VARCHAR(255),
    reset_token_expires TIMESTAMPTZ,
    is_active BOOLEAN DEFAULT TRUE,
    last_login TIMESTAMPTZ,
    failed_login_attempts INTEGER DEFAULT 0,
    account_locked_until TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Refresh tokens for JWT management
CREATE TABLE auth_service.refresh_tokens (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES auth_service.users(id) ON DELETE CASCADE,
    token_hash VARCHAR(255) NOT NULL,
    expires_at TIMESTAMPTZ NOT NULL,
    is_revoked BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ==============================================
-- USER SERVICE SCHEMA
-- ==============================================

-- User profiles (extends auth data)
CREATE TABLE user_service.profiles (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID UNIQUE NOT NULL, -- References auth_service.users.id
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    phone VARCHAR(20),
    preferred_language VARCHAR(10) DEFAULT 'en' REFERENCES localization_service.languages(code),
    preferred_currency VARCHAR(3) DEFAULT 'USD' REFERENCES localization_service.currencies(code),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- User addresses
CREATE TABLE user_service.addresses (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL, -- References auth_service.users.id
    type VARCHAR(20) NOT NULL CHECK (type IN ('billing', 'shipping', 'both')),
    is_primary BOOLEAN DEFAULT FALSE,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    address_line_1 VARCHAR(255) NOT NULL,
    city VARCHAR(100) NOT NULL,
    postal_code VARCHAR(20) NOT NULL,
    country_code VARCHAR(2) NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- ==============================================
-- PRODUCT SERVICE SCHEMA
-- ==============================================

-- Product categories
CREATE TABLE product_service.categories (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    parent_id UUID REFERENCES product_service.categories(id),
    name VARCHAR(255) NOT NULL,
    slug VARCHAR(255) UNIQUE NOT NULL,
    description TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    sort_order INTEGER DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Products
CREATE TABLE product_service.products (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    sku VARCHAR(100) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    slug VARCHAR(255) UNIQUE NOT NULL,
    description TEXT,
    base_price DECIMAL(12,2) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- ==============================================
-- SAMPLE DATA
-- ==============================================

-- Insert supported languages
INSERT INTO localization_service.languages (code, name, native_name, is_active) VALUES
('en', 'English', 'English', true),
('es', 'Spanish', 'Español', true),
('zh', 'Chinese', '中文', true);

-- Insert supported currencies  
INSERT INTO localization_service.currencies (code, name, symbol, decimal_places) VALUES
('USD', 'US Dollar', '$', 2),
('EUR', 'Euro', '€', 2),
('CNY', 'Chinese Yuan', '¥', 2);

-- Insert sample exchange rates
INSERT INTO localization_service.exchange_rates (from_currency, to_currency, rate, effective_date, source) VALUES
('USD', 'EUR', 0.85, NOW(), 'manual'),
('USD', 'CNY', 6.50, NOW(), 'manual'),
('EUR', 'USD', 1.18, NOW(), 'manual');

-- Insert sample categories
INSERT INTO product_service.categories (name, slug, description, is_active, sort_order) VALUES
('Electronics', 'electronics', 'Electronic devices and accessories', true, 1),
('Clothing', 'clothing', 'Fashion and apparel', true, 2),
('Books', 'books', 'Books and publications', true, 3);

-- ==============================================
-- INDEXES FOR PERFORMANCE
-- ==============================================

CREATE INDEX idx_users_email ON auth_service.users(email);
CREATE INDEX idx_users_active ON auth_service.users(is_active);
CREATE INDEX idx_refresh_tokens_user ON auth_service.refresh_tokens(user_id);
CREATE INDEX idx_profiles_user_id ON user_service.profiles(user_id);
CREATE INDEX idx_addresses_user_id ON user_service.addresses(user_id);
CREATE INDEX idx_products_active ON product_service.products(is_active);
CREATE INDEX idx_products_slug ON product_service.products(slug);
CREATE INDEX idx_categories_parent ON product_service.categories(parent_id);
