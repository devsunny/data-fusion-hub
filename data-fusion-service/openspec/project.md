# Data Fusion Hub Service Project Specification

## Overview

This document defines the specification for the Data Fusion Hub Service - a FastAPI-based RESTful API backend service that serves as the core component of the data fusion hub system. The service provides role management and user authentication capabilities with audit trails, following established microservices architecture patterns.

## Project Name
Data Fusion Hub Service (data-fusion-hub-service)

## Purpose
The Data Fusion Hub Service acts as the foundational RESTful API backend for the data fusion hub ecosystem. It provides core functionality including:
- Role-based access control system 
- User registration and authentication with password hashing
- Audit trail support through created_by/updated_by fields
- Database persistence using SQLAlchemy ORM

## Tech Stack

### Core Frameworks
- **FastAPI**: Main web framework for building RESTful APIs with automatic OpenAPI documentation
- **SQLAlchemy**: Object-relational mapping for database operations
- **Pydantic**: Data validation and settings management using Python type annotations

### Security & Authentication
- **JWT (JSON Web Tokens)**: For secure authentication and session management
- **bcrypt**: Password hashing library for secure credential storage
- **python-jose**: JWT token handling utilities
- **passlib**: Comprehensive password hashing library

### Development Tools
- **pytest**: Testing framework with fixtures and parametrized testing
- **uvicorn**: ASGI server for running the FastAPI application
- **Docker Compose**: Container orchestration for development environment setup

### Database & Infrastructure
- **PostgreSQL**: Primary database for persistent data storage
- **ActiveMQ**: Message broker for asynchronous communication (in development)
- **Redis**: Caching layer and message queuing (in development)

## Architecture Patterns

### Microservices Architecture
This service follows a microservices pattern, designed to be part of a larger ecosystem where:
- Each service has a single responsibility 
- Services communicate through well-defined APIs
- The data-fusion-hub-service-api is the first component in this ecosystem

### API Design Principles
- RESTful endpoints with consistent naming conventions
- HTTP status codes for proper error handling
- JSON-based request/response format
- Versioned API routes (`/api/v1/`)
- Comprehensive documentation through OpenAPI/Swagger

### Data Models
All data models follow these conventions:
- UUID primary keys for all entities
- Audit trail fields (created_by, updated_by) on all entities
- Proper validation using Pydantic models
- Timestamps for created_at and updated_at fields

## Project Structure

```
data-fusion-hub-service/
├── app/                    # Main application code
│   ├── api/                # API routes and controllers  
│   │   └── v1/             # Version 1 of the API
│   │       ├── auth.py     # Authentication endpoints
│   │       ├── roles.py    # Role management endpoints
│   │       ├── users.py    # User management endpoints
│   │       └── datasources.py # Data source registration endpoints  
│   ├── core/               # Core application components
│   │   ├── database.py     # Database configuration and connection
│   │   └── security.py     # Security utilities (JWT, password hashing)
│   ├── models/             # Data models and Pydantic schemas
│   ├── repositories/       # Repository patterns for data access
│   ├── services/           # Business logic layer
│   └── utils/              # Utility functions
├── tests/                  # Test suite
├── openspec/               # OpenSpec documentation and change management
│   ├── changes/            # Versioned specification changes
│   └── project.md          # Project specification (this file)
├── specs/                  # Detailed technical specifications
├── Dockerfile              # Container configuration
├── docker-compose.yml      # Development environment setup
└── requirements.txt        # Python dependencies
```

## Conventions

### Naming Conventions
- **Endpoints**: Use lowercase with hyphens for paths (e.g., `/users`, `/auth/login`)
- **Models**: PascalCase for class names, snake_case for attributes  
- **Variables**: snake_case for variables and functions
- **Files**: snake_case for file names

### API Response Format
All successful responses return JSON objects. Error responses follow this format:
```json
{
  "detail": "Error message describing the problem"
}
```

### HTTP Status Codes
- `200 OK` - Successful GET, PUT, PATCH requests
- `201 Created` - Successful POST requests that create resources  
- `204 No Content` - Successful DELETE requests
- `400 Bad Request` - Invalid request data
- `401 Unauthorized` - Authentication required or invalid credentials
- `403 Forbidden` - Insufficient permissions for the requested action
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Unexpected server error

### Database Conventions
- All entities use UUID primary keys (string format)
- Audit trail fields: created_by, updated_by (both optional strings)  
- Timestamps: created_at, updated_at (datetime objects)
- Foreign key relationships are properly defined with constraints

## Implementation Status

This service implements the following OpenSpec changes:

✅ **Original change `20251122-145359`**: Role model with UUID primary key, name, and description  
✅ **Enhancement `20251122-150102`**: Added created_by and updated_by fields for audit trail support  
✅ **New change `20251122-151049`**: User registration service with email, name information and optional password authentication
✅ **Update `20251122-163000`**: Updated to use modern Pydantic v2 API (from_attributes instead of orm_mode)
✅ **New change `20251122-170000`**: Added Docker Compose configuration for development environment
✅ **Authentication feature `20251122-180000`**: JWT-based login endpoint with token generation  
✅ **Data Source Registration Service `20251122-172403`**: Comprehensive data source registration service supporting 18 different types

## Development Environment Setup

### Prerequisites
- Python 3.8+
- Docker and Docker Compose (for development environment)
- PostgreSQL database access

### Local Development
1. Install dependencies: `pip install -r requirements.txt`
2. Start services using Docker Compose: `docker-compose up -d`  
3. Run the application: `uvicorn app.main:app --reload`
4. Access API documentation at: `http://localhost:8000/docs`

### Testing
Run tests with: `pytest tests/`

## Future Considerations

- Implement comprehensive role-based access control (RBAC) system
- Add more robust authentication methods (OAuth2, SAML)
- Include rate limiting for API endpoints  
- Add request/response logging middleware
- Implement health check and monitoring endpoints
- Add support for multi-tenancy if needed in future versions