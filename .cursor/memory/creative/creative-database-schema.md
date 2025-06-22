# 🎨🎨🎨 ENTERING CREATIVE PHASE: DATABASE SCHEMA DESIGN 🎨🎨🎨

**Creative Phase ID**: CREATIVE-001
**Component**: All Services (System-wide)
**Type**: Data Model Architecture
**Priority**: CRITICAL
**Status**: IN PROGRESS

## Problem Statement

The global e-commerce platform requires a comprehensive database schema that supports:
- Multi-currency transactions with precision
- Multi-language product localization
- Complex user management with addresses and profiles
- Order lifecycle management from cart to fulfillment
- Secure payment processing with multiple gateways
- Real-time inventory tracking
- Administrative operations with audit trails
- Scalable microservices architecture

**Key Challenges**:
1. Maintaining data consistency across microservices
2. Supporting DECIMAL precision for multi-currency operations
3. Efficient localization without data duplication
4. Complex relationships between users, products, orders, and payments
5. UUID-based primary keys for distributed systems
6. Optimized queries for e-commerce search and filtering
7. Audit trails and temporal data tracking

## Requirements Analysis

### Functional Requirements
- **User Management**: Registration, profiles, multiple addresses, preferences
- **Product Catalog**: Products, categories, inventory, multi-language descriptions
- **Order Processing**: Shopping carts, orders, order items, status tracking
- **Payment Processing**: Transactions, multiple gateways, webhook tracking
- **Localization**: Languages, currencies, exchange rates, translations
- **Administrative**: User management, product management, order management

### Non-Functional Requirements
- **Performance**: Sub-second query responses for product searches
- **Scalability**: Support for millions of products and users
- **Consistency**: ACID compliance for financial transactions
- **Reliability**: Data integrity and referential consistency
- **Security**: Encrypted sensitive data, audit logging
- **Maintainability**: Clear schema design, proper indexing

## Database Schema Options Analysis

### Option 1: Single Database with Service Schemas
**Description**: One PostgreSQL database with separate schemas for each microservice

**Pros**:
- Simplified deployment and maintenance
- Easy cross-service queries and joins
- Strong consistency guarantees
- Reduced infrastructure complexity
- Better performance for complex queries

**Cons**:
- Tight coupling between services
- Potential single point of failure
- Scaling limitations
- Service boundaries less clear
- Deployment dependencies

**Complexity**: MEDIUM
**Implementation Time**: 2-3 weeks
**Scalability**: MEDIUM
**Maintainability**: HIGH

### Option 2: Database per Service (True Microservices)
**Description**: Separate PostgreSQL database for each microservice

**Pros**:
- True service independence
- Independent scaling and optimization
- Clear service boundaries
- Fault isolation
- Technology diversity possible

**Cons**:
- Complex cross-service queries
- Data consistency challenges
- Increased infrastructure complexity
- Network latency for joins
- Duplicate data management

**Complexity**: HIGH
**Implementation Time**: 4-5 weeks
**Scalability**: HIGH
**Maintainability**: MEDIUM

### Option 3: Hybrid Approach with Shared Core
**Description**: Shared database for core entities (users, products) with service-specific databases

**Pros**:
- Balance of independence and consistency
- Optimized for e-commerce patterns
- Reduced data duplication
- Clear service boundaries for business logic
- Good performance for core operations

**Cons**:
- Mixed architectural approach
- Complexity in data ownership
- Partial service independence
- Migration challenges
- Potential bottlenecks in shared core

**Complexity**: HIGH
**Implementation Time**: 3-4 weeks
**Scalability**: MEDIUM-HIGH
**Maintainability**: MEDIUM

## 🎨 CREATIVE CHECKPOINT: Schema Design Decision

**Recommended Approach**: **Option 1 - Single Database with Service Schemas**

**Rationale**:
1. **Simplicity**: For a new e-commerce platform, the operational complexity of multiple databases outweighs the benefits
2. **Development Speed**: Faster to implement and debug
3. **Data Consistency**: E-commerce requires strong consistency for inventory, orders, and payments
4. **Performance**: Complex queries (order with user, products, payments) are common in e-commerce
5. **Evolution Path**: Can migrate to Option 2 later as the system grows

