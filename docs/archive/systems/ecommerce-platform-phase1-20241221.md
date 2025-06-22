# SYSTEM ARCHIVE: Global E-commerce Platform - Phase 1

## Metadata
- **Complexity**: Level 4 (Complex System)
- **Type**: Multi-Service E-commerce Platform
- **Date Completed**: December 21, 2024
- **Phase**: Phase 1 - Core Backend Services
- **Related Tasks**: ECOMM-SYS Phase 1 Implementation
- **Archive ID**: ARCH-ECOMM-PHASE1-20241221

## System Overview

### System Purpose and Scope
Successfully implemented the foundational core of a scalable, multi-currency, multi-language e-commerce platform using microservices architecture. Phase 1 established the critical authentication and user management systems that serve as the security foundation for all subsequent services.

**Business Context**: Global e-commerce platform supporting multi-currency transactions, multiple payment gateways, and multi-language support across web and mobile interfaces.

### System Architecture
- **Pattern**: Microservices architecture with shared database
- **Database Strategy**: Single PostgreSQL database with service-specific schemas
- **Authentication**: JWT-based inter-service authentication
- **API Design**: RESTful APIs with consistent error handling
- **Security**: Production-grade security from first implementation

### Key Components Implemented
1. **Authentication Service** (`backend/auth-service/app.py`)
   - Complete JWT-based authentication system
   - Email verification and password reset
   - Rate limiting and account lockout protection
   - Comprehensive security features

2. **User Service** (`backend/user-service/app.py`)
   - User profile management system
   - Multiple address management (billing/shipping)
   - Primary address functionality
   - Integration with authentication service

3. **Database Infrastructure** (`database/init.sql`)
   - Comprehensive PostgreSQL schema
   - Service-specific schemas for all 7 planned microservices
   - Optimized indexing and relationships
   - Multi-currency and multi-language support

### Integration Points
- **Internal**: JWT token validation between auth-service and user-service
- **External**: SMTP email service integration (configurable)
- **Database**: All services connect to PostgreSQL with service-specific schemas
- **Future**: API Gateway integration points established

### Technology Stack
- **Backend Framework**: Python Flask 3.1.1 + Flask-RESTful + Flask-JWT-Extended
- **Database**: PostgreSQL 17 with uuid-ossp and pgcrypto extensions
- **Validation**: Marshmallow 4.0.0 for input validation and serialization
- **Security**: Werkzeug security, JWT tokens, rate limiting
- **Development**: Python virtual environments, comprehensive logging
- **Testing**: Integration testing framework with requests library
- **Containerization**: Docker with production-ready configurations

### Deployment Environment
- **Local Development**: Python virtual environments with PostgreSQL
- **Containerization**: Docker containers for all services
- **Orchestration**: Docker Compose with service networking
- **Database**: PostgreSQL with comprehensive schema and sample data

## Requirements and Design Documentation

### Business Requirements
1. **Secure User Authentication**: Multi-layered security with email verification
2. **User Profile Management**: Comprehensive profile and address management
3. **Scalable Architecture**: Microservices foundation for global scale
4. **Multi-Language Support**: Database structure supporting internationalization
5. **Multi-Currency Support**: Database structure supporting global commerce
6. **Production Readiness**: Enterprise-grade security and error handling

### Functional Requirements
1. **User Registration**: Email-based registration with verification
2. **User Login**: Secure login with JWT token generation
3. **Password Management**: Secure password reset functionality
4. **Profile Management**: User profile CRUD operations
5. **Address Management**: Multiple address support with primary designation
6. **Token Management**: JWT token refresh and blacklisting
7. **Security Features**: Rate limiting, account lockout, brute force protection

### Non-Functional Requirements
1. **Security**: Production-grade security features implemented
2. **Performance**: Optimized database queries with proper indexing
3. **Scalability**: Microservices architecture supporting horizontal scaling
4. **Maintainability**: Comprehensive error handling and logging
5. **Reliability**: Database integrity with proper constraints and validation
6. **Usability**: RESTful API design with consistent response formats

### Architecture Decision Records
1. **ADR-001: Single Database with Service Schemas**
   - **Decision**: Use single PostgreSQL database with service-specific schemas
   - **Rationale**: Balances microservices benefits with relationship simplicity
   - **Status**: Implemented and validated

2. **ADR-002: JWT-Based Authentication**
   - **Decision**: Use Flask-JWT-Extended with refresh tokens and blacklisting
   - **Rationale**: Provides stateless authentication with advanced security features
   - **Status**: Implemented with comprehensive security

