# Technical Context: Global E-commerce Platform

## Technology Stack

### Frontend Stack
- **Framework**: React.js (component-based UI)
- **Styling**: Tailwind CSS (utility-first CSS framework)
- **Internationalization**: react-i18next
- **HTTP Client**: Axios/Fetch API
- **Routing**: React Router
- **State Management**: React Context API or Zustand
- **Build**: Standard React build pipeline

### Backend Stack
- **Framework**: Python Flask (microservices)
- **ORM**: SQLAlchemy
- **Database Adapter**: psycopg2 (PostgreSQL)
- **API**: Flask-RESTful
- **Authentication**: Flask-JWT-Extended
- **Serialization**: marshmallow
- **Environment**: python-dotenv
- **HTTP Client**: requests library
- **Password Hashing**: werkzeug.security with bcrypt

### Database
- **Primary**: PostgreSQL
- **Extensions**: uuid-ossp for UUID generation
- **Data Types**: UUID for PKs, DECIMAL for money, JSONB for flexible data
- **Indexing**: Foreign keys and frequently queried columns

### Infrastructure
- **Containerization**: Docker
- **Orchestration**: Kubernetes
- **API Gateway**: Nginx (reverse proxy, load balancer, SSL termination)
- **Cloud**: Cloud-agnostic (AWS/GCP/Azure ready)

## Service Architecture

### Authentication Service
- **Routes**: /register, /login, /refresh, /forgot_password, /reset_password, /verify_email
- **Features**: JWT tokens, bcrypt hashing, email integration
- **Libraries**: Flask-JWT-Extended, werkzeug.security

### User Service
- **Routes**: /users/{id}, /users/{id}/addresses
- **Features**: Profile management, address management
- **Data**: User profiles, shipping/billing addresses

### Product Service (PIM)
- **Routes**: /products, /products/{id}, /categories
- **Features**: Product catalog, inventory, localization
- **Integration**: Calls Localization Service for currency conversion

### Order Service (OMS)
- **Routes**: /cart, /orders, /orders/{id}
- **Features**: Cart persistence, order creation, status management
- **Integration**: Product Service (inventory), Payment Service

### Payment Service
- **Routes**: /payments/process, /payments/webhook/{gateway_name}
- **Features**: Gateway integration, webhook handling
- **Gateways**: Stripe, PayPal, Alipay, WeChat Pay

### Localization Service
- **Routes**: /languages, /currencies, /convert_currency
- **Features**: Exchange rate management, currency conversion
- **Scheduling**: APScheduler for rate updates

### Admin Service
- **Routes**: /admin/* (products, users, orders, localization)
- **Features**: Administrative operations, RBAC
- **Integration**: Orchestrates calls to other services

## External Integrations

### Payment Gateways
- **Stripe**: Credit card processing, international payments
- **PayPal**: Online payment processing
- **Alipay/WeChat Pay**: Chinese market payments
- **Integration**: Official Python SDKs

### Third-Party APIs
- **Currency**: Open Exchange Rates / ECB API
- **Email**: SendGrid / Mailgun
- **Storage**: AWS S3 / Google Cloud Storage
- **CDN**: Cloudflare / AWS CloudFront

## Database Schema Highlights

### Key Tables
- `users`: UUID PK, email (unique), password_hash, roles
- `user_profiles`: User details, language/currency preferences
- `products`: UUID PK, SKU (unique), base_price (DECIMAL), inventory
- `product_localized_details`: Composite key (product_id, language_id)
- `orders`: UUID PK, user_id, total (DECIMAL), currency_id, status
- `exchange_rates`: Currency conversion rates with timestamps

### Data Type Standards
- **Primary Keys**: UUID using uuid_generate_v4()
- **Money**: DECIMAL for precision
- **Timestamps**: TIMESTAMP WITH TIME ZONE
- **Flexible Data**: JSONB for payment responses, attributes

## Development Environment
- **IDE**: VS Code, PyCharm
- **Containers**: Docker Desktop
- **Database Tools**: DBeaver, pgAdmin
- **API Testing**: Postman, Insomnia
- **Package Management**: npm/yarn (frontend), pip/pipenv/Poetry (backend)

## Performance & Monitoring
- **Caching**: Redis for API responses, CDN for static assets
- **Monitoring**: Prometheus, Grafana, OpenTelemetry
- **Logging**: Centralized logging with ELK Stack or Datadog
- **CI/CD**: GitHub Actions / GitLab CI with automated testing and deployment
