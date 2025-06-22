## Technical Specification: Global E-commerce Platform

**Version:** 1.1
**Date:** June 21, 2025
**Prepared By:** AI Assistant

-----

### 1\. Introduction

This document outlines the detailed technical specifications for the development of a multi-currency, multi-language e-commerce platform. It specifies the chosen technologies and their implementation for key functionalities, ensuring a scalable, secure, and maintainable system capable of serving a global user base.

### 2\. Technology Stack

  * **Frontend:** React.js, Tailwind CSS
  * **Backend:** Python Flask
  * **Database:** PostgreSQL
  * **API Gateway/Load Balancer:** Nginx (or cloud-native equivalent)
  * **Containerization:** Docker
  * **Orchestration:** Kubernetes
  * **Cloud Platform:** Cloud-agnostic design (e.g., AWS, GCP, Azure for deployment)

### 3\. Architecture Overview

The system will adhere to a **microservices architecture**, where distinct business capabilities are encapsulated into independent, deployable Flask services. The frontend (React) will consume APIs exposed via an API Gateway. PostgreSQL will serve as the persistent data store across services.

```mermaid
graph TD
    User -->|Web Browser (HTTP/S)| ReactApp[React + Tailwind CSS Frontend]
    ReactApp -->|REST API Calls| APIGateway[API Gateway / Load Balancer]

    subgraph Backend Services (Python Flask Microservices)
        APIGateway --> AuthSvc(Authentication Service)
        APIGateway --> UserSvc(User Service)
        APIGateway --> ProductSvc(Product Service PIM)
        APIGateway --> OrderSvc(Order Service OMS)
        APIGateway --> PaymentSvc(Payment Service)
        APIGateway --> LocalizationSvc(Localization Service)
        APIGateway --> AdminSvc(Admin Service)
    end

    subgraph Data Layer
        AuthSvc --- DB(PostgreSQL Database)
        UserSvc --- DB
        ProductSvc --- DB
        OrderSvc --- DB
        PaymentSvc --- DB
        LocalizationSvc --- DB
    end

    AuthSvc --> EmailService(Email Service)
    ProductSvc --> LocalizationSvc
    OrderSvc --> PaymentSvc
    LocalizationSvc --> CurrencyAPI(External Currency Exchange API)
    PaymentSvc --> PaymentGateway(External Payment Gateways)
    ProductSvc --> CloudStorage(Cloud Storage for Media)
    ReactApp --> CDN(CDN for Static Assets)

    AdminSvc --(Admin Functions)--> ProductSvc
    AdminSvc --(Admin Functions)--> OrderSvc
    AdminSvc --(Admin Functions)--> UserSvc
    AdminSvc --(Admin Functions)--> LocalizationSvc
```

### 4\. Component-Specific Technical Details

#### 4.1. Frontend (React.js with Tailwind CSS)

  * **Framework/Libraries**:
      * **React.js**: For building the component-based UI.
      * **Tailwind CSS**: For utility-first styling and responsive design. Will load via CDN for development, potentially bundled for production.
      * **`react-i18next`**: For internationalization and managing translated strings.
      * **Axios / Fetch API**: For making HTTP requests to backend services.
      * **React Router (or similar)**: For client-side routing within the SPA.
      * **State Management**: React Context API or a lightweight library like Zustand for application state.
  * **Localization Implementation**:
      * User's selected language will be stored in local storage or a cookie.
      * The `Accept-Language` header will be sent with all API requests, allowing backend services to return localized data.
      * UI components will use `react-i18next` hooks/components to display translated text.
  * **Multi-Currency Display**:
      * User's selected currency will be stored in local storage/cookie.
      * All price displays will dynamically format values based on the selected currency, potentially including the converted amount received from the backend.
      * `Intl.NumberFormat` will be used for proper currency formatting.
  * **Authentication**:
      * Upon successful login, JWT access and refresh tokens are stored securely (e.g., HTTP-only cookies for refresh tokens, memory for access tokens, or a combination depending on security posture).
      * Access tokens are included in `Authorization` headers for all authenticated API requests.
      * Logic for refreshing expired access tokens using the refresh token.
  * **Responsiveness**: Heavy use of Tailwind's responsive prefixes (e.g., `sm:`, `md:`, `lg:`) to ensure optimal layout and readability across various screen sizes and orientations.

#### 4.2. Backend Services (Python Flask)