3. **ADR-003: Security-First Implementation**
   - **Decision**: Implement production security features from the beginning
   - **Rationale**: Prevents security technical debt and ensures production readiness
   - **Status**: Implemented with rate limiting, account lockout, email verification

### Design Patterns Used
1. **Repository Pattern**: Database access through SQLAlchemy ORM
2. **Factory Pattern**: Flask application and extension initialization
3. **Decorator Pattern**: JWT authentication decorators for protected endpoints
4. **Strategy Pattern**: Rate limiting implementation with configurable strategies
5. **Observer Pattern**: Token blacklisting and refresh token management

### Design Constraints
1. **Technology Stack**: Python Flask ecosystem for consistency
2. **Database**: PostgreSQL for ACID compliance and JSON support
3. **Security**: Must support enterprise-grade security requirements
4. **Scalability**: Must support horizontal scaling through containerization
5. **Maintainability**: Comprehensive error handling and logging required

## Implementation Documentation

### Component Implementation Details

#### Authentication Service (`backend/auth-service/app.py`)
- **Purpose**: Centralized authentication and security services
- **Implementation Approach**: Flask-JWT-Extended with comprehensive security layers
- **Key Classes/Modules**:
  - `User` model with comprehensive security fields
  - `RefreshToken` model for token management
  - `RegisterResource` with email verification
  - `LoginResource` with security protection
  - `PasswordResetResource` with secure token handling
- **Dependencies**: PostgreSQL, SMTP service, JWT library
- **Special Considerations**: Rate limiting, account lockout, token blacklisting

#### User Service (`backend/user-service/app.py`)
- **Purpose**: User profile and address management
- **Implementation Approach**: RESTful API with JWT integration
- **Key Classes/Modules**:
  - `Profile` model for user information
  - `Address` model for address management
  - `ProfileResource` with CRUD operations
  - `AddressListResource` with address management
- **Dependencies**: Authentication service for JWT validation
- **Special Considerations**: Multiple address types, primary address logic

#### Database Infrastructure (`database/init.sql`)
- **Purpose**: Comprehensive data foundation for all services
- **Implementation Approach**: Service-specific schemas with optimized relationships
- **Key Components**:
  - Authentication service schema with security features
  - User service schema with profile and address tables
  - Localization service schema for multi-currency/language support
  - Product, order, payment service schemas (ready for implementation)
- **Dependencies**: PostgreSQL with uuid-ossp extension
- **Special Considerations**: UUID primary keys, DECIMAL currency precision, comprehensive indexing

### Key Files and Components Affected
**From Implementation Tasks:**
- `backend/auth-service/app.py`: Complete authentication system
- `backend/auth-service/requirements.txt`: Python dependencies
- `backend/auth-service/Dockerfile`: Container configuration
- `backend/user-service/app.py`: User management system
- `backend/user-service/requirements.txt`: User service dependencies
- `database/init.sql`: Comprehensive database schema
- `docker-compose.yml`: Multi-service orchestration
- `test_services.py`: Integration testing suite

### Algorithms and Complex Logic
1. **JWT Token Management**: Refresh token rotation with blacklisting
2. **Rate Limiting Algorithm**: Time-window based request counting
3. **Account Lockout Logic**: Progressive lockout with automatic reset
4. **Password Security**: Secure hashing with Werkzeug security
5. **Email Verification**: Secure token generation and validation

### Third-Party Integrations
1. **Flask Framework**: Web application framework
2. **SQLAlchemy**: Database ORM with PostgreSQL
3. **Flask-JWT-Extended**: JWT token management
4. **Marshmallow**: Input validation and serialization
5. **SMTP Libraries**: Email service integration
6. **PostgreSQL**: Database engine with extensions

### Configuration Parameters
**Authentication Service:**
- `DATABASE_URL`: PostgreSQL connection string
- `JWT_SECRET_KEY`: JWT token signing key
- `SMTP_SERVER`: Email server configuration
- `FLASK_ENV`: Environment (development/production)

**User Service:**
- `DATABASE_URL`: PostgreSQL connection string
- `JWT_SECRET_KEY`: JWT token verification key
- `FLASK_ENV`: Environment configuration

### Build and Packaging Details
1. **Python Virtual Environments**: Isolated dependency management
2. **Requirements.txt**: Pinned dependency versions
3. **Docker Containers**: Production-ready containerization
4. **Docker Compose**: Multi-service orchestration

