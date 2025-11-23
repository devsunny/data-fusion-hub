# Data Fusion Hub

## Overview

Data Fusion Hub is a comprehensive system for managing data fusion components with role-based access control and user management capabilities.

## Project Structure

```
data-fusion-hub/
├── data-fusion-service/     # Main FastAPI service
├── docker-compose.yml       # Docker Compose configuration  
├── ADD_SUDOERS_INSTRUCTIONS.md  # Instructions for sudoers setup
└── scripts/                 # Utility scripts
    └── add-sudoers.sh       # Script to configure passwordless sudo
```

## Getting Started

### Prerequisites

- Python 3.8+
- Docker and Docker Compose (for development environment)
- PostgreSQL, ActiveMQ, Redis services (via docker-compose)

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd data-fusion-hub

# Start all required services using Docker Compose
docker-compose up -d

# Install Python dependencies for the service
pip install -r data-fusion-service/requirements.txt
```

### Running the Service

```bash
# Run with uvicorn directly (requires database setup)
uvicorn data-fusion-service/app/main:app --reload

# Or use Docker Compose to start all services including the API
docker-compose up -d
```

## Development Environment Setup

For local development, you can use the provided Docker Compose setup which includes:

1. **PostgreSQL** (port 5432) - Primary database  
2. **ActiveMQ** (ports 8161, 61616, 5672) - Message broker
3. **Redis** (port 6379) - Caching layer

To start the development environment:
```bash
docker-compose up -d
```

The service will be available at `http://localhost:8000`.

## System Administration

### Adding Users to Sudoers Without Password

For certain deployment scenarios, you may need passwordless sudo access. See detailed instructions in:

- [ADD_SUDOERS_INSTRUCTIONS.md](ADD_SUDOERS_INSTRUCTIONS.md)
- [scripts/add-sudoers.sh](scripts/add-sudoers.sh)

**⚠️ Security Warning**: Granting passwordless sudo access reduces system security. Only use this approach in controlled environments.

## API Documentation

The service exposes RESTful APIs for managing roles and users:

### Roles
- `POST /roles` - Create a new role  
- `GET /roles` - List all roles
- `GET /roles/{role_id}` - Get a specific role by ID
- `PUT /roles/{role_id}` - Update an existing role
- `DELETE /roles/{role_id}` - Delete a role

### Users
- `POST /users` - Register a new user
- `GET /users` - List all users  
- `GET /users/{user_id}` - Get a specific user by ID
- `PUT /users/{user_id}` - Update an existing user
- `DELETE /users/{user_id}` - Delete a user

## Implementation Status

This service implements the following OpenSpec changes:

✅ **Original change `20251122-145359`**: Role model with UUID primary key, name, and description  
✅ **Enhancement `20251122-150102`**: Added created_by and updated_by fields for audit trail support  
✅ **New change `20251122-151049`**: User registration service with email, name information and optional password authentication
✅ **Update `20251122-163000`**: Updated to use modern Pydantic v2 API (from_attributes instead of orm_mode)
✅ **New change `20251122-170000`**: Added Docker Compose configuration for development environment
✅ **New change `20251122-173000`**: Documentation and scripts for sudoers configuration

## Testing

Run tests with:
```bash
pytest data-fusion-service/tests/
```

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.