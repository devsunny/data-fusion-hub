# Data Fusion Hub Service

A comprehensive API service for managing data domains, connectors, and objects in the Data Fusion Hub ecosystem with enhanced user role management capabilities.

## Overview

The Data Fusion Hub Service provides a RESTful API for managing data assets including domains, connectors, and objects. This implementation includes a complete User Role Request system that allows users to request membership in additional roles beyond their default "public" role, with approval workflows managed by designated approver roles.

## Features

### Core Functionality
- **Data Management**: CRUD operations for data domains, connectors, and objects
- **User Authentication & Authorization**: Secure access control mechanisms  
- **Role Management**: Comprehensive role-based access control system
- **User Role Requests**: Request and approval workflow for additional roles

### User Role Request System
The service implements a complete user role request system with:
- Request submission with justification requirements
- Approval workflows with designated approver roles
- Optional reason fields for approvals/denials  
- Database persistence ready for ActiveMQ notifications
- Administrative functionality to assign approver roles

## Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Client Apps   │    │  Data Fusion     │    │   Database      │
│                 │    │   Service API    │    │                 │
│  ┌───────────┐  │    │  ┌─────────────┐ │    │  ┌────────────┐ │
│  │           │  │    │  │             │ │    │  │            │ │
│  │   Frontend│  │    │  │ API Routes  │ │    │  │   SQLite   │ │
│  │           │  │    │  │             │ │    │  │            │ │
│  └───────────┘  │    │  └─────────────┘ │    │  └────────────┘ │
│                 │    │                  │    │                 │
│  ┌───────────┐  │    │  ┌─────────────┐ │    │  ┌────────────┐ │
│  │           │  │    │  │             │ │    │  │            │ │
│  │   Mobile  │  │    │  │   Models    │ │    │  │  Tables    │ │
│  │           │  │    │  │             │ │    │  │            │ │
│  └───────────┘  │    │  └─────────────┘ │    │  └────────────┘ │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## API Endpoints

### Data Management
- `GET /datadomains` - Get all data domains  
- `POST /datadomains` - Create a new data domain
- `GET /datadomains/{id}` - Get specific data domain
- `PUT /datadomains/{id}` - Update data domain
- `DELETE /datadomains/{id}` - Delete data domain

### Data Connectors  
- `GET /dataconnectors` - Get all connectors
- `POST /dataconnectors` - Create a new connector
- `GET /dataconnectors/{id}` - Get specific connector
- `PUT /dataconnectors/{id}` - Update connector
- `DELETE /dataconnectors/{id}` - Delete connector

### Data Objects
- `GET /dataobjects` - Get all data objects
- `POST /dataobjects` - Create a new data object  
- `GET /dataobjects/{id}` - Get specific data object
- `PUT /dataobjects/{id}` - Update data object
- `DELETE /dataobjects/{id}` - Delete data object

### Users & Roles
- `GET /users` - Get all users
- `POST /users` - Create a new user
- `GET /users/{id}` - Get specific user  
- `PUT /users/{id}` - Update user
- `DELETE /users/{id}` - Delete user

### User Role Requests (New Feature)
- `POST /user-role-requests` - Submit role request with justification
- `GET /user-role-requests` - List user's requests
- `GET /user-role-requests/{id}` - Get specific request details  
- `PUT /user-role-requests/{id}/approve` - Approve a request
- `PUT /user-role-requests/{id}/deny` - Deny a request

### Role Approver Management
- `PUT /roles/{role_id}/approver-roles` - Assign approver roles to existing role
- `GET /roles/{role_id}/approver-roles` - Get approver roles for a specific role

## Installation

### Prerequisites
- Python 3.12+
- pip (Python package manager)

### Setup Instructions

1. **Clone the repository**:
```bash
git clone <repository-url>
cd data-fusion-service
```

2. **Create and activate virtual environment**:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Run the application**:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

## Usage Examples

### Create a User Role Request
```bash
curl -X POST "http://localhost:8000/user-role-requests" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user-123",
    "role_id": "role-456", 
    "justification": "Need admin access for project management"
  }'
```

### Approve a Role Request
```bash
curl -X PUT "http://localhost:8000/user-role-requests/req-789/approve" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "approved",
    "reason": "Manager approved access request"
  }'
```

### Assign Approver Roles
```bash
curl -X PUT "http://localhost:8000/roles/role-456/approver-roles" \
  -H "Content-Type: application/json" \
  -d '["role-111", "role-222"]'
```

## Database

The service uses SQLite for data persistence with the following tables:
- `datadomains` - Data domain information
- `dataconnectors` - Connector configurations  
- `dataobjects` - Data object metadata
- `users` - User accounts and profiles
- `roles` - Role definitions
- `user_role_requests` - Role request tracking
- `role_approver_relationships` - Approver role mappings

## Testing

Run tests using pytest:
```bash
pytest tests/
```

## Documentation

Comprehensive API documentation is available in the `/docs` directory and can be accessed at:
- **API Docs**: `http://localhost:8000/docs`
- **Swagger UI**: `http://localhost:8000/redoc`

## Security Considerations

- All endpoints require proper authentication
- Role-based access control implemented throughout
- Passwords are hashed using bcrypt encryption  
- JWT tokens for secure session management

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)  
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a pull request

## Support

For support, please open an issue in the GitHub repository or contact the development team.