## API Documentation

### API Overview
Two main services providing RESTful APIs:
1. **Authentication API**: User authentication and security services
2. **User Management API**: Profile and address management services

### Authentication Service API Endpoints

#### User Registration
- **URL/Path**: `/register`
- **Method**: POST
- **Purpose**: Register new user with email verification
- **Request Format**: 
  ```json
  {
    "email": "user@example.com",
    "password": "securepassword123",
    "confirm_password": "securepassword123"
  }
  ```
- **Response Format**: 
  ```json
  {
    "message": "User registered successfully. Please check your email for verification.",
    "user_id": "uuid"
  }
  ```
- **Error Codes**: 400 (validation), 409 (user exists), 500 (server error)
- **Security**: Rate limited (3 attempts per 5 minutes)

#### User Login
- **URL/Path**: `/login`
- **Method**: POST
- **Purpose**: Authenticate user and generate JWT tokens
- **Request Format**: 
  ```json
  {
    "email": "user@example.com",
    "password": "securepassword123"
  }
  ```
- **Response Format**: 
  ```json
  {
    "access_token": "jwt_token",
    "refresh_token": "refresh_token",
    "user": {
      "id": "uuid",
      "email": "user@example.com",
      "email_verified": true
    }
  }
  ```
- **Error Codes**: 401 (invalid credentials), 403 (email not verified), 423 (account locked)
- **Security**: Rate limited (5 attempts per 5 minutes), account lockout after 5 failures

#### Additional Authentication Endpoints
- `/logout` (POST): Logout and blacklist token
- `/refresh` (POST): Refresh access token
- `/verify-email` (POST): Verify email address
- `/password-reset-request` (POST): Request password reset
- `/password-reset` (POST): Reset password with token
- `/protected` (GET): Test protected endpoint
- `/health` (GET): Service health check

### User Service API Endpoints

#### Profile Management
- **URL/Path**: `/profile`
- **Method**: GET/PUT
- **Purpose**: Manage user profile information
- **Authentication**: JWT token required
- **Request Format (PUT)**: 
  ```json
  {
    "first_name": "John",
    "last_name": "Doe",
    "phone": "+1234567890",
    "preferred_language": "en",
    "preferred_currency": "USD"
  }
  ```

#### Address Management
- **URL/Path**: `/addresses`
- **Method**: GET/POST
- **Purpose**: Manage user addresses
- **Authentication**: JWT token required
- **Request Format (POST)**: 
  ```json
  {
    "type": "shipping",
    "first_name": "John",
    "last_name": "Doe",
    "address_line_1": "123 Main St",
    "city": "New York",
    "postal_code": "10001",
    "country_code": "US"
  }
  ```

### API Authentication
- **Method**: JWT Bearer token authentication
- **Header**: `Authorization: Bearer <jwt_token>`
- **Token Expiration**: 1 hour for access tokens, 30 days for refresh tokens
- **Token Refresh**: Available through `/refresh` endpoint

### API Versioning Strategy
- **Current Version**: v1 (implicit)
- **Future Versioning**: URL-based versioning (`/api/v2/`)
- **Migration Strategy**: Backward compatibility during transition periods

## Data Model and Schema Documentation

### Data Model Overview
Comprehensive relational data model supporting microservices architecture with service-specific schemas within a single PostgreSQL database.

### Database Schema

#### Authentication Service Schema (`auth_service`)
```sql
-- Users table
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

-- Refresh tokens table
CREATE TABLE auth_service.refresh_tokens (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES auth_service.users(id) ON DELETE CASCADE,
    token_hash VARCHAR(255) NOT NULL,
    expires_at TIMESTAMPTZ NOT NULL,
    is_revoked BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
```

#### User Service Schema (`user_service`)
```sql
-- User profiles table
CREATE TABLE user_service.profiles (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID UNIQUE NOT NULL, -- References auth_service.users.id
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    phone VARCHAR(20),
    preferred_language VARCHAR(10) DEFAULT 'en',
    preferred_currency VARCHAR(3) DEFAULT 'USD',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- User addresses table
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
```

#### Localization Service Schema (`localization_service`)
```sql
-- Languages table
CREATE TABLE localization_service.languages (
    code VARCHAR(10) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    native_name VARCHAR(100) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Currencies table
CREATE TABLE localization_service.currencies (
    code VARCHAR(3) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    symbol VARCHAR(10) NOT NULL,
    decimal_places INTEGER DEFAULT 2,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Exchange rates table
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
```