Each Flask service will be built using a minimal Flask application, leveraging extensions for common functionalities.

  * **Core Libraries/Extensions (per service as needed)**:

      * **Flask**: Web framework.
      * **SQLAlchemy**: Object Relational Mapper (ORM) for interacting with PostgreSQL.
      * **`psycopg2`**: PostgreSQL adapter for Python.
      * **Flask-RESTful**: For quickly building REST APIs.
      * **Flask-JWT-Extended**: For handling JWT-based authentication (access tokens, refresh tokens).
      * **`marshmallow`**: For request/response data serialization and validation.
      * **`dotenv`**: For managing environment variables.
      * **`requests`**: For making external HTTP calls (e.g., to currency API, other microservices).
      * **`werkzeug.security`**: For password hashing (e.g., `generate_password_hash`, `check_password_hash` using bcrypt).

  * **Service-Specific Details**:

    ##### 4.2.1. Authentication Service

      * **Routes**: `/register`, `/login`, `/refresh`, `/forgot_password`, `/reset_password`, `/verify_email`.
      * **Password Storage**: `bcrypt` hashing.
      * **Tokens**: Generates JWT access tokens (short-lived) and refresh tokens (long-lived) upon successful login.
      * **Email Integration**: Interacts with the Email Service to send verification and password reset emails.

    ##### 4.2.2. User Service

      * **Routes**: `/users/{id}`, `/users/{id}/addresses`.
      * **Data**: Manages user profiles (name, email, preferences) and multiple shipping/billing addresses.

    ##### 4.2.3. Product Service (PIM)

      * **Routes**: `/products`, `/products/{id}`, `/categories`.
      * **Data**: Stores product base information (SKU, base price, inventory).
      * **Localization**: Retrieves product name and description based on the `Accept-Language` header from the `product_localized_details` table.
      * **Currency Conversion (Internal Call)**: For `GET /products/{id}` or `GET /products`, the service will call the **Localization Service** to get the converted price based on the requested currency before sending the response to the frontend.
      * **Inventory Management**: Updates `inventory_quantity` for products upon order placement/cancellation.

    ##### 4.2.4. Order Service (OMS)

      * **Routes**: `/cart`, `/orders`, `/orders/{id}`.
      * **Cart Persistence**: Stores cart items in the database.
      * **Order Creation**:
          * Calculates total based on current product prices (in the user's selected currency).
          * Stores order details, including the selected currency and the price of each item at the time of purchase.
          * Reduces product inventory via communication with the Product Service.
          * Initiates payment processing via the Payment Service.
      * **Order Status**: Manages state transitions for orders (e.g., `pending`, `paid`, `shipped`, `delivered`).

    ##### 4.2.5. Payment Service

      * **Routes**: `/payments/process`, `/payments/webhook/{gateway_name}`.
      * **Gateway Integration**: Flask service integrates with payment gateway SDKs/APIs (e.g., Stripe Python library).
      * **Security**: Minimal sensitive data handling; relies on tokenization/hosted solutions from payment gateways.
      * **Webhooks**: Configures webhook endpoints to receive payment status updates from gateways (e.g., successful payment, failure, refund). Updates Order Service upon transaction completion.

    ##### 4.2.6. Localization Service

      * **Routes**: `/languages`, `/currencies`, `/convert_currency`.
      * **Exchange Rate Update**: A scheduled task (e.g., using `APScheduler` within the Flask app or an external cron job) fetches daily exchange rates from a reliable external API (e.g., ECB, Open Exchange Rates API) and stores them in PostgreSQL.
      * **Conversion Logic**: Provides an internal endpoint for other services to convert amounts between currencies using the latest stored rates.
      * **Database**: Stores supported languages, currencies, and their respective exchange rates.

    ##### 4.2.7. Admin Service

      * **Routes**: Dedicated routes for `/admin/products`, `/admin/users`, `/admin/orders`, `/admin/localization`.
      * **Access Control**: Implements strict role-based access control (RBAC) to ensure only authorized administrators can access these endpoints.
      * **Orchestration**: Acts as an intermediary, calling other microservices (Product, User, Order, Localization) to perform administrative actions.

#### 4.3. Database (PostgreSQL)

  * **Deployment**: Can be a managed PostgreSQL service in the cloud or a self-hosted instance.
  * **Schema Design Principles**:
      * **Normalized Design**: Follows relational database normalization principles to reduce data redundancy.
      * **UUID Primary Keys**: All primary keys will be UUIDs (`UUID` type in PostgreSQL, generated using `uuid_generate_v4()` from `uuid-ossp` extension).
      * **Decimal for Money**: Use `DECIMAL` data type for all monetary values to ensure precision and avoid floating-point inaccuracies.
      * **JSONB for Flexible Data**: Utilize `JSONB` type for storing semi-structured data, like payment gateway responses or product attributes that might vary widely.
      * **Indexing**: Create indexes on foreign keys and frequently queried columns to optimize read performance.
      * **Timestamp Columns**: `created_at` and `updated_at` columns with `TIMESTAMP WITH TIME ZONE` for all major entities.
  * **Key Tables (Illustrative, not exhaustive)**:
      * `users`: `id (UUID PK)`, `email (UNIQUE)`, `password_hash`, `status`, `roles (ARRAY/JSONB)`, `created_at`, `updated_at`.
      * `user_profiles`: `id (UUID PK)`, `user_id (UUID FK)`, `first_name`, `last_name`, `phone`, `default_language_id (FK)`, `default_currency_id (FK)`.
      * `user_addresses`: `id (UUID PK)`, `user_id (UUID FK)`, `address_line1`, `city`, `country_code`, `postal_code`, `type (ENUM: 'shipping', 'billing')`.
      * `languages`: `id (PK)`, `code (VARCHAR UNIQUE, e.g., 'en', 'zh')`, `name`.
      * `currencies`: `id (PK)`, `code (VARCHAR UNIQUE, e.g., 'USD', 'CNY')`, `symbol`, `name`.
      * `exchange_rates`: `id (PK)`, `from_currency_id (FK)`, `to_currency_id (FK)`, `rate (DECIMAL)`, `last_updated_at`.
      * `products`: `id (UUID PK)`, `sku (UNIQUE)`, `base_price (DECIMAL)`, `inventory_quantity (INT)`, `primary_image_url`, `category_id (UUID FK)`, `created_at`, `updated_at`.
      * `product_localized_details`: `product_id (UUID FK)`, `language_id (FK)`, `name`, `description`, `seo_title`, `seo_description`, `PRIMARY KEY (product_id, language_id)`.
      * `categories`: `id (UUID PK)`, `parent_id (UUID FK)`, `name`, `localized_name (JSONB)`.
      * `carts`: `id (UUID PK)`, `user_id (UUID FK UNIQUE)`, `created_at`, `updated_at`.
      * `cart_items`: `id (UUID PK)`, `cart_id (UUID FK)`, `product_id (UUID FK)`, `quantity`, `price_at_add (DECIMAL)`, `currency_id (FK)`.
      * `orders`: `id (UUID PK)`, `user_id (UUID FK)`, `shipping_address_id (UUID FK)`, `billing_address_id (UUID FK)`, `order_total (DECIMAL)`, `order_currency_id (FK)`, `status (VARCHAR)`, `created_at`, `updated_at`.
      * `order_items`: `id (UUID PK)`, `order_id (UUID FK)`, `product_id (UUID FK)`, `quantity`, `price_per_unit (DECIMAL)`, `currency_id (FK)`.
      * `transactions`: `id (UUID PK)`, `order_id (UUID FK)`, `gateway_transaction_id (UNIQUE)`, `amount (DECIMAL)`, `currency_id (FK)`, `status (VARCHAR)`, `gateway_response (JSONB)`, `created_at`.

#### 4.4. API Gateway / Load Balancer (Nginx)

  * **Role**:
      * **Reverse Proxy**: All client requests are routed through Nginx.
      * **Load Balancing**: Distributes incoming requests across multiple instances of each Flask microservice.
      * **SSL Termination**: Handles HTTPS, offloading encryption/decryption from backend services.
      * **Request Routing**: Routes requests to the appropriate backend service based on URL path (e.g., `/api/auth` to Auth Service, `/api/products` to Product Service).
      * **Authentication (Optional Pre-Check)**: Can perform basic JWT validation or pass JWT headers to backend services.
      * **Rate Limiting**: Configured to protect backend services from excessive requests.
  * **Configuration Example (Illustrative)**:
    ```nginx
    server {
        listen 80;
        listen 443 ssl;
        server_name yourdomain.com;

        # SSL Configuration (assuming certificates are in place)
        ssl_certificate /etc/nginx/ssl/yourdomain.com.crt;
        ssl_certificate_key /etc/nginx/ssl/yourdomain.com.key;

        location / {
            # Serve React static files
            root /var/www/frontend_build;
            try_files $uri /index.html;
        }

        location /api/auth/ {
            proxy_pass http://auth_service_upstream; # points to Docker/K8s service name
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            # ... other proxy headers
        }
        # ... similar blocks for other microservices (/api/users/, /api/products/, etc.)
    }

    upstream auth_service_upstream {
        server auth-service:5000; # Example for Docker/K8s service discovery
    }
    # ... upstreams for other microservices
    ```

#### 4.5. External Services & Integrations

  * **Payment Gateways**:
      * **Stripe**: For credit card processing, international payments.
      * **PayPal**: Widely used for online payments.
      * **Alipay/WeChat Pay**: Essential for the Chinese market.
      * Integration via official Python SDKs in the Payment Service.
  * **Currency Exchange Rate API**:
      * **Open Exchange Rates / European Central Bank (ECB) API**: Fetched by Localization Service.
  * **Email Service**:
      * **SendGrid / Mailgun**: For transactional emails (user registration, password resets, order confirmations). Integrated via their respective Python SDKs in relevant services (e.g., Authentication Service, Order Service).
  * **Cloud Storage (for media)**:
      * **AWS S3 / Google Cloud Storage**: For storing product images, videos, and other media assets. Product Service will manage URLs to these assets.
  * **Content Delivery Network (CDN)**:
      * **Cloudflare / AWS CloudFront**: To cache and deliver static frontend assets (JS, CSS, images) globally, improving loading times.

### 5\. Cross-Cutting Concerns

#### 5.1. Security

  * **Authentication**: JWT for API authentication, `bcrypt` for password hashing, email verification for new accounts.
  * **Authorization**: Role-Based Access Control (RBAC) implemented in backend services using Flask interceptors/decorators to verify user roles and permissions for specific endpoints.
  * **HTTPS**: All communication over HTTPS. Nginx handles SSL termination.
  * **Input Validation**: Strict server-side validation of all API inputs using `marshmallow` schemas or similar to prevent injection attacks (SQL, XSS).
  * **CORS**: Properly configured CORS headers in Flask services to allow requests only from the frontend domain.
  * **Rate Limiting**: Applied at the API Gateway and potentially within individual Flask services for critical endpoints (login, registration).
  * **Sensitive Data**: Minimal storage of sensitive data. PCI DSS compliance for payment processing (relying on gateway tokenization).
  * **Error Handling**: Generic error responses, avoiding exposing sensitive server details.
  * **Dependency Security**: Regular updates and vulnerability scanning of Python packages and Node.js dependencies.

#### 5.2. Performance & Scalability

  * **Load Balancing**: Nginx distributes traffic across multiple instances of each Flask microservice.
  * **Horizontal Scaling**: Flask services designed to be stateless and easily scalable by adding more instances behind the load balancer.
  * **Database Scaling**: PostgreSQL can be scaled with read replicas (for read-heavy operations) and potentially sharding for extreme load (future consideration).
  * **Caching**:
      * **Redis**: For API response caching (e.g., frequently accessed product lists, exchange rates).
      * **CDN**: For frontend static assets and media files.
  * **Asynchronous Processing**: Use background tasks or message queues (e.g., Celery with Redis/RabbitMQ, or a simple Flask-APScheduler for cron-like jobs) for non-critical, long-running operations (e.g., sending emails, updating exchange rates).
  * **Optimized Queries**: Efficient SQL queries with proper indexing.

#### 5.3. Monitoring & Logging

  * **Centralized Logging**: All Flask services will log to `stdout`/`stderr` which will be collected by a logging system (e.g., Fluentd, Logstash) and pushed to a centralized log management platform (e.g., ELK Stack, Datadog Logs).
  * **Application Performance Monitoring (APM)**: Integration of APM tools (e.g., Prometheus, Grafana, OpenTelemetry with Jaeger) for tracing requests across microservices, monitoring resource utilization, and identifying bottlenecks.
  * **Alerting**: Configured alerts for critical errors, service downtime, high latency, and resource exhaustion.

#### 5.4. Continuous Integration/Continuous Deployment (CI/CD)

  * **Version Control**: Git (e.g., GitHub, GitLab).
  * **Pipelines**: Automated CI/CD pipelines (e.g., GitHub Actions, GitLab CI) for:
      * Code Linting (ESLint for React, Flake8/Black for Python).
      * Unit and Integration Testing.
      * Docker Image Building for each service.
      * Image Registry Push.
      * Kubernetes Deployment (Rolling Updates).

#### 5.5. Error Handling & Resilience

  * **Graceful Degradation**: Design services to handle failures of dependencies gracefully (e.g., if currency API is down, use last known rates).
  * **Circuit Breakers**: Implement patterns like circuit breakers (e.g., using `pybreaker`) to prevent cascading failures between microservices.
  * **Retry Mechanisms**: Implement retry logic for transient network or service errors in inter-service communication.
  * **Idempotency**: Ensure critical operations (e.g., payment processing) are idempotent to prevent unintended side effects on retries.

### 6\. Development Environment & Tools

  * **IDE**: VS Code, PyCharm.
  * **Containerization**: Docker Desktop.
  * **Database Client**: DBeaver, pgAdmin.
  * **API Testing**: Postman, Insomnia.
  * **Package Managers**: `npm`/`yarn` for React, `pip`/`pipenv`/`Poetry` for Python.
