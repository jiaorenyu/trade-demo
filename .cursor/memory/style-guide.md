# Style Guide: Global E-commerce Platform

## Code Style Standards

### Python (Flask Services)
- **Formatter**: Black (line length: 88 characters)
- **Linter**: Flake8
- **Import Order**: isort
- **Docstrings**: Google style docstrings
- **Type Hints**: Use type hints for function parameters and return values

#### Naming Conventions
- **Functions/Variables**: snake_case
- **Classes**: PascalCase
- **Constants**: UPPER_SNAKE_CASE
- **Files**: snake_case.py
- **Modules**: snake_case

#### Flask Service Structure
```python
# app.py structure
from flask import Flask
from flask_restful import Api
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
api = Api(app)

# Resource registration
api.add_resource(ResourceClass, '/endpoint')
```

### JavaScript/React (Frontend)
- **Formatter**: Prettier
- **Linter**: ESLint
- **Style**: Airbnb JavaScript Style Guide
- **Components**: Functional components with hooks

#### Naming Conventions
- **Components**: PascalCase
- **Files**: PascalCase.jsx
- **Functions/Variables**: camelCase
- **Constants**: UPPER_SNAKE_CASE
- **CSS Classes**: Tailwind utility classes

#### React Component Structure
```jsx
import React, { useState, useEffect } from 'react';

const ComponentName = ({ prop1, prop2 }) => {
  const [state, setState] = useState(initialValue);
  
  useEffect(() => {
    // Side effects
  }, [dependencies]);
  
  return (
    <div className="tailwind-classes">
      {/* Component JSX */}
    </div>
  );
};

export default ComponentName;
```

### Database (PostgreSQL)
- **Table Names**: snake_case, plural
- **Column Names**: snake_case
- **Indexes**: idx_tablename_columnname
- **Constraints**: fk_tablename_columnname, uk_tablename_columnname

#### Schema Standards
- **Primary Keys**: UUID using uuid_generate_v4()
- **Timestamps**: created_at, updated_at (TIMESTAMP WITH TIME ZONE)
- **Money**: DECIMAL(10,2) or higher precision as needed
- **Foreign Keys**: Explicit naming with _id suffix

## API Design Standards

### REST API Conventions
- **HTTP Methods**: GET (read), POST (create), PUT (update), DELETE (delete)
- **Status Codes**: 200 (OK), 201 (Created), 400 (Bad Request), 401 (Unauthorized), 404 (Not Found), 500 (Server Error)
- **Content-Type**: application/json
- **Authentication**: Bearer tokens in Authorization header

### Endpoint Naming
- **Resources**: Plural nouns (/users, /products, /orders)
- **Actions**: HTTP verbs (GET /users, POST /users, PUT /users/{id})
- **Nested Resources**: /users/{id}/addresses
- **Filtering**: Query parameters (?status=active&category=electronics)

### Response Format
```json
{
  "success": true,
  "data": {
    // Response data
  },
  "message": "Operation successful",
  "errors": []
}
```

## Documentation Standards

### Code Documentation
- **Python**: Google-style docstrings
- **JavaScript**: JSDoc comments
- **API**: OpenAPI/Swagger specifications
- **Database**: Schema documentation with descriptions

### Commit Messages
- **Format**: `type(scope): description`
- **Types**: feat, fix, docs, style, refactor, test, chore
- **Examples**: 
  - `feat(auth): add JWT refresh token mechanism`
  - `fix(payment): handle Stripe webhook timeout`

## Testing Standards

### Python Tests
- **Framework**: pytest
- **Coverage**: Minimum 80% coverage
- **Structure**: Arrange-Act-Assert pattern
- **Mocking**: Use unittest.mock for external dependencies

### JavaScript Tests
- **Framework**: Jest + React Testing Library
- **Coverage**: Minimum 80% coverage
- **Structure**: Describe-It pattern
- **Components**: Test user interactions, not implementation

## Security Standards

### Authentication
- **Passwords**: bcrypt hashing, minimum 8 characters
- **Tokens**: JWT with expiration, refresh token rotation
- **Sessions**: Secure, HttpOnly cookies where applicable

### Input Validation
- **Server-side**: Always validate on the server
- **Sanitization**: Escape all user inputs
- **SQL Injection**: Use parameterized queries/ORM
- **XSS Prevention**: Sanitize HTML content

## Performance Standards

### Frontend
- **Bundle Size**: Monitor and optimize bundle sizes
- **Lazy Loading**: Implement code splitting
- **Caching**: Use browser caching effectively
- **Images**: Optimize images and use appropriate formats

### Backend
- **Database**: Use indexes for frequently queried columns
- **Caching**: Implement Redis caching for frequently accessed data
- **Async**: Use async operations for I/O-bound tasks
- **Monitoring**: Log performance metrics

## Deployment Standards

### Environment Configuration
- **Variables**: Use environment variables for configuration
- **Secrets**: Never commit secrets to version control
- **Configs**: Separate configs for dev/staging/prod

### Docker
- **Base Images**: Use official, minimal base images
- **Layers**: Optimize Docker layers for caching
- **Security**: Run containers as non-root users
- **Health Checks**: Implement health check endpoints