### Data Dictionary
- **UUID Fields**: All primary keys use UUID for global uniqueness
- **Email Fields**: Validated email addresses with uniqueness constraints
- **Password Fields**: Hashed using Werkzeug security with salt
- **Currency Fields**: DECIMAL precision for accurate financial calculations
- **Timestamp Fields**: UTC timestamps with timezone awareness
- **Language Codes**: ISO standard language codes (en, es, zh)
- **Currency Codes**: ISO 4217 currency codes (USD, EUR, CNY)
- **Country Codes**: ISO 3166-1 alpha-2 country codes

### Data Validation Rules
1. **Email Validation**: RFC-compliant email validation
2. **Password Strength**: Minimum 8 characters required
3. **Currency Precision**: DECIMAL(12,2) for money values
4. **Foreign Key Integrity**: Enforced referential integrity
5. **Check Constraints**: Enumerated values for address types
6. **Unique Constraints**: Email uniqueness, user-language combinations

### Data Migration Procedures
1. **Schema Versioning**: SQL migration scripts with version control
2. **Data Preservation**: Non-destructive migrations with rollback capability
3. **Index Management**: Concurrent index creation for zero-downtime
4. **Constraint Addition**: Gradual constraint enforcement

## Security Documentation

### Security Architecture
Multi-layered security approach with defense in depth:
1. **Authentication Layer**: JWT-based stateless authentication
2. **Authorization Layer**: Token validation and user permissions
3. **Network Layer**: Rate limiting and request filtering
4. **Data Layer**: Encrypted storage and secure database access
5. **Application Layer**: Input validation and secure coding practices

### Authentication and Authorization
1. **JWT Tokens**: Stateless authentication with secure signing
2. **Refresh Tokens**: Secure token rotation with expiration
3. **Token Blacklisting**: Revoked token tracking for immediate invalidation
4. **Account Lockout**: Progressive lockout after failed attempts
5. **Email Verification**: Required email verification for account activation
6. **Password Security**: Secure hashing with Werkzeug security

### Data Protection Measures
1. **Password Hashing**: Salted password hashing with Werkzeug
2. **Token Security**: Secure JWT signing with configurable secrets
3. **Database Security**: Parameterized queries preventing SQL injection
4. **Input Validation**: Comprehensive validation with Marshmallow
5. **Error Handling**: Secure error messages without information disclosure

### Security Controls
1. **Rate Limiting**: Configurable rate limits on authentication endpoints
2. **CORS Configuration**: Secure cross-origin resource sharing
3. **Request Validation**: Comprehensive input validation and sanitization
4. **Logging**: Security event logging for audit trails
5. **Environment Configuration**: Secure configuration management

### Vulnerability Management
1. **Dependency Management**: Pinned dependency versions with security updates
2. **Code Review**: Security-focused code review processes
3. **Input Validation**: Defense against injection attacks
4. **Authentication Security**: Protection against brute force and timing attacks

### Security Testing Results
1. **Authentication Testing**: All authentication flows tested
2. **Rate Limiting Testing**: Rate limits validated and working
3. **Input Validation Testing**: All inputs validated against injection
4. **Token Security Testing**: JWT token handling tested

### Compliance Considerations
1. **Data Protection**: User data protection with secure storage
2. **Privacy**: User consent and data handling transparency
3. **Security Standards**: Industry-standard security practices
4. **Audit Trail**: Comprehensive logging for compliance requirements

## Testing Documentation

### Test Strategy
Comprehensive testing approach covering:
1. **Unit Testing**: Individual component testing
2. **Integration Testing**: Service-to-service communication testing
3. **Security Testing**: Authentication and authorization testing
4. **API Testing**: Complete API endpoint testing
5. **Database Testing**: Data integrity and relationship testing

### Test Cases
**Authentication Service Tests:**
1. User registration with email verification
2. User login with valid/invalid credentials
3. Password reset functionality
4. Token refresh and blacklisting
5. Rate limiting enforcement
6. Account lockout mechanism

**User Service Tests:**
1. Profile management (CRUD operations)
2. Address management (multiple addresses)
3. JWT token validation
4. Input validation and error handling

### Automated Tests
**Integration Test Suite** (`test_services.py`):
- Service health checks
- User registration flow
- Authentication flow
- Profile management testing
- Cross-service communication validation