**Risk Mitigation**:
- Use PostgreSQL schemas to maintain logical separation
- Implement service-level access controls
- Design for eventual migration to separate databases
- Use connection pooling to prevent resource contention

## Detailed Schema Design

### Core Database Structure

```sql
-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create schemas for logical separation
CREATE SCHEMA auth_service;
CREATE SCHEMA user_service;
CREATE SCHEMA product_service;
CREATE SCHEMA order_service;
CREATE SCHEMA payment_service;
CREATE SCHEMA localization_service;
CREATE SCHEMA admin_service;
```

### 1. Authentication Service Schema

```sql
-- auth_service.users: Core user authentication
CREATE TABLE auth_service.users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    email_verified BOOLEAN DEFAULT FALSE,
    password_hash VARCHAR(255) NOT NULL,
    status VARCHAR(50) DEFAULT 'active' CHECK (status IN ('active', 'suspended', 'deleted')),
    roles JSONB DEFAULT '["customer"]',
    last_login_at TIMESTAMP WITH TIME ZONE,
    failed_login_attempts INTEGER DEFAULT 0,
    locked_until TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- auth_service.user_sessions: JWT refresh token tracking
CREATE TABLE auth_service.user_sessions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES auth_service.users(id) ON DELETE CASCADE,
    refresh_token_hash VARCHAR(255) NOT NULL,
    expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    revoked_at TIMESTAMP WITH TIME ZONE
);

-- auth_service.password_resets: Password reset tokens
CREATE TABLE auth_service.password_resets (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES auth_service.users(id) ON DELETE CASCADE,
    token_hash VARCHAR(255) NOT NULL,
    expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
    used_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
```

### 2. Localization Service Schema

```sql
-- localization_service.languages: Supported languages
CREATE TABLE localization_service.languages (
    id SERIAL PRIMARY KEY,
    code VARCHAR(10) UNIQUE NOT NULL, -- ISO 639-1 codes (en, zh, es, etc.)
    name VARCHAR(100) NOT NULL,
    native_name VARCHAR(100) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    is_default BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- localization_service.currencies: Supported currencies
CREATE TABLE localization_service.currencies (
    id SERIAL PRIMARY KEY,
    code VARCHAR(3) UNIQUE NOT NULL, -- ISO 4217 codes (USD, CNY, EUR, etc.)
    name VARCHAR(100) NOT NULL,
    symbol VARCHAR(10) NOT NULL,
    decimal_places INTEGER DEFAULT 2,
    is_active BOOLEAN DEFAULT TRUE,
    is_default BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- localization_service.exchange_rates: Currency conversion rates
CREATE TABLE localization_service.exchange_rates (
    id SERIAL PRIMARY KEY,
    from_currency_id INTEGER NOT NULL REFERENCES localization_service.currencies(id),
    to_currency_id INTEGER NOT NULL REFERENCES localization_service.currencies(id),
    rate DECIMAL(18,8) NOT NULL, -- High precision for exchange rates
    effective_date DATE NOT NULL,
    source VARCHAR(100), -- API source (ECB, OpenExchangeRates, etc.)
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(from_currency_id, to_currency_id, effective_date)
);
```

### 3. User Service Schema

```sql
-- user_service.user_profiles: Extended user information
CREATE TABLE user_service.user_profiles (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID UNIQUE NOT NULL REFERENCES auth_service.users(id) ON DELETE CASCADE,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    phone VARCHAR(20),
    date_of_birth DATE,
    gender VARCHAR(20),
    preferred_language_id INTEGER REFERENCES localization_service.languages(id),
    preferred_currency_id INTEGER REFERENCES localization_service.currencies(id),
    marketing_emails_enabled BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- user_service.user_addresses: User shipping/billing addresses
CREATE TABLE user_service.user_addresses (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES auth_service.users(id) ON DELETE CASCADE,
    type VARCHAR(20) NOT NULL CHECK (type IN ('shipping', 'billing', 'both')),
    is_default BOOLEAN DEFAULT FALSE,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    company VARCHAR(100),
    address_line1 VARCHAR(255) NOT NULL,
    address_line2 VARCHAR(255),
    city VARCHAR(100) NOT NULL,
    state_province VARCHAR(100),
    postal_code VARCHAR(20) NOT NULL,
    country_code VARCHAR(2) NOT NULL, -- ISO 3166-1 alpha-2
    phone VARCHAR(20),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
```

