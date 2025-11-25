# User Role Request API Documentation

## Overview

The User Role Request service enables users to request membership in additional roles beyond their default "public" role. Requests must be approved by designated approver roles before being granted, with comprehensive approval workflows and administrative capabilities.

## Base URL
`http://localhost:8000`

## Authentication

All endpoints require proper authentication headers:
```
Authorization: Bearer <JWT_TOKEN>
```

## Data Models

### UserRoleRequestDB
```json
{
  "id": "uuid",
  "user_id": "uuid", 
  "role_id": "uuid",
  "justification": "string",
  "reason": "string|null",
  "status": "pending|approved|denied",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

### RoleApproverRelationshipDB
```json
{
  "role_id": "uuid",
  "approver_role_id": "uuid"
}
```

## Endpoints

### Create User Role Request
**POST** `/user-role-requests`

Create a new role request with justification.

#### Request Body
```json
{
  "user_id": "string",
  "role_id": "string", 
  "justification": "string"
}
```

#### Response
- **201 Created**: Role request created successfully
- **400 Bad Request**: Invalid input data
- **401 Unauthorized**: Authentication required  
- **403 Forbidden**: Insufficient permissions

### Get User Role Requests
**GET** `/user-role-requests`

List all role requests for the authenticated user.

#### Response
```json
[
  {
    "id": "uuid",
    "user_id": "uuid",
    "role_id": "uuid", 
    "justification": "string",
    "reason": "string|null",
    "status": "pending|approved|denied",
    "created_at": "datetime",
    "updated_at": "datetime"
  }
]
```

### Get Specific Role Request
**GET** `/user-role-requests/{id}`

Get details of a specific role request.

#### Response  
- **200 OK**: Request details returned
- **404 Not Found**: Request not found
- **401 Unauthorized**: Authentication required

### Approve Role Request
**PUT** `/user-role-requests/{id}/approve`

Approve a pending role request.

#### Request Body
```json
{
  "status": "approved",
  "reason": "string|null"
}
```

#### Response
- **200 OK**: Request approved successfully  
- **400 Bad Request**: Invalid status or missing fields
- **401 Unauthorized**: Authentication required
- **403 Forbidden**: Insufficient permissions

### Deny Role Request
**PUT** `/user-role-requests/{id}/deny`

Deny a pending role request.

#### Request Body
```json
{
  "status": "denied", 
  "reason": "string|null"
}
```

#### Response
- **200 OK**: Request denied successfully
- **400 Bad Request**: Invalid status or missing fields  
- **401 Unauthorized**: Authentication required
- **403 Forbidden**: Insufficient permissions

### Assign Approver Roles
**PUT** `/roles/{role_id}/approver-roles`

Assign one or more roles as approvers to an existing role.

#### Request Body
```json
["role-id-1", "role-id-2"]
```

#### Response
- **200 OK**: Approver roles assigned successfully  
- **400 Bad Request**: Invalid input data
- **401 Unauthorized**: Authentication required
- **403 Forbidden**: Insufficient permissions

### Get Approver Roles
**GET** `/roles/{role_id}/approver-roles`

Get all approver roles for a specific role.

#### Response
```json
["role-id-1", "role-id-2"]
```

## Approval Workflow Process

1. **Request Submission**: User submits role request with justification  
2. **Validation**: System validates that:
   - Role is not "public" 
   - User and target role exist
   - Justification is provided
3. **Approval Processing**: 
   - Request waits for approver roles to review
   - Approvers can optionally provide reasons
4. **Outcome**:
   - Approved: Request status changes to "approved" 
   - Denied: Request status changes to "denied"
5. **Role Assignment**: Upon approval, user is assigned the requested role

## Error Handling

All endpoints return appropriate HTTP status codes and error messages:

- **400 Bad Request**: Invalid request data
- **401 Unauthorized**: Authentication required  
- **403 Forbidden**: Insufficient permissions
- **404 Not Found**: Resource not found
- **500 Internal Server Error**: Server-side errors

## Usage Examples

### Create a Role Request
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

## Security Considerations

- All endpoints require proper authentication
- Only designated approver roles can approve/deny requests  
- Audit trail maintained through created_at/updated_at timestamps
- Reason fields contribute to compliance audit requirements