### Known Issues and Limitations
1. **Email Service**: Requires external SMTP configuration for production
2. **Redis Integration**: Token blacklisting uses in-memory storage (needs Redis for production scaling)
3. **Rate Limiting**: Simple in-memory implementation (needs distributed solution for scaling)

## Deployment Documentation

### Deployment Architecture
**Development Environment:**
- Local PostgreSQL instance
- Python virtual environments
- Flask development servers

**Production-Ready Configuration:**
- Docker containers for all services
- PostgreSQL database with production configuration
- Nginx API gateway (validated configuration)
- Docker Compose orchestration

### Environment Configuration
**Development:**
```bash
DATABASE_URL=postgresql://ecommerce_user:ecommerce_pass@localhost:5432/ecommerce_db
JWT_SECRET_KEY=development-secret-key
FLASK_ENV=development
```

**Production:**
```bash
DATABASE_URL=postgresql://user:pass@db-host:5432/ecommerce_db
JWT_SECRET_KEY=secure-production-key
FLASK_ENV=production
SMTP_SERVER=production-smtp-server
```

### Deployment Procedures
1. **Database Setup**: Create PostgreSQL database and run init.sql
2. **Service Deployment**: Build and deploy Docker containers
3. **Configuration**: Set environment variables for production
4. **Health Checks**: Verify all services are operational
5. **Integration Testing**: Run full integration test suite

### Configuration Management
- Environment-specific configuration files
- Docker environment variable injection
- Secure secret management for production

## Operational Documentation

### Operating Procedures
1. **Service Monitoring**: Health endpoint monitoring
2. **Log Monitoring**: Application and error log monitoring
3. **Database Maintenance**: Regular backup and maintenance procedures
4. **Security Monitoring**: Authentication and security event monitoring

### Maintenance Tasks
1. **Database Cleanup**: Expired token cleanup
2. **Log Rotation**: Application log management
3. **Security Updates**: Regular dependency updates
4. **Performance Monitoring**: Database and application performance

### Troubleshooting Guide
**Common Issues:**
1. **Database Connection**: Check DATABASE_URL and PostgreSQL service
2. **JWT Token Issues**: Verify JWT_SECRET_KEY configuration
3. **Email Verification**: Check SMTP configuration
4. **Rate Limiting**: Monitor rate limit logs

## Project History and Learnings

### Project Timeline
- **Week 1**: Technology validation and architecture setup
- **Week 2**: Authentication service implementation
- **Week 3**: User service implementation and integration
- **Completion**: Phase 1 fully implemented with production-ready features

### Key Decisions and Rationale
1. **Single Database Approach**: Simplified relationships while maintaining service separation
2. **Security-First Implementation**: Prevented technical debt and ensured production readiness
3. **Comprehensive Schema Design**: Upfront investment for all services reduced future complexity

### Challenges and Solutions
1. **Authentication Complexity**: Implemented comprehensive security features beyond basic requirements
2. **Database Design**: Balanced microservices principles with relationship management
3. **Technology Integration**: Systematic validation prevented integration issues

### Lessons Learned
1. **Technology Validation Gates Essential**: Prevented all technical risks
2. **Security-First Approach Delivers Value**: Production-ready systems from first implementation
3. **Creative Phase Investment Pays Off**: Upfront design dramatically improved implementation quality

### Performance Against Objectives
- **Timeline**: On schedule with quality improvements
- **Quality**: Exceeded expectations with production-ready features
- **Security**: Implemented enterprise-grade security from the beginning
- **Architecture**: Validated microservices approach with working implementation

### Future Enhancements
1. **Redis Integration**: Distributed token blacklisting and rate limiting
2. **Production Email Service**: SendGrid or AWS SES integration
3. **Enhanced Monitoring**: Application performance monitoring
4. **Additional Security**: OAuth integration, 2FA support
5. **API Gateway**: Complete Nginx API gateway implementation

## Cross-References
- **Reflection Document**: `.cursor/memory/reflection.md`
- **Tasks Documentation**: `.cursor/memory/tasks.md`
- **Progress Tracking**: `.cursor/memory/progress.md`
- **Creative Phase Documents**: `.cursor/memory/creative/`
- **Source Code**: `backend/auth-service/`, `backend/user-service/`
- **Database Schema**: `database/init.sql`
- **Integration Tests**: `test_services.py`

---

**Archive Created**: December 21, 2024  
**Next Phase**: Product Service and Localization Service Implementation  
**Status**: Phase 1 Complete and Archived  