### 4. Product Service Schema

```sql
-- product_service.categories: Product categories
CREATE TABLE product_service.categories (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    parent_id UUID REFERENCES product_service.categories(id),
    slug VARCHAR(255) UNIQUE NOT NULL,
    sort_order INTEGER DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- product_service.category_translations: Localized category names
CREATE TABLE product_service.category_translations (
    category_id UUID NOT NULL REFERENCES product_service.categories(id) ON DELETE CASCADE,
    language_id INTEGER NOT NULL REFERENCES localization_service.languages(id),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    meta_title VARCHAR(255),
    meta_description TEXT,
    PRIMARY KEY (category_id, language_id)
);

-- product_service.products: Core product information
CREATE TABLE product_service.products (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    sku VARCHAR(100) UNIQUE NOT NULL,
    category_id UUID REFERENCES product_service.categories(id),
    base_price DECIMAL(12,4) NOT NULL, -- Base price in default currency
    cost_price DECIMAL(12,4), -- Cost for profit calculation
    compare_at_price DECIMAL(12,4), -- Original price for discounts
    weight DECIMAL(8,3), -- Weight in kg
    dimensions JSONB, -- {"length": 10, "width": 5, "height": 3, "unit": "cm"}
    inventory_quantity INTEGER NOT NULL DEFAULT 0,
    inventory_policy VARCHAR(20) DEFAULT 'deny' CHECK (inventory_policy IN ('continue', 'deny')),
    requires_shipping BOOLEAN DEFAULT TRUE,
    is_taxable BOOLEAN DEFAULT TRUE,
    is_active BOOLEAN DEFAULT TRUE,
    is_featured BOOLEAN DEFAULT FALSE,
    tags JSONB DEFAULT '[]', -- ["electronics", "smartphone", "5g"]
    vendor VARCHAR(255),
    product_type VARCHAR(100),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- product_service.product_translations: Localized product content
CREATE TABLE product_service.product_translations (
    product_id UUID NOT NULL REFERENCES product_service.products(id) ON DELETE CASCADE,
    language_id INTEGER NOT NULL REFERENCES localization_service.languages(id),
    title VARCHAR(255) NOT NULL,
    description TEXT,
    short_description TEXT,
    meta_title VARCHAR(255),
    meta_description TEXT,
    handle VARCHAR(255), -- URL slug
    PRIMARY KEY (product_id, language_id)
);

-- product_service.product_images: Product images
CREATE TABLE product_service.product_images (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    product_id UUID NOT NULL REFERENCES product_service.products(id) ON DELETE CASCADE,
    url VARCHAR(500) NOT NULL,
    alt_text VARCHAR(255),
    sort_order INTEGER DEFAULT 0,
    is_primary BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- product_service.product_variants: Product variations (size, color, etc.)
CREATE TABLE product_service.product_variants (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    product_id UUID NOT NULL REFERENCES product_service.products(id) ON DELETE CASCADE,
    sku VARCHAR(100) UNIQUE NOT NULL,
    title VARCHAR(255) NOT NULL,
    price DECIMAL(12,4) NOT NULL,
    compare_at_price DECIMAL(12,4),
    cost_price DECIMAL(12,4),
    inventory_quantity INTEGER NOT NULL DEFAULT 0,
    weight DECIMAL(8,3),
    is_active BOOLEAN DEFAULT TRUE,
    option1 VARCHAR(255), -- e.g., "Red"
    option2 VARCHAR(255), -- e.g., "Large"
    option3 VARCHAR(255), -- e.g., "Cotton"
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
```

### 5. Order Service Schema

```sql
-- order_service.carts: Shopping cart persistence
CREATE TABLE order_service.carts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID UNIQUE REFERENCES auth_service.users(id) ON DELETE CASCADE,
    session_id VARCHAR(255), -- For guest carts
    expires_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CHECK (user_id IS NOT NULL OR session_id IS NOT NULL)
);

-- order_service.cart_items: Items in shopping cart
CREATE TABLE order_service.cart_items (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    cart_id UUID NOT NULL REFERENCES order_service.carts(id) ON DELETE CASCADE,
    product_id UUID NOT NULL REFERENCES product_service.products(id),
    variant_id UUID REFERENCES product_service.product_variants(id),
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    price_at_add DECIMAL(12,4) NOT NULL, -- Price when added to cart
    currency_id INTEGER NOT NULL REFERENCES localization_service.currencies(id),
    properties JSONB DEFAULT '{}', -- Custom properties, personalization
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(cart_id, product_id, variant_id)
);

-- order_service.orders: Customer orders
CREATE TABLE order_service.orders (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    order_number VARCHAR(50) UNIQUE NOT NULL, -- Human-readable order number
    user_id UUID REFERENCES auth_service.users(id),
    guest_email VARCHAR(255), -- For guest orders
    status VARCHAR(50) NOT NULL DEFAULT 'pending' CHECK (status IN (
        'pending', 'confirmed', 'processing', 'shipped', 'delivered', 
        'cancelled', 'refunded', 'partially_refunded'
    )),
    fulfillment_status VARCHAR(50) DEFAULT 'unfulfilled' CHECK (fulfillment_status IN (
        'unfulfilled', 'partial', 'fulfilled', 'restocked'
    )),
    payment_status VARCHAR(50) DEFAULT 'pending' CHECK (payment_status IN (
        'pending', 'authorized', 'paid', 'partially_paid', 'refunded', 
        'partially_refunded', 'voided'
    )),
    
    -- Pricing
    subtotal DECIMAL(12,4) NOT NULL,
    tax_amount DECIMAL(12,4) DEFAULT 0,
    shipping_amount DECIMAL(12,4) DEFAULT 0,
    discount_amount DECIMAL(12,4) DEFAULT 0,
    total_amount DECIMAL(12,4) NOT NULL,
    currency_id INTEGER NOT NULL REFERENCES localization_service.currencies(id),
    
    -- Addresses (snapshot at order time)
    billing_address JSONB NOT NULL,
    shipping_address JSONB NOT NULL,
    
    -- Metadata
    notes TEXT,
    tags JSONB DEFAULT '[]',
    source_name VARCHAR(100), -- web, mobile, admin
    
    -- Timestamps
    processed_at TIMESTAMP WITH TIME ZONE,
    shipped_at TIMESTAMP WITH TIME ZONE,
    delivered_at TIMESTAMP WITH TIME ZONE,
    cancelled_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    CHECK (user_id IS NOT NULL OR guest_email IS NOT NULL)
);

-- order_service.order_items: Items in an order
CREATE TABLE order_service.order_items (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    order_id UUID NOT NULL REFERENCES order_service.orders(id) ON DELETE CASCADE,
    product_id UUID NOT NULL REFERENCES product_service.products(id),
    variant_id UUID REFERENCES product_service.product_variants(id),
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    price_per_unit DECIMAL(12,4) NOT NULL, -- Price at order time
    total_price DECIMAL(12,4) NOT NULL,
    currency_id INTEGER NOT NULL REFERENCES localization_service.currencies(id),
    
    -- Product snapshot at order time
    product_title VARCHAR(255) NOT NULL,
    product_variant_title VARCHAR(255),
    product_sku VARCHAR(100) NOT NULL,
    
    -- Properties and customizations
    properties JSONB DEFAULT '{}',
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
```

### 6. Payment Service Schema

```sql
-- payment_service.payment_methods: Available payment methods
CREATE TABLE payment_service.payment_methods (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) NOT NULL,
    type VARCHAR(50) NOT NULL, -- 'credit_card', 'paypal', 'alipay', 'wechat_pay'
    gateway VARCHAR(50) NOT NULL, -- 'stripe', 'paypal', 'alipay'
    is_active BOOLEAN DEFAULT TRUE,
    supported_currencies JSONB NOT NULL, -- ["USD", "EUR", "CNY"]
    config JSONB DEFAULT '{}', -- Gateway-specific configuration
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- payment_service.transactions: Payment transactions
CREATE TABLE payment_service.transactions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    order_id UUID NOT NULL REFERENCES order_service.orders(id),
    payment_method_id UUID NOT NULL REFERENCES payment_service.payment_methods(id),
    
    -- Transaction details
    type VARCHAR(50) NOT NULL CHECK (type IN ('payment', 'refund', 'partial_refund')),
    status VARCHAR(50) NOT NULL CHECK (status IN (
        'pending', 'processing', 'success', 'failed', 'cancelled', 'refunded'
    )),
    amount DECIMAL(12,4) NOT NULL,
    currency_id INTEGER NOT NULL REFERENCES localization_service.currencies(id),
    
    -- Gateway information
    gateway_transaction_id VARCHAR(255),
    gateway_status VARCHAR(100),
    gateway_response JSONB, -- Full gateway response
    
    -- Metadata
    reference_number VARCHAR(100),
    failure_reason TEXT,
    processed_at TIMESTAMP WITH TIME ZONE,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- payment_service.webhooks: Webhook event tracking
CREATE TABLE payment_service.webhooks (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    gateway VARCHAR(50) NOT NULL,
    event_type VARCHAR(100) NOT NULL,
    event_id VARCHAR(255), -- Gateway's event ID
    transaction_id UUID REFERENCES payment_service.transactions(id),
    payload JSONB NOT NULL,
    processed BOOLEAN DEFAULT FALSE,
    processed_at TIMESTAMP WITH TIME ZONE,
    error_message TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
```

### 7. Admin Service Schema

```sql
-- admin_service.audit_logs: System audit trail
CREATE TABLE admin_service.audit_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES auth_service.users(id),
    action VARCHAR(100) NOT NULL, -- 'create', 'update', 'delete', 'login', etc.
    resource_type VARCHAR(100) NOT NULL, -- 'user', 'product', 'order', etc.
    resource_id UUID,
    old_values JSONB,
    new_values JSONB,
    ip_address INET,
    user_agent TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- admin_service.system_settings: System configuration
CREATE TABLE admin_service.system_settings (
    key VARCHAR(255) PRIMARY KEY,
    value JSONB NOT NULL,
    description TEXT,
    updated_by UUID REFERENCES auth_service.users(id),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
```

## Database Indexes and Optimization

```sql
-- Authentication Service Indexes
CREATE INDEX idx_users_email ON auth_service.users(email);
CREATE INDEX idx_users_status ON auth_service.users(status);
CREATE INDEX idx_user_sessions_user_id ON auth_service.user_sessions(user_id);
CREATE INDEX idx_user_sessions_expires_at ON auth_service.user_sessions(expires_at);

-- User Service Indexes
CREATE INDEX idx_user_profiles_user_id ON user_service.user_profiles(user_id);
CREATE INDEX idx_user_addresses_user_id ON user_service.user_addresses(user_id);
CREATE INDEX idx_user_addresses_type ON user_service.user_addresses(type);

-- Product Service Indexes
CREATE INDEX idx_products_sku ON product_service.products(sku);
CREATE INDEX idx_products_category_id ON product_service.products(category_id);
CREATE INDEX idx_products_is_active ON product_service.products(is_active);
CREATE INDEX idx_products_is_featured ON product_service.products(is_featured);
CREATE INDEX idx_products_created_at ON product_service.products(created_at);
CREATE INDEX idx_product_variants_product_id ON product_service.product_variants(product_id);
CREATE INDEX idx_product_variants_sku ON product_service.product_variants(sku);
CREATE INDEX idx_product_images_product_id ON product_service.product_images(product_id);

-- Order Service Indexes
CREATE INDEX idx_carts_user_id ON order_service.carts(user_id);
CREATE INDEX idx_carts_session_id ON order_service.carts(session_id);
CREATE INDEX idx_cart_items_cart_id ON order_service.cart_items(cart_id);
CREATE INDEX idx_orders_user_id ON order_service.orders(user_id);
CREATE INDEX idx_orders_status ON order_service.orders(status);
CREATE INDEX idx_orders_created_at ON order_service.orders(created_at);
CREATE INDEX idx_orders_order_number ON order_service.orders(order_number);
CREATE INDEX idx_order_items_order_id ON order_service.order_items(order_id);
CREATE INDEX idx_order_items_product_id ON order_service.order_items(product_id);

-- Payment Service Indexes
CREATE INDEX idx_transactions_order_id ON payment_service.transactions(order_id);
CREATE INDEX idx_transactions_status ON payment_service.transactions(status);
CREATE INDEX idx_transactions_gateway_transaction_id ON payment_service.transactions(gateway_transaction_id);
CREATE INDEX idx_webhooks_gateway ON payment_service.webhooks(gateway);
CREATE INDEX idx_webhooks_processed ON payment_service.webhooks(processed);

-- Localization Service Indexes
CREATE INDEX idx_exchange_rates_from_to_date ON localization_service.exchange_rates(from_currency_id, to_currency_id, effective_date);

-- Admin Service Indexes
CREATE INDEX idx_audit_logs_user_id ON admin_service.audit_logs(user_id);
CREATE INDEX idx_audit_logs_resource ON admin_service.audit_logs(resource_type, resource_id);
CREATE INDEX idx_audit_logs_created_at ON admin_service.audit_logs(created_at);
```

## Data Validation and Constraints

```sql
-- Additional constraints for data integrity
ALTER TABLE localization_service.currencies 
ADD CONSTRAINT chk_currencies_single_default 
CHECK ((SELECT COUNT(*) FROM localization_service.currencies WHERE is_default = TRUE) <= 1);

ALTER TABLE localization_service.languages 
ADD CONSTRAINT chk_languages_single_default 
CHECK ((SELECT COUNT(*) FROM localization_service.languages WHERE is_default = TRUE) <= 1);

-- Ensure cart items have valid product references
ALTER TABLE order_service.cart_items 
ADD CONSTRAINT chk_cart_items_variant_product 
CHECK (variant_id IS NULL OR EXISTS (
    SELECT 1 FROM product_service.product_variants pv 
    WHERE pv.id = variant_id AND pv.product_id = cart_items.product_id
));

-- Ensure order totals are calculated correctly
ALTER TABLE order_service.orders 
ADD CONSTRAINT chk_orders_total_calculation 
CHECK (total_amount = subtotal + tax_amount + shipping_amount - discount_amount);
```

## Implementation Guidelines

### 1. Migration Strategy
- Use Alembic for database migrations
- Create migration scripts for each schema
- Test migrations on staging data
- Implement rollback procedures

### 2. Data Seeding
- Create seed data for languages and currencies
- Add default system settings
- Create sample products for testing
- Set up payment method configurations

### 3. Performance Optimization
- Implement connection pooling (PgBouncer)
- Use read replicas for heavy queries
- Implement query caching where appropriate
- Monitor slow queries and optimize

### 4. Security Measures
- Use parameterized queries to prevent SQL injection
- Implement row-level security where needed
- Encrypt sensitive data at rest
- Audit all data access

### 5. Backup and Recovery
- Implement automated backups
- Test recovery procedures
- Document disaster recovery plans
- Monitor backup integrity

## Verification Against Requirements

✅ **Requirements Met**:
- [x] Multi-currency support with DECIMAL precision
- [x] Multi-language localization structure
- [x] Complex user management with addresses
- [x] Complete order lifecycle management
- [x] Secure payment processing structure
- [x] Real-time inventory tracking
- [x] Administrative operations with audit trails
- [x] UUID-based primary keys for scalability
- [x] Proper indexing for performance
- [x] Data integrity constraints

✅ **Technical Feasibility**: HIGH - PostgreSQL fully supports all required features
✅ **Risk Assessment**: LOW - Well-established patterns and technologies

🎨🎨🎨 EXITING CREATIVE PHASE - DATABASE SCHEMA DESIGN COMPLETE 🎨🎨🎨

**Decision**: Single database with service schemas approach
**Implementation**: Comprehensive schema with all required tables, relationships, and optimizations
**Next Steps**: Update tasks.md with schema decisions and proceed to API Gateway architecture